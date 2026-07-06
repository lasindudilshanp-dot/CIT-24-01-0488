# Docker Notes App
## CCS3308 - Virtualization and Containers | Assignment 1

## Deployment Requirements
- Ubuntu 22.04 or later
- Docker Engine 24.0 or later
- Internet connection (to pull redis:7 image from Docker Hub)

## Application Description
A simple web-based Notes application built with two Docker services:
- Flask (Python web framework) serves the frontend and handles user requests
- Redis (in-memory database) stores the notes persistently

Users can add notes through the web browser. Notes survive container
restarts because Redis data is stored in a named Docker volume.

## Network and Volume Details

### Network
| Name     | Type   | Purpose                                         |
|----------|--------|-------------------------------------------------|
| app-net  | bridge | Allows web and redis containers to communicate  |

### Volume
| Name       | Mount Point | Purpose                         |
|------------|-------------|---------------------------------|
| redis-data | /data       | Persists Redis database to disk |

## Container Configuration

### web (Flask application)
| Property       | Value                       |
|----------------|-----------------------------|
| Image          | my-flask-app (custom built) |
| Port           | 5000:5000                   |
| Network        | app-net                     |
| Restart policy | unless-stopped              |

### redis (Database)
| Property       | Value                       |
|----------------|-----------------------------|
| Image          | redis:7 (Docker Hub)        |
| Port           | 6379 (internal only)        |
| Network        | app-net                     |
| Volume         | redis-data:/data            |
| Restart policy | unless-stopped              |

## Container List
| Container | Role                                         |
|-----------|----------------------------------------------|
| web       | Serves the Notes web app on port 5000        |
| redis     | Stores and retrieves notes data persistently |

## Instructions

### 1. Prepare the application
```bash
./prepare-app.sh
```

### 2. Start the application
```bash
./start-app.sh
```
Then open browser and go to: http://localhost:5000

### 3. Stop the application (data is preserved)
```bash
./stop-app.sh
```

### 4. Remove all resources
```bash
./remove-app.sh
```

## Example Workflow
```bash
# Create application resources
./prepare-app.sh
Preparing app ...

# Run the application
./start-app.sh
Running app ...
The app is available at http://localhost:5000

# Open a web browser and interact with the application

# Pause the application
./stop-app.sh
Stopping app ...

# Delete all application resources
./remove-app.sh
Removed app.
```

## Project File Structure
