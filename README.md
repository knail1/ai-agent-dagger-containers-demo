# Dagger.io Container Orchestration Demo

This repository demonstrates how to use Dagger.io to deploy and orchestrate a three-tier application across separate containers. It showcases Docker-in-Docker capabilities, allowing a container to create and manage sub-containers for a complete application stack.

## 🏗️ Architecture

The architecture consists of:

1. **Orchestrator Container**: The main container that orchestrates everything using Dagger
2. **Frontend Container**: React application for the user interface
3. **API Container**: Flask middleware for business logic
4. **Database Container**: PostgreSQL for data storage

The Dagger orchestrator builds, deploys, and orchestrates these containers, creating a seamless end-to-end application.

For a detailed architecture diagram and explanation, see [Architecture Overview](docs/architecture.md).

## 🚀 Quick Start

### Prerequisites

For this demo, you need:
1. Docker installed on your machine
2. Docker socket accessible for Docker-in-Docker operations
3. Python 3.9+ for running the orchestrator

### Option 1: Run with Execute Script (Recommended)

```bash
# Clone the repository
git clone https://github.com/knail1/ai-agent-dagger-containers-demo.git
cd ai-agent-dagger-containers-demo

# Make the script executable
chmod +x execute.py

# Run the orchestration script
./execute.py
```

This will:
1. Install required dependencies
2. Set up Docker networking
3. Deploy and orchestrate the three-tier application
4. Perform health checks to ensure everything is working

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

You can customize the application by modifying the configuration files:

### Option 1: Edit Configuration Files Directly

```bash
# Edit the main configuration file
nano agent/config.json

# Edit Docker Compose configuration
nano docker-compose.yml
```

### Option 2: Use the Customization Tool

```bash
# Create your specification file (use example-spec.json as a template)
cp example-spec.json my-spec.json

# Edit the specification file
nano my-spec.json

# Run the customization tool
python agent/customize.py --spec my-spec.json

# Deploy your customized application
./execute.py
```

## 🔄 Interaction Flow

1. User clones this repository
2. User runs the execute.py script
3. The Dagger orchestrator uses Docker-in-Docker to create sub-containers for each tier of the application
4. The orchestrator deploys the code in these containerized environments
5. User interacts with the application through the React frontend
6. React frontend makes requests to the Flask API
7. Flask API queries the PostgreSQL database
8. Data flows back to the user through the same path

### Docker-in-Docker Workflow

The key feature of this demo is the Docker-in-Docker capability:

1. The Dagger orchestrator runs with access to the host's Docker socket
2. It creates and manages three sub-containers:
   - Frontend container (React)
   - API container (Flask)
   - Database container (PostgreSQL)
3. These containers communicate with each other through a Docker network
4. The orchestrator can modify code in these containers and rebuild them as needed
5. All of this happens within a single execution environment

## 🛠 Technologies Demonstrated

- **Docker-in-Docker**: Using Docker socket to create and manage containers from within a container
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
├── execute.py              # Entry point script
├── .env.example            # Example environment variables
├── create-spec.py          # Interactive specification generator
├── example-spec.json       # Example specification file
└── README.md               # Documentation
```

## ✅ Verification

After deploying the application:

1. Visit the React frontend at http://localhost:3001
2. Click the "Load Quotes" button to fetch quotes from the database
3. Verify that quotes are displayed on the screen
4. Check the API endpoints directly:
   - API Health Check: http://localhost:5000/api/health
   - API Quotes: http://localhost:5000/api/quotes
   
Note: The frontend port has been changed to 3001 to avoid conflicts with other services.

## 🔍 How It Works

### Dagger Orchestrator

The Dagger orchestrator is the main component that:

1. Runs with access to the Docker socket
2. Uses Dagger.io to build and deploy the other containers
3. Configures networking between containers
4. Performs health checks to ensure everything is working
5. Provides tools for customizing the application
6. Supports exporting containers to Docker registries

### Docker-in-Docker Implementation

The Docker-in-Docker implementation is achieved by:

1. Accessing the host's Docker socket (`/var/run/docker.sock`)
2. Using the Docker API to create and manage sub-containers
3. Creating a Docker network for inter-container communication
4. Using volume mounts to share code between containers
5. Managing container lifecycle (create, start, stop, remove)
6. Implementing proper cleanup procedures

### Container Communication

- Frontend container communicates with API container
- API container communicates with Database container
- All containers are connected through a dedicated Docker network
- Persistent volume for database storage

This demonstrates a practical example of how Dagger can deploy and manage containerized applications.

## 📚 Additional Resources

- [Dagger.io Documentation](https://docs.dagger.io/) - Learn more about Dagger for container orchestration
- [Docker-in-Docker Guide](https://jpetazzo.github.io/2015/09/03/do-not-use-docker-in-docker-for-ci/) - Understanding Docker-in-Docker concepts
- [Docker Compose Documentation](https://docs.docker.com/compose/) - Learn more about Docker Compose
- [Docker Registry Documentation](https://docs.docker.com/registry/) - Learn about Docker registries for container export

## 🔐 Environment Variables

The application uses the following environment variables, which can be set in a `.env` file:

```
# Docker Registry Configuration
REGISTRY_URL=your-registry-url
REGISTRY_USERNAME=your-username
REGISTRY_PASSWORD=your-password

# Database Configuration
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=quotes
DATABASE_URL=postgresql://postgres:postgres@db:5432/quotes

# Network Configuration
DOCKER_NETWORK=app-network
```

See `.env.example` for a template.
