# Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│                     Host Machine / Cloud                        │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                                                         │   │
│  │              OpenHands AI Container                     │   │
│  │                                                         │   │
│  │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │   │
│  │  │             │    │             │    │             │  │   │
│  │  │   Dagger    │    │ Customizer  │    │  Health     │  │   │
│  │  │ Orchestrator│    │    Tool     │    │  Checker    │  │   │
│  │  │             │    │             │    │             │  │   │
│  │  └─────────────┘    └─────────────┘    └─────────────┘  │   │
│  │                                                         │   │
│  └──────────────┬──────────────┬──────────────┬────────────┘   │
│                 │              │              │                │
│                 ▼              ▼              ▼                │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │                 │  │                 │  │                 │ │
│  │     React       │  │     Flask       │  │   PostgreSQL    │ │
│  │    Frontend     │◄─┼─►     API       │◄─┼─►   Database    │ │
│  │    Container    │  │    Container    │  │    Container    │ │
│  │                 │  │                 │  │                 │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow

1. **User Interaction**:
   - User interacts with the React frontend
   - Frontend makes API requests to the Flask backend

2. **API Processing**:
   - Flask API receives requests
   - API queries the PostgreSQL database
   - API processes data and returns responses

3. **Data Storage**:
   - PostgreSQL stores application data
   - Database is initialized with sample data

## Container Orchestration

The OpenHands AI container orchestrates the entire system:

1. **Deployment**:
   - Builds and deploys all containers
   - Sets up networking between containers
   - Configures environment variables

2. **Monitoring**:
   - Performs health checks
   - Monitors container status
   - Reports issues

3. **Customization**:
   - Allows users to customize the application
   - Updates configuration based on specifications
   - Rebuilds containers as needed

## Technology Stack

- **OpenHands AI**: Python-based orchestration with Docker-in-Docker
- **Dagger.io**: Container orchestration and pipeline automation
- **React**: Frontend user interface
- **Flask**: API middleware
- **PostgreSQL**: Database backend
- **Docker**: Containerization platform