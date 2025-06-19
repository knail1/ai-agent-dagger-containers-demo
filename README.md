# OpenHands AI with Dagger.io Container Orchestration Demo

This repository demonstrates how [OpenHands AI](https://github.com/All-Hands-AI/OpenHands) (running in its own Docker container) can use Dagger.io to deploy and orchestrate a three-tier application across separate containers. It showcases Docker-in-Docker capabilities, allowing the OpenHands container to create and manage sub-containers for a complete application stack.

## 🏗️ Architecture

The architecture consists of:

1. **OpenHands AI Container**: The main container that orchestrates everything
2. **Frontend Container**: React application for the user interface
3. **API Container**: Flask middleware for business logic
4. **Database Container**: PostgreSQL for data storage

OpenHands AI uses Dagger.io to build, deploy, and orchestrate these containers, creating a seamless end-to-end application.

For a detailed architecture diagram and explanation, see [Architecture Overview](docs/architecture.md).

## 🚀 Quick Start

### Option 1: Run with OpenHands AI Container (Recommended)

For this demo, we assume you have:
1. Installed Docker on your machine
2. Pulled and run the OpenHands AI container using:
   ```bash
   docker run -p 3000:3000 -v /var/run/docker.sock:/var/run/docker.sock -v $(pwd):/workspace allhandsai/openhands:latest
   ```
3. Accessed the OpenHands web interface at http://localhost:3000
4. In the OpenHands chat interface, asked it to:
   - Clone this repository: `knail1/ai-agent-dagger-containers-demo`
   - Fork it to your own GitHub account
   - Modify it based on your application specifications

Alternatively, you can run the OpenHands AI container directly from this repository:

```bash
# Make the script executable
chmod +x run-openhands.sh

# Run OpenHands AI in a Docker container
./run-openhands.sh
```

This will:
1. Build the OpenHands AI agent Docker image
2. Run the OpenHands AI container with Docker-in-Docker capabilities
3. Deploy and orchestrate the three-tier application

For more details on running OpenHands locally, see the [OpenHands GitHub repository](https://github.com/All-Hands-AI/OpenHands).

### Option 2: Run Directly with Dagger

```bash
# Install Dagger dependencies
pip install -r agent/requirements.txt

# Run the application with Dagger
python agent/main.py
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
./run-openhands.sh
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
./run-openhands.sh
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

## 📂 Repository Structure

```
ai-agent-dagger-containers-demo/
├── .dagger/                # Dagger cache directory
├── agent/                  # OpenHands AI agent code
│   ├── main.py             # Main orchestration script
│   ├── customize.py        # Customization tool
│   ├── config.json         # Configuration file
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile          # Docker image for OpenHands AI
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
│   └── gpt-4.5-research.md # Research notes
├── docker-compose.yml      # Docker Compose configuration
├── run-openhands.sh        # Script to run OpenHands AI container
├── create-spec.py          # Interactive specification generator
├── example-spec.json       # Example specification file
└── README.md               # Documentation
```

## ✅ Verification

After deploying the application:

1. Visit the React frontend at http://localhost:3000
2. Click the "Load Quotes" button to fetch quotes from the database
3. Verify that quotes are displayed on the screen
4. Check the API endpoints directly:
   - API Health Check: http://localhost:5000/api/health
   - API Quotes: http://localhost:5000/api/quotes

## 🔍 How It Works

### OpenHands AI Container

The OpenHands AI container is the main orchestrator. It:

1. Runs in a Docker container with access to the Docker socket
2. Uses Dagger.io to build and deploy the other containers
3. Configures networking between containers
4. Performs health checks to ensure everything is working
5. Provides tools for customizing the application

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

## 📚 Additional Resources

- [OpenHands AI GitHub Repository](https://github.com/All-Hands-AI/OpenHands) - The main OpenHands AI project
- [Dagger.io Documentation](https://docs.dagger.io/) - Learn more about Dagger for container orchestration
- [Docker-in-Docker Guide](https://jpetazzo.github.io/2015/09/03/do-not-use-docker-in-docker-for-ci/) - Understanding Docker-in-Docker concepts
