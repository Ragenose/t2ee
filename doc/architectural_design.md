# Architectural Design

## Block Diagram

![Block Diagram](images/block_diagram.png?raw=true)

## System Design

The project is running in docker containers except OpenStack controller node and compute node. The reason why using docker container is to build and start the project with one `docker-compose up` command.

### 1. Nginx

The Nginx container is the gateway and reverse proxy of the project. It will redirect HTTP requests toward the two containers: Webpage and RESTful API.

The following is part of the Nginx configuration file for reverse proxy.

```bash
location / {
            proxy_pass  http://webpage:4201;
        }
        location /api {
            proxy_pass  http://api:5000/api;
        }
```

The proxy pass works based on URL. Requests toward `www.example.com/` will be passed to Webpage container and requests toward `www.example.com/api` will be passed to RESTful API container.

The hostnames - webpage and api - are defined in docker compose file for easy container-wise routing.

```yaml
version: '3'
services:
    ...
    api:
        hostname: "api"
    ...
    webpage:
        hostname: "webpage"
    ...
```

