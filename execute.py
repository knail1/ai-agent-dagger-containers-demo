#!/usr/bin/env python3
"""
Entry point script for OpenHands to execute the three-tier application setup.
This script should be run from within the OpenHands container.
"""

import subprocess
import sys
import os
import time

def main():
    """Execute the three-tier application setup within OpenHands environment"""
    print("🚀 Starting three-tier application deployment from OpenHands...")
    
    # Verify Docker access
    try:
        subprocess.run(["docker", "version"], check=True, capture_output=True)
        print("✅ Docker access verified")
    except subprocess.CalledProcessError:
        print("❌ Docker access failed. Check Docker-in-Docker configuration.")
        sys.exit(1)
    
    # Install dependencies
    print("📦 Installing Python dependencies...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "agent/requirements.txt"], check=True)
    
    # Execute main orchestration
    print("🔧 Starting container orchestration...")
    os.chdir("agent")
    subprocess.run([sys.executable, "main.py"], check=True)

if __name__ == "__main__":
    main()