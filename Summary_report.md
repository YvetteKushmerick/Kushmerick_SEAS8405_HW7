deliverables/summary_report.md 

•	Steps taken.

Containers are self-contained applications for developers. Docker is one of a few container infrastructures. It is similar to virtual machines but rather than using a hypervisor, it uses a Docker engine and utilizes significantly less memory space. The files to compose a Docker environment are a Dockerfile, appy.py, docker-compose.yml (or yaml), Makefile.txt and requirement.txt. The app.py is the main Python application file which contains the application logic and functionality. The Dockerfile defines the steps to build a Docker image for the application. The yml or yaml file defines and manages multi-container Docker applications. The Makefile automates common development tasks using make commands. The requirements text file lists the dependencies required by the application. Note that the saved extension needed to be deleted from the Dockerfile before running.

The tools needed to create the Docker containers and test for vulnerabilities are:
    1. Docker Desktop - download 
    2. Command prompt - Windows command prompt 
    3. Create folder with all the above files to create the Docker Platform as a Service container.
    4. Visual Studio Code or other IDE to review the code in the above files. 

After downloading Docker Desktop, use the Windows Command Prompt to compose the Docker container by changing the directory to the folder containing the above files. The command is docker compose up. Docker compose is ideal for defining and managing multi-contain Docker applications. While 'Build' was sufficient for this assignment, in anticipation for future assignments, I opted to get used to docker compose. After running the command, the three options available are v for View in Docker Desktop, o for View Config and w for Enable Watch. v initiates the Docker Desktop then using Docker Scout, run vulnerability scans. Clicking on Before postgres:13 then run scan shows vulnerabilities with four being the most severe:  CVE-2023-24538, CVE-2023-24540, CVE-2024-24790, and CVE-2025-22871. From there, click on recommended fixes. 

Separately, ping to 8.8.8.8 transmitted and received 68 packets before exiting the command. 

•	Vulnerabilities found and fixed.

For the demo, create a separate folder with corrected files. Specifically, the code corrections are:

    1. For app.py, 
        a. Changed hardcoded passwords to environment variable.
        b. Fixed input validation.
        c. Secured calculate route using ast.literal_eval instead of eval. From geeks for geeks, ast.literal_eval() is a function from Python's ast (Abstract Syntax Tree) module. It safely evaluates a string containing a Python literal or a container object. Unlike eval(), it only processes basic literals like strings, numbers, lists, tuples, dictionaries, booleans, and None. It raises an error if the input contains anything beyond these, making it significantly safer.
        d. Bind 127.0.0.1 for localhost instead of all interfaces (0.0.0.0). This restricted port exposure. 

    2.	Dockerfil Hardening:
        a. Used a minimal base image. Added read_only, security_opt, mem_limit, and pids_limit.
        b. Ensure the app runs as a non-root user. Note that root is the default.
        c. Added a HEALTHCHECK directive. - HEALTHCHECK --interval=30s --timeout=10s CMD curl -f http://localhost:5000/ || exit 1
        d. Implement multi-stage builds if possible.
        e. The main difference in fixing vulnerabilities was upgrading 3.9-alpine to 3.13 alpine.

    3.	Other Improvements:
        a. Used .env files for secret handling. Similar to the Dockerfile, saved extensions should be deleted before running. 

A second compose after the vulnerability mitigations were implemented revealed zero vulnerabilities in Docker Scout. 

•	Architecture and how it improves security.
Refer to the Docker network diagram titled Deliverables_architecture_diagram.drawio. The command prompt and Docker Desktop reside at the Docker Client. The Docker Client interacted with the Docker Host via an API. The Docker host hosts the Docker Daemon (client-server architecture). Within the Docker Host are also the containers and images. On the right is the Docker Registry. A Docker pull command from the Client pulls stored images from the Registry to the Docker images under Daemon. Using Docker images, the docker build command, creates the containers. Security is vital to creating the containers to allow tool development. As in any software development environment, access controls and privilege monitoring along with simply using the most up-to-date code are important to the confidentiality, integrity and availability of future tools developed in that environment. An insecure platform injects vulnerabilities before development even starts. 

•	Reflection on lessons learned.
Because my targets nor my teams used Docker containers, this entire exercise was new. Docker containers are powerful tools when developing tools to be reviewed across various people and host systems. Like VMs, malware can also be tested without affecting personal devices. There are concerning default settings, such as root, that would be updated by editing the prerequisite files before creating the infrastructure. 
