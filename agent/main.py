import dagger
import asyncio
import sys
import time
import os
import json
import argparse

class OpenHandsOrchestrator:
    """
    OpenHands AI Orchestrator for deploying and managing containerized applications.
    This class simulates an AI agent running in its own container that can deploy
    and orchestrate a three-tier application across separate containers.
    """
    
    def __init__(self, project_dir="."):
        self.project_dir = project_dir
        self.client = None
        self.db_service = None
        self.api_service = None
        self.frontend_service = None
        self.config = self._load_config()
        
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
                "port": 5432
            },
            "api": {
                "image": "python:3.11-slim",
                "port": 5000
            },
            "frontend": {
                "image": "node:20-alpine",
                "port": 3000
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
    
    async def deploy_database(self, project_dir):
        """Deploy the PostgreSQL database container"""
        print("🛢️ Setting up PostgreSQL database...")
        db_config = self.config["db"]
        
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
            .with_exec(["flask", "run", "--host=0.0.0.0"])
            .as_service()
            .with_exposed_port(api_config["port"])
        )
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
        return self.frontend_service
    
    async def perform_health_checks(self):
        """Perform health checks on all services"""
        print("🔍 Performing health checks...")
        print("  ⏳ Waiting for database to initialize...")
        # Give the database some time to initialize
        time.sleep(5)
        
        # Health check for API
        test_api_health = (
            self.client.container()
            .from_("alpine/curl")
            .with_service_binding("api", self.api_service)
            .with_exec(["curl", "-s", "http://api:5000/api/health"])
        )
        
        try:
            api_health_output = await test_api_health.stdout()
            print(f"  ✅ API Health Check: {api_health_output}")
        except Exception as e:
            print(f"  ❌ API Health Check Failed: {str(e)}")
            return False

        # Health check for quotes endpoint
        test_quotes = (
            self.client.container()
            .from_("alpine/curl")
            .with_service_binding("api", self.api_service)
            .with_exec(["curl", "-s", "http://api:5000/api/quotes"])
        )
        
        try:
            quotes_output = await test_quotes.stdout()
            print(f"  ✅ Quotes API Check: {quotes_output[:100]}..." if len(quotes_output) > 100 else f"  ✅ Quotes API Check: {quotes_output}")
        except Exception as e:
            print(f"  ❌ Quotes API Check Failed: {str(e)}")
            return False
            
        return True
    
    async def run(self):
        """Run the full orchestration process"""
        print("🚀 OpenHands AI starting Dagger orchestration...")
        
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
                print(f"  • Frontend: http://localhost:{self.config['frontend']['port']}")
                print(f"  • API Health: http://localhost:{self.config['api']['port']}/api/health")
                print(f"  • API Quotes: http://localhost:{self.config['api']['port']}/api/quotes")
                
                print("\n⏱️ Services will remain running. Press Ctrl+C to stop.")
                
                # Keep the services running
                while True:
                    await asyncio.sleep(1)
            else:
                print("\n❌ Health checks failed. Please check the logs for more information.")
                sys.exit(1)
                
        except Exception as e:
            print(f"\n❌ Error during orchestration: {str(e)}")
            sys.exit(1)
            
    async def close(self):
        """Close the Dagger client connection"""
        if self.client:
            await self.client.__aexit__(None, None, None)

async def main():
    parser = argparse.ArgumentParser(description="OpenHands AI Container Orchestrator")
    parser.add_argument("--project-dir", default=".", help="Project directory path")
    args = parser.parse_args()
    
    orchestrator = OpenHandsOrchestrator(args.project_dir)
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