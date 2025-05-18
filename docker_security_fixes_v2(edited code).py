import os
import json
import yaml
import subprocess
from flask import Flask, request, jsonify
import ast
import ipaddress


# Paths to files (adjust as necessary)
DAEMON_JSON_PATH = '/etc/docker/daemon.json'
DOCKERFILE_PATH = 'Dockerfile'
DOCKER_COMPOSE_PATH = 'docker-compose.yml'

# Retrieve password from environment variable instead of hardcoding
PASSWORD = os.environ.get('PASSWORD')
#changed the .env file password function to a complex password. Below is an example. 

#MIN_PASSWORD_LEN = 16 #changed to be more secure
#SPEC_CHARS = {';', ')', '&', '!'}
#NUM_SPECIALS = 2

#def first_password():
#    username = input("Enter a username: ")
 #   password1, password2 = 1,2
#    while(password1 != password2):
#        password1 = getpass.getpass("Enter a password: ")
#        password2 = getpass.getpass("Reenter your password: ")
#        num_of_specials = sum(1 for char in password1 if char in SPEC_CHARS)
#        if (password1 != password2):
#            input("Your passwords do not match. Press Enter to try again")
#        elif (len(password1) < MIN_PASSWORD_LEN):
  #          password1, password2 = 1,2
 #           input(f"Your password must be {MIN_PASSWORD_LEN} characters long. Press Enter to try again")
#        elif (num_of_specials < NUM_SPECIALS):
 #           password1, password2 = 1,2
 #          input(f"Your password must have {NUM_SPECIALS} special characters. Press Enter to try again")

def update_daemon_json():
    """Update or create daemon.json with security settings."""
    settings = {
        "icc": False,
        "userns-remap": "default", #masks existing image and container layers
        "live-restore": True,
        "userland-proxy": False
    }
    if os.path.exists(DAEMON_JSON_PATH):
        with open(DAEMON_JSON_PATH, 'r') as f:
            current_settings = json.load(f)
        current_settings.update(settings)
    else:
        current_settings = settings
    with open(DAEMON_JSON_PATH, 'w') as f:
        json.dump(current_settings, f, indent=4)
    print(f"Updated {DAEMON_JSON_PATH} with security settings.")

def update_dockerfile():
    """Modify Dockerfile to add non-root user and health check."""
    with open(DOCKERFILE_PATH, 'r') as f:
        lines = f.readlines()
    # Insert non-root user and health check if not present
    if not any('RUN adduser -D appuser' in line for line in lines):
        lines.insert(1, 'RUN adduser -D appuser\n')
    if not any('HEALTHCHECK' in line for line in lines):
        lines.insert(-1, 'HEALTHCHECK --interval=30s --timeout=10s CMD curl -f http://localhost:5000/ || exit 1\n')
    if not any('USER appuser' in line for line in lines):
        lines.insert(-1, 'USER appuser\n')
    with open(DOCKERFILE_PATH, 'w') as f:
        f.writelines(lines)
    print(f"Updated {DOCKERFILE_PATH} with non-root user and health check.")

def update_docker_compose():
    """Update docker-compose.yml with security settings for containers."""
    with open(DOCKER_COMPOSE_PATH, 'r') as f:
        compose_data = yaml.safe_load(f)
    for service in compose_data.get('services', {}).values():
        service['mem_limit'] = '512m'
        service['read_only'] = True
        service['security_opt'] = ['no-new-privileges:true']
        service['pids_limit'] = 100
        if 'ports' in service:
            for i, port in enumerate(service['ports']):
                if port.startswith('0.0.0.0'):
                    service['ports'][i] = port.replace('0.0.0.0', '127.0.0.1')
    with open(DOCKER_COMPOSE_PATH, 'w') as f:
        yaml.dump(compose_data, f, default_flow_style=False, sort_keys=False)
    print(f"Updated {DOCKER_COMPOSE_PATH} with security settings.")

def main():
    print("Applying Docker security fixes...")
    update_daemon_json()
    update_dockerfile()
    update_docker_compose()
    print("Security fixes applied. Please review the changes and restart Docker services as necessary.")

# Secure ping route with input validation and no shell=True
@app.route('/ping')
def ping():
    ip = request.args.get('ip')
    try:
        ipaddress.ip_address(ip)  # Validate IP address
        result = subprocess.check_output(["ping", "-c", "1", ip], timeout=3) #added timeout for rate limiting
        return jsonify({"result": result.decode("utf-8")})
    except ValueError:
        return jsonify({"error": "Invalid IP address"}), 400

# Secure calculate route using ast.literal_eval instead of eval
@app.route('/calculate')
def calculate():
    expression = request.args.get('expr')
    try:
        result = ast.literal_eval(expression)
        return str(result)
    except (SyntaxError, ValueError):
        return jsonify({"error": "Invalid expression"}), 400

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)  # Bind to localhost instead of all interfaces
