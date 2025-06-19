#!/usr/bin/env python3
"""
OpenHands AI Application Customization Tool

This script allows users to customize the application by modifying the code
in the frontend, API, and database components based on their specifications.
"""

import os
import json
import argparse
import sys

def update_frontend(spec):
    """Update the frontend code based on user specifications"""
    print("🔄 Updating frontend based on specifications...")
    
    # Example: Update the title in the React app
    if 'title' in spec:
        app_js_path = os.path.join('frontend', 'src', 'App.js')
        if os.path.exists(app_js_path):
            with open(app_js_path, 'r') as f:
                content = f.read()
            
            # Replace the title in the App.js file
            content = content.replace('<h1>Quote Generator</h1>', f'<h1>{spec["title"]}</h1>')
            
            with open(app_js_path, 'w') as f:
                f.write(content)
            print(f"  ✅ Updated frontend title to: {spec['title']}")
    
    # Example: Update the button text
    if 'buttonText' in spec:
        app_js_path = os.path.join('frontend', 'src', 'App.js')
        if os.path.exists(app_js_path):
            with open(app_js_path, 'r') as f:
                content = f.read()
            
            # Replace the button text in the App.js file
            content = content.replace('Load Quotes', spec['buttonText'])
            
            with open(app_js_path, 'w') as f:
                f.write(content)
            print(f"  ✅ Updated button text to: {spec['buttonText']}")

def update_api(spec):
    """Update the API code based on user specifications"""
    print("🔄 Updating API based on specifications...")
    
    # Example: Add a new endpoint
    if 'newEndpoint' in spec:
        app_py_path = os.path.join('api', 'app.py')
        if os.path.exists(app_py_path):
            with open(app_py_path, 'r') as f:
                content = f.read()
            
            # Add a new endpoint to the Flask app
            new_endpoint = f"""
@app.route('/api/{spec['newEndpoint']['path']}', methods=['GET'])
def {spec['newEndpoint']['name']}():
    return jsonify({{
        'message': '{spec['newEndpoint']['message']}'
    }})
"""
            # Insert the new endpoint before the if __name__ == "__main__" line
            if 'if __name__ == "__main__":' in content:
                content = content.replace('if __name__ == "__main__":', new_endpoint + '\nif __name__ == "__main__":')
                
                with open(app_py_path, 'w') as f:
                    f.write(content)
                print(f"  ✅ Added new endpoint: /api/{spec['newEndpoint']['path']}")

def update_database(spec):
    """Update the database initialization based on user specifications"""
    print("🔄 Updating database based on specifications...")
    
    # Example: Add new quotes to the database
    if 'newQuotes' in spec and isinstance(spec['newQuotes'], list):
        init_sql_path = os.path.join('db', 'init.sql')
        if os.path.exists(init_sql_path):
            with open(init_sql_path, 'r') as f:
                content = f.read()
            
            # Find the last INSERT statement
            last_insert_pos = content.rfind('INSERT INTO')
            if last_insert_pos != -1:
                # Find the end of the last INSERT statement
                end_pos = content.find(';', last_insert_pos)
                if end_pos != -1:
                    # Generate new INSERT statements for the new quotes
                    new_inserts = '\n'
                    for quote in spec['newQuotes']:
                        new_inserts += f"INSERT INTO quotes (text, author) VALUES ('{quote['text']}', '{quote['author']}');\n"
                    
                    # Insert the new statements after the last INSERT statement
                    content = content[:end_pos+1] + new_inserts + content[end_pos+1:]
                    
                    with open(init_sql_path, 'w') as f:
                        f.write(content)
                    print(f"  ✅ Added {len(spec['newQuotes'])} new quotes to the database")

def update_config(spec):
    """Update the configuration based on user specifications"""
    print("🔄 Updating configuration based on specifications...")
    
    config_path = os.path.join('agent', 'config.json')
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        # Update database configuration
        if 'db' in spec:
            for key, value in spec['db'].items():
                if key in config['db']:
                    config['db'][key] = value
        
        # Update API configuration
        if 'api' in spec:
            for key, value in spec['api'].items():
                if key in config['api']:
                    config['api'][key] = value
        
        # Update frontend configuration
        if 'frontend' in spec:
            for key, value in spec['frontend'].items():
                if key in config['frontend']:
                    config['frontend'][key] = value
        
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        print("  ✅ Updated configuration")

def main():
    parser = argparse.ArgumentParser(description='OpenHands AI Application Customization Tool')
    parser.add_argument('--spec', required=True, help='Path to the specification JSON file')
    args = parser.parse_args()
    
    try:
        with open(args.spec, 'r') as f:
            spec = json.load(f)
        
        print("🚀 Starting application customization...")
        
        # Update components based on specifications
        update_frontend(spec)
        update_api(spec)
        update_database(spec)
        update_config(spec)
        
        print("\n✅ Customization completed successfully!")
        print("🔍 Run the OpenHands agent to deploy your customized application:")
        print("   ./run-openhands.sh")
        
    except FileNotFoundError:
        print(f"❌ Error: Specification file '{args.spec}' not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"❌ Error: Invalid JSON in specification file '{args.spec}'.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error during customization: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()