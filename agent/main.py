import dagger
import asyncio
import sys
import time
import os
import json
import argparse
import docker

class DaggerOrchestrator:
    """
    Dagger Orchestrator for deploying and managing containerized applications.
    This class uses Dagger to deploy and orchestrate a three-tier application 
    across separate containers.
    """
    
    def __init__(self, project_dir="."):
        self.project_dir = project_dir
        self.client = None
        self.db_service = None
        self.api_service = None
        self.frontend_service = None
        self.config = self._load_config()
        self.docker_client = None
        self.container_ids = {}
        self._verify_docker_access()
        
    def _verify_docker_access(self):
        """Verify Docker socket access for container management"""
        try:
            self.docker_client = docker.from_env()
            self.docker_client.ping()
            print("✅ Docker socket access verified")
        except Exception as e:
            print(f"❌ Docker socket access failed: {str(e)}")
            print("Please ensure Docker is running and the socket is accessible")
            sys.exit(1)
        
    def _load_config(self):
        """Load configuration from config.json if it exists, otherwise use defaults"""
        config_path = os.path.join(self.project_dir, "agent", "config.json")
        default_config = {
            "db": {
                "image": "postgres:15-alpine",
                "env": {
                    "POSTGRES_PASSWORD": "postgres",
                    "POSTGRES_USER": "postgres",
                    "POSTGRES_DB": "postgres"
                },
                "port": 5432,
                "host_port": 5432,
                "network": "app-network"
            },
            "api": {
                "image": "python:3.11-slim",
                "port": 5000,
                "host_port": 5000,
                "network": "app-network"
            },
            "frontend": {
                "image": "node:20-alpine",
                "port": 3000,
                "host_port": 3001,
                "network": "app-network"
            },
            "registry": {
                "default_registry": "docker.io",
                "tag_prefix": "ai-agent-demo",
                "version": "latest"
            }
        }
        
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ Error loading config: {str(e)}. Using defaults.")
                return default_config
        return default_config
    
    async def initialize_client(self):
        """Initialize the Dagger client"""
        self.client = await dagger.Connection().__aenter__()
        return self.client
    
    async def setup_project_directory(self):
        """Set up the project directory in the Dagger client"""
        print("📂 Setting up project directories...")
        return self.client.host().directory(".", exclude=[".dagger", "__pycache__", "node_modules", ".git"])
    
    async def setup_network(self):
        """Set up Docker network for container communication"""
        network_name = "app-network"
        try:
            # Check if network exists
            networks = self.docker_client.networks.list(names=[network_name])
            if not networks:
                print(f"🌐 Creating Docker network: {network_name}")
                self.docker_client.networks.create(network_name, driver="bridge")
            else:
                print(f"✅ Using existing Docker network: {network_name}")
            return network_name
        except Exception as e:
            print(f"❌ Failed to set up network: {str(e)}")
            return None
    
    async def deploy_database(self, project_dir):
        """Deploy the PostgreSQL database container"""
        print("🛢️ Setting up PostgreSQL database...")
        db_config = self.config["db"]
        
        # Ensure network exists
        network_name = await self.setup_network()
        
        db = (
            self.client.container()
            .from_(db_config["image"])
        )
        
        # Add environment variables
        for key, value in db_config["env"].items():
            db = db.with_env_variable(key, value)
        
        # Add initialization scripts
        db = db.with_directory("/docker-entrypoint-initdb.d", project_dir.directory("db"))
        
        # Create service with exposed port
        self.db_service = db.as_service().with_exposed_port(db_config["port"])
        
        # Get container ID for host port mapping
        db_container = await db.with_exec(["pg_isready", "-U", "postgres"]).with_exposed_port(db_config["port"]).publish()
        db_container_id = db_container.id
        self.container_ids["db"] = db_container_id
        
        # Map container port to host port
        try:
            container = self.docker_client.containers.get(db_container_id)
            host_config = self.docker_client.api.create_host_config(
                port_bindings={db_config["port"]: db_config["host_port"]},
                network_mode=network_name
            )
            self.docker_client.api.update_container(
                container.id,
                host_config=host_config
            )
            print(f"✅ Database container exposed on host port {db_config['host_port']}")
        except Exception as e:
            print(f"⚠️ Failed to map database port to host: {str(e)}")
        
        return self.db_service
    
    async def deploy_api(self, project_dir):
        """Deploy the Flask API container"""
        print("🐍 Setting up Flask API...")
        api_config = self.config["api"]
        
        api = (
            self.client.container()
            .from_(api_config["image"])
            .with_directory("/app", project_dir.directory("api"))
            .with_workdir("/app")
            .with_exec(["pip", "install", "-r", "requirements.txt"])
        )
        
        self.api_service = (
            api.with_service_binding("db", self.db_service)
            .with_env_variable("FLASK_APP", "app.py")
            .with_env_variable("DATABASE_URL", f"postgresql://{self.config['db']['env']['POSTGRES_USER']}:{self.config['db']['env']['POSTGRES_PASSWORD']}@db:{self.config['db']['port']}/{self.config['db']['env']['POSTGRES_DB']}")
            .with_exec(["flask", "run", "--host=0.0.0.0"])
            .as_service()
            .with_exposed_port(api_config["port"])
        )
        
        # Get container ID for host port mapping
        api_container = await api.with_service_binding("db", self.db_service).with_exposed_port(api_config["port"]).publish()
        api_container_id = api_container.id
        self.container_ids["api"] = api_container_id
        
        # Map container port to host port
        try:
            container = self.docker_client.containers.get(api_container_id)
            host_config = self.docker_client.api.create_host_config(
                port_bindings={api_config["port"]: api_config["host_port"]},
                network_mode=api_config["network"]
            )
            self.docker_client.api.update_container(
                container.id,
                host_config=host_config
            )
            print(f"✅ API container exposed on host port {api_config['host_port']}")
        except Exception as e:
            print(f"⚠️ Failed to map API port to host: {str(e)}")
        
        return self.api_service
    
    async def deploy_frontend(self, project_dir):
        """Deploy the React frontend container"""
        print("⚛️ Setting up React frontend...")
        frontend_config = self.config["frontend"]
        
        frontend = (
            self.client.container()
            .from_(frontend_config["image"])
            .with_directory("/app", project_dir.directory("frontend"))
            .with_workdir("/app")
            .with_exec(["npm", "install"])
            .with_exec(["npm", "run", "build"])
            .with_exec(["npm", "install", "-g", "serve"])
        )
        
        self.frontend_service = (
            frontend
            .with_service_binding("api", self.api_service)
            .with_exec(["serve", "-s", "build", "-l", str(frontend_config["port"])])
            .as_service()
            .with_exposed_port(frontend_config["port"])
        )
        
        # Get container ID for host port mapping
        frontend_container = await frontend.with_service_binding("api", self.api_service).with_exposed_port(frontend_config["port"]).publish()
        frontend_container_id = frontend_container.id
        self.container_ids["frontend"] = frontend_container_id
        
        # Map container port to host port
        try:
            container = self.docker_client.containers.get(frontend_container_id)
            host_config = self.docker_client.api.create_host_config(
                port_bindings={frontend_config["port"]: frontend_config["host_port"]},
                network_mode=frontend_config["network"]
            )
            self.docker_client.api.update_container(
                container.id,
                host_config=host_config
            )
            print(f"✅ Frontend container exposed on host port {frontend_config['host_port']}")
        except Exception as e:
            print(f"⚠️ Failed to map frontend port to host: {str(e)}")
        
        return self.frontend_service
    
    async def perform_health_checks(self):
        """Perform health checks on all services"""
        print("🔍 Performing health checks...")
        print("  ⏳ Waiting for database to initialize...")
        # Give the database some time to initialize
        time.sleep(5)
        
        # Health check for API using host port
        api_config = self.config["api"]
        try:
            # First try internal service check
            test_api_health = (
                self.client.container()
                .from_("alpine/curl")
                .with_service_binding("api", self.api_service)
                .with_exec(["curl", "-s", "http://api:5000/api/health"])
            )
            api_health_output = await test_api_health.stdout()
            print(f"  ✅ API Internal Health Check: {api_health_output}")
            
            # Then try host port check
            host_check = self.docker_client.containers.run(
                "alpine/curl", 
                f"curl -s http://host.docker.internal:{api_config['host_port']}/api/health",
                network_mode="host",
                remove=True
            )
            print(f"  ✅ API Host Health Check: {host_check.decode('utf-8')}")
        except Exception as e:
            print(f"  ⚠️ API Health Check Warning: {str(e)}")
            print("  ⚠️ Continuing despite health check warning...")
            # Don't fail completely, as host networking might be different in some environments

        # Health check for quotes endpoint
        try:
            test_quotes = (
                self.client.container()
                .from_("alpine/curl")
                .with_service_binding("api", self.api_service)
                .with_exec(["curl", "-s", "http://api:5000/api/quotes"])
            )
            
            quotes_output = await test_quotes.stdout()
            print(f"  ✅ Quotes API Check: {quotes_output[:100]}..." if len(quotes_output) > 100 else f"  ✅ Quotes API Check: {quotes_output}")
        except Exception as e:
            print(f"  ❌ Quotes API Check Failed: {str(e)}")
            return False
            
        return True
    
    async def export_containers(self):
        """Export containers to Docker registry if configured"""
        if not self.container_ids:
            print("❌ No containers to export")
            return False
            
        try:
            from export import ContainerExporter
            exporter = ContainerExporter()
            exported = exporter.export_all_containers(self.container_ids)
            print(f"✅ Exported containers: {exported}")
            return True
        except ImportError:
            print("⚠️ Container export module not found. Skipping export.")
            return False
        except Exception as e:
            print(f"❌ Failed to export containers: {str(e)}")
            return False
    
    async def cleanup_containers(self):
        """Clean up containers when shutting down"""
        print("🧹 Cleaning up containers...")
        for service, container_id in self.container_ids.items():
            try:
                container = self.docker_client.containers.get(container_id)
                container.stop()
                container.remove()
                print(f"  ✅ Removed {service} container")
            except Exception as e:
                print(f"  ⚠️ Failed to remove {service} container: {str(e)}")
    
    async def run(self):
        """Run the full orchestration process"""
        print("🚀 Starting Dagger container orchestration...")
        
        try:
            # Initialize client
            await self.initialize_client()
            
            # Set up project directory
            project_dir = await self.setup_project_directory()
            
            # Deploy all services
            await self.deploy_database(project_dir)
            await self.deploy_api(project_dir)
            await self.deploy_frontend(project_dir)
            
            # Perform health checks
            health_checks_passed = await self.perform_health_checks()
            
            if health_checks_passed:
                # Print success message with URLs
                print("\n✅ Application fully operational!")
                print("\n🌐 Access your application at:")
                print(f"  • Frontend: http://localhost:{self.config['frontend']['host_port']}")
                print(f"  • API Health: http://localhost:{self.config['api']['host_port']}/api/health")
                print(f"  • API Quotes: http://localhost:{self.config['api']['host_port']}/api/quotes")
                print(f"  • Database: localhost:{self.config['db']['host_port']} (postgres/postgres)")
                
                print("\n⏱️ Services will remain running. Press Ctrl+C to stop.")
                
                # Keep the services running
                while True:
                    await asyncio.sleep(1)
            else:
                print("\n⚠️ Some health checks failed, but services may still be operational.")
                print("\n🌐 Try accessing your application at:")
                print(f"  • Frontend: http://localhost:{self.config['frontend']['host_port']}")
                print(f"  • API Health: http://localhost:{self.config['api']['host_port']}/api/health")
                print(f"  • API Quotes: http://localhost:{self.config['api']['host_port']}/api/quotes")
                
                print("\n⏱️ Services will remain running. Press Ctrl+C to stop.")
                
                # Keep the services running despite health check failures
                while True:
                    await asyncio.sleep(1)
                
        except Exception as e:
            print(f"\n❌ Error during orchestration: {str(e)}")
            await self.cleanup_containers()
            sys.exit(1)
            
    async def close(self):
        """Close the Dagger client connection and clean up"""
        try:
            await self.cleanup_containers()
        except Exception as e:
            print(f"⚠️ Error during cleanup: {str(e)}")
            
        if self.client:
            await self.client.__aexit__(None, None, None)

async def main():
    parser = argparse.ArgumentParser(description="Dagger Container Orchestrator")
    parser.add_argument("--project-dir", default=".", help="Project directory path")
    args = parser.parse_args()
    
    orchestrator = DaggerOrchestrator(args.project_dir)
    try:
        await orchestrator.run()
    finally:
        await orchestrator.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Shutting down services...")
        sys.exit(0)