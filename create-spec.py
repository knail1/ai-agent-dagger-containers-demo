#!/usr/bin/env python3
"""
OpenHands AI Specification Generator

This script helps users create a customization specification for the OpenHands AI agent.
It asks a series of questions and generates a JSON specification file based on the answers.
"""

import json
import os
import sys

def get_input(prompt, default=None):
    """Get input from the user with a default value"""
    if default:
        result = input(f"{prompt} [{default}]: ")
        return result if result else default
    else:
        return input(f"{prompt}: ")

def main():
    print("🚀 OpenHands AI Specification Generator")
    print("--------------------------------------")
    print("This tool will help you create a customization specification for your application.")
    print("Press Enter to accept the default values shown in brackets.\n")
    
    # Application basics
    title = get_input("Enter the application title", "My Custom Quote App")
    button_text = get_input("Enter the button text", "Get Inspirational Quotes")
    
    # New endpoint
    add_endpoint = input("Do you want to add a new API endpoint? (y/n) [n]: ").lower() == 'y'
    new_endpoint = None
    if add_endpoint:
        endpoint_path = get_input("Enter the endpoint path (without /api/)", "status")
        endpoint_name = get_input("Enter the endpoint function name", "get_status")
        endpoint_message = get_input("Enter the endpoint response message", "The system is operational")
        new_endpoint = {
            "path": endpoint_path,
            "name": endpoint_name,
            "message": endpoint_message
        }
    
    # New quotes
    add_quotes = input("Do you want to add new quotes? (y/n) [n]: ").lower() == 'y'
    new_quotes = []
    if add_quotes:
        while True:
            quote_text = get_input("Enter the quote text")
            quote_author = get_input("Enter the quote author")
            new_quotes.append({
                "text": quote_text,
                "author": quote_author
            })
            if input("Add another quote? (y/n) [n]: ").lower() != 'y':
                break
    
    # Container configuration
    print("\nContainer Configuration")
    print("----------------------")
    
    # Database
    db_image = get_input("Enter the database image", "postgres:15-alpine")
    db_port = int(get_input("Enter the database port", "5432"))
    
    # API
    api_image = get_input("Enter the API image", "python:3.11-slim")
    api_port = int(get_input("Enter the API port", "5000"))
    
    # Frontend
    frontend_image = get_input("Enter the frontend image", "node:20-alpine")
    frontend_port = int(get_input("Enter the frontend port", "3000"))
    
    # Create the specification
    spec = {
        "title": title,
        "buttonText": button_text,
        "db": {
            "image": db_image,
            "port": db_port
        },
        "api": {
            "image": api_image,
            "port": api_port
        },
        "frontend": {
            "image": frontend_image,
            "port": frontend_port
        }
    }
    
    if new_endpoint:
        spec["newEndpoint"] = new_endpoint
    
    if new_quotes:
        spec["newQuotes"] = new_quotes
    
    # Save the specification
    filename = get_input("Enter the filename for your specification", "my-spec.json")
    with open(filename, 'w') as f:
        json.dump(spec, f, indent=2)
    
    print(f"\n✅ Specification saved to {filename}")
    print("\nTo use this specification with OpenHands AI, run:")
    print(f"python agent/customize.py --spec {filename}")
    print("./run-openhands.sh")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)