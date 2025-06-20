# Dagger.io Container Orchestration Demo

This repository demonstrates how [OpenHands AI](https://github.com/All-Hands-AI/OpenHands) (running in its own Docker container) can use Dagger.io to deploy and orchestrate a three-tier application across separate containers. It showcases Docker-in-Docker capabilities, allowing the OpenHands container to create and manage sub-containers for a complete application stack.

## 🏗️ Architecture

The architecture consists of:

1. **OpenHands AI Container**: The main container that orchestrates everything
2. **Frontend Container**: React application for the user interface  
3. **API Container**: Flask middleware for business logic
4. **Database Container**: PostgreSQL for data storage

OpenHands AI uses Dagger.io to build, deploy, and orchestrate these containers, creating a seamless end-to-end application.

For a detailed architecture diagram and explanation, see [Architecture Overview](docs/architecture.md).

## 🚀 Getting Started

### Prerequisites

For this demo, you need:

1. **Docker Installation**: Install Docker Desktop or Docker Engine with the following settings for Docker-in-Docker support:

   **Docker Desktop Settings (Required for Docker-in-Docker)**:
   - Enable "Use Docker Compose V2"
   - Enable "Use containerd for pulling and storing images"
   - In "Resources" → "Advanced": Allocate at least 4GB RAM and 2 CPUs
   - Enable "Experimental Features" if available

   **Linux Docker Engine Additional Setup**:
   ```bash
   # Add your user to docker group
   sudo usermod -aG docker $USER

   # Enable Docker socket with proper permissions
   sudo chmod 666 /var/run/docker.sock

   # For Docker-in-Docker support
   sudo sysctl -w kernel.security.apparmor.restrict_unprivileged_userns=0
   ```

2. **OpenHands Container**: Pull the OpenHands container before proceeding:
   ```bash
   # Pull the latest OpenHands container
   docker pull allhandsai/openhands:latest
   ```

3. **Claude API Key**: 
   - Sign up for an Anthropic account at https://console.anthropic.com
   - Generate an API key
   - Keep the key available for OpenHands configuration

4. **Docker Registry Access (Optional)**: For container export functionality:
   - Docker Hub account OR
   - AWS ECR access OR  
   - Private registry credentials

### Docker-in-Docker Configuration

This application requires OpenHands to create and manage sub-containers. Ensure your Docker setup supports this:

**Docker Desktop Users:**
1. Go to Settings → General
2. Enable "Use Docker Compose V2"
3. Go to Settings → Resources → Advanced
4. Allocate minimum 4GB RAM, 2 CPUs
5. Apply & Restart

**Linux Users:**
```bash
# Enable Docker socket access
sudo chmod 666 /var/run/docker.sock

# Configure AppArmor for container nesting (Ubuntu/Debian)
sudo sysctl -w kernel.security.apparmor.restrict_unprivileged_userns=0

# Make permanent
echo 'kernel.security.apparmor.restrict_unprivileged_userns=0' | sudo tee -a /etc/sysctl.conf
```

**Verification:**
Test Docker-in-Docker capability:
```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock docker:latest docker ps
```

### Option 1: Run with OpenHands AI Container (Recommended)

**Start OpenHands with Proper Privileges:**
```bash
# Run OpenHands with Docker-in-Docker support
docker run -it --rm \
  --privileged \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v $(pwd):/workspace \
  -w /workspace \
  -p 3000:3000 \
  -e ANTHROPIC_API_KEY=your_claude_api_key_here \
  allhandsai/openhands:latest
```

**Execute from OpenHands:**
Once inside OpenHands interface (http://localhost:3000), run:
```bash
# Clone and execute this repository
git clone https://github.com/knail1/ai-agent-dagger-containers-demo.git
cd ai-agent-dagger-containers-demo
python execute.py
```

This will:
1. Verify Docker access and install dependencies
2. Run the Dagger orchestrator with Docker-in-Docker capabilities
3. Deploy and orchestrate the three-tier application
4. Perform health checks to ensure everything is working

For more details on running OpenHands locally, see the [OpenHands GitHub repository](https://github.com/All-Hands-AI/OpenHands).

### Option 2: Run Directly with Dagger

```bash
# Install Dagger dependencies
pip install -r agent/requirements.txt

# Run the application with Dagger
cd agent
python main.py
```

### Option 3: Run with Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f
```

## 🔧 Customizing Your Application

You can customize the application using the interactive specification generator:

```bash
# Run the interactive specification generator
python create-spec.py

# Run the customization tool with your generated specification
python agent/customize.py --spec my-spec.json

# Deploy your customized application
python execute.py
```

Alternatively, you can manually create a specification file:

```bash
# Create your specification file (use example-spec.json as a template)
cp example-spec.json my-spec.json

# Edit the specification file
nano my-spec.json

# Run the customization tool
python agent/customize.py --spec my-spec.json

# Deploy your customized application
python execute.py
```

## 🔄 Interaction Flow

1. User forks this repository
2. User pulls it into their OpenHands Docker instance
3. User asks OpenHands to modify it based on their application specification
4. OpenHands uses Docker-in-Docker to create sub-containers for each tier of the application
5. OpenHands deploys the code in these containerized environments
6. User interacts with the application through the React frontend
7. React frontend makes requests to the Flask API
8. Flask API queries the PostgreSQL database
9. Data flows back to the user through the same path

### Docker-in-Docker Workflow

The key feature of this demo is the Docker-in-Docker capability:

1. The OpenHands AI container runs with access to the host's Docker socket
2. OpenHands creates and manages three sub-containers:
   - Frontend container (React)
   - API container (Flask)
   - Database container (PostgreSQL)
3. These containers communicate with each other through a Docker network
4. OpenHands can modify code in these containers and rebuild them as needed
5. All of this happens without leaving the OpenHands container environment

## 🛠 Technologies Demonstrated

- **Docker-in-Docker**: OpenHands AI runs in a Docker container that orchestrates other containers
- **Dagger.io**: Used for container orchestration and pipeline automation
- **React**: Frontend user interface
- **Flask**: API middleware
- **PostgreSQL**: Database backend
- **Configuration Management**: Dynamic configuration through JSON files
- **Container Export**: Functionality to export containers to Docker registries

## 📂 Repository Structure

```
ai-agent-dagger-containers-demo/
├── .dagger/                # Dagger cache directory
├── agent/                  # Dagger orchestrator code
│   ├── main.py             # Main orchestration script
│   ├── customize.py        # Customization tool
│   ├── config.json         # Configuration file
│   ├── export.py           # Container export functionality
│   └── requirements.txt    # Python dependencies
├── frontend/               # React frontend application
│   ├── src/                # React source code
│   ├── public/             # Static assets
│   ├── package.json        # Node.js dependencies
│   └── Dockerfile          # Docker image for frontend
├── api/                    # Flask API middleware
│   ├── app.py              # Flask application
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile          # Docker image for API
├── db/                     # PostgreSQL database
│   └── init.sql            # Database initialization script
├── docs/                   # Documentation
│   ├── architecture.md     # Architecture diagram and explanation
│   └── fixes.md            # Implementation notes
├── docker-compose.yml      # Docker Compose configuration
├── execute.py              # Entry point script for OpenHands
├── .env.example            # Example environment variables
├── create-spec.py          # Interactive specification generator
├── example-spec.json       # Example specification file
└── README.md               # Documentation
```

## ✅ Testing Your Application

After deploying the application:

- **Frontend**: http://localhost:3001
- **API Health Check**: http://localhost:5000/api/health
- **API Quotes**: http://localhost:5000/api/quotes
- **Database**: localhost:5432 (postgres/postgres)

Click the "Load Quotes" button in the frontend to fetch quotes from the database and verify that quotes are displayed on the screen.

Note: The frontend runs on port 3001 to avoid conflicts with OpenHands running on port 3000.

## 📦 Container Export to Docker Registry

After successfully deploying your application, you can export the containers to a Docker registry:

### Export to Docker Hub
```bash
# From within the OpenHands container
cd agent
python -c "
from export import ContainerExporter
exporter = ContainerExporter()
# Get running container IDs
import docker
client = docker.from_env()
containers = {c.name: c.id for c in client.containers.list() if 'demo' in c.name}
exported = exporter.export_all_containers(containers)
print('Exported containers:', exported)
"
```

### Export to AWS ECR
```bash
# Configure AWS credentials in OpenHands container
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export AWS_DEFAULT_REGION=us-east-1

# Login to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin your_account.dkr.ecr.us-east-1.amazonaws.com

# Export containers
python -c "
from export import ContainerExporter
import json

# Update config for ECR
config = json.load(open('config.json'))
config['registry']['default_registry'] = 'your_account.dkr.ecr.us-east-1.amazonaws.com'
json.dump(config, open('config.json', 'w'), indent=2)

# Export
exporter = ContainerExporter()
# ... export logic
"
```

### Export to Private Registry
```bash
# Login to your private registry
docker login your-registry.com

# Update config.json with your registry details
# Export using the same pattern as above
```

### Exported Container Usage
```bash
# Pull and run exported containers on any Docker host
docker pull your-registry/demo-frontend:latest
docker pull your-registry/demo-api:latest  
docker pull your-registry/demo-db:latest

# Run with docker-compose
# (Use the exported image names in docker-compose.yml)
```

## 🔍 How It Works

### The Orchestrator

The Dagger orchestrator is the main component that:

1. Runs with access to the Docker socket
2. Uses Dagger.io to build and deploy the other containers
3. Configures networking between containers
4. Performs health checks to ensure everything is working
5. Provides tools for customizing the application
6. Supports exporting containers to Docker registries

### Docker-in-Docker Implementation

The Docker-in-Docker implementation is achieved by:

1. Mounting the host's Docker socket (`/var/run/docker.sock`) into the OpenHands container
2. Using the Docker API from within the OpenHands container to create and manage sub-containers
3. Creating a Docker network for inter-container communication
4. Using volume mounts to share code between the OpenHands container and sub-containers
5. Managing container lifecycle (create, start, stop, remove) from within OpenHands

### Container Communication

- Frontend container communicates with API container
- API container communicates with Database container
- All orchestrated by the OpenHands AI container

This demonstrates a practical example of how OpenHands AI can deploy and manage containerized applications.

## 🧹 Cleanup

When you're done with the application, you can clean up all resources:

```bash
# Stop and remove all containers
docker-compose down

# Remove the Docker network
docker network rm app-network

# Remove any dangling volumes
docker volume prune -f
```

## 📚 Additional Resources

- [OpenHands AI GitHub Repository](https://github.com/All-Hands-AI/OpenHands) - The main OpenHands AI project
- [Dagger.io Documentation](https://docs.dagger.io/) - Learn more about Dagger for container orchestration
- [Docker-in-Docker Guide](https://jpetazzo.github.io/2015/09/03/do-not-use-docker-in-docker-for-ci/) - Understanding Docker-in-Docker concepts
- [Docker Registry Documentation](https://docs.docker.com/registry/) - Learn about Docker registries for container export
