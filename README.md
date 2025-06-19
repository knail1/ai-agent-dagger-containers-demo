# OpenHands AI with Dagger.io Container Orchestration Demo

This repository demonstrates how OpenHands AI (running in its own Docker container) can use Dagger.io to deploy and orchestrate a three-tier application across separate containers.

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
4. OpenHands deploys the code in containerized environments
5. User interacts with the application through the React frontend
6. React frontend makes requests to the Flask API
7. Flask API queries the PostgreSQL database
8. Data flows back to the user through the same path

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

### Container Communication

- Frontend container communicates with API container
- API container communicates with Database container
- All orchestrated by the OpenHands AI container

This demonstrates a practical example of how OpenHands AI can deploy and manage containerized applications.
