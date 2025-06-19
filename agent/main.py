import dagger
import asyncio
import sys
import time

async def main():
    print("🚀 Starting Dagger orchestration...")
    
    # Initialize Dagger client
    async with dagger.Connection() as client:
        print("📂 Setting up project directories...")
        project_dir = client.host().directory(".", exclude=[".dagger", "__pycache__", "node_modules", ".git"])

        # Setup PostgreSQL database
        print("🛢️ Setting up PostgreSQL database...")
        db = (
            client.container()
            .from_("postgres:15-alpine")
            .with_env_variable("POSTGRES_PASSWORD", "postgres")
            .with_env_variable("POSTGRES_USER", "postgres")
            .with_env_variable("POSTGRES_DB", "postgres")
            .with_directory("/docker-entrypoint-initdb.d", project_dir.directory("db"))
        )
        db_service = db.as_service().with_exposed_port(5432)

        # Setup Flask API
        print("🐍 Setting up Flask API...")
        api = (
            client.container()
            .from_("python:3.11-slim")
            .with_directory("/app", project_dir.directory("api"))
            .with_workdir("/app")
            .with_exec(["pip", "install", "-r", "requirements.txt"])
        )
        api_service = (
            api.with_service_binding("db", db_service)
            .with_env_variable("FLASK_APP", "app.py")
            .with_exec(["flask", "run", "--host=0.0.0.0"])
            .as_service()
            .with_exposed_port(5000)
        )

        # Setup React frontend
        print("⚛️ Setting up React frontend...")
        frontend = (
            client.container()
            .from_("node:20-alpine")
            .with_directory("/app", project_dir.directory("frontend"))
            .with_workdir("/app")
            .with_exec(["npm", "install"])
            .with_exec(["npm", "run", "build"])
            .with_exec(["npm", "install", "-g", "serve"])
        )
        frontend_service = (
            frontend
            .with_service_binding("api", api_service)
            .with_exec(["serve", "-s", "build", "-l", "3000"])
            .as_service()
            .with_exposed_port(3000)
        )

        # Health check for database
        print("🔍 Performing health checks...")
        print("  ⏳ Waiting for database to initialize...")
        # Give the database some time to initialize
        time.sleep(5)
        
        # Health check for API
        test_api_health = (
            client.container()
            .from_("alpine/curl")
            .with_service_binding("api", api_service)
            .with_exec(["curl", "-s", "http://api:5000/api/health"])
        )
        
        try:
            api_health_output = await test_api_health.stdout()
            print(f"  ✅ API Health Check: {api_health_output}")
        except Exception as e:
            print(f"  ❌ API Health Check Failed: {str(e)}")
            sys.exit(1)

        # Health check for quotes endpoint
        test_quotes = (
            client.container()
            .from_("alpine/curl")
            .with_service_binding("api", api_service)
            .with_exec(["curl", "-s", "http://api:5000/api/quotes"])
        )
        
        try:
            quotes_output = await test_quotes.stdout()
            print(f"  ✅ Quotes API Check: {quotes_output[:100]}..." if len(quotes_output) > 100 else f"  ✅ Quotes API Check: {quotes_output}")
        except Exception as e:
            print(f"  ❌ Quotes API Check Failed: {str(e)}")
            sys.exit(1)

        # Print success message with URLs
        print("\n✅ Application fully operational!")
        print("\n🌐 Access your application at:")
        print("  • Frontend: http://localhost:3000")
        print("  • API Health: http://localhost:5000/api/health")
        print("  • API Quotes: http://localhost:5000/api/quotes")
        
        print("\n⏱️ Services will remain running. Press Ctrl+C to stop.")
        
        # Keep the services running
        while True:
            await asyncio.sleep(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Shutting down services...")
        sys.exit(0)