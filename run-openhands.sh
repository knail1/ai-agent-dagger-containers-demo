#!/bin/bash

# Build the OpenHands agent Docker image
docker build -t openhands-agent ./agent

# Run the OpenHands agent in a Docker container with Docker socket mounted
# This allows Docker-in-Docker operation for container orchestration
docker run -it --rm \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v $(pwd):/app/project \
  -w /app/project \
  -p 3000:3000 \
  -p 5000:5000 \
  openhands-agent --project-dir /app/project