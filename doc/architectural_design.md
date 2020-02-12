# Architectural Design

This document is to explain the architectural and system design of this project.

**Table of Content:**

- [Architectural Design](#architectural-design)
  - [Block Diagram](#block-diagram)
  - [System Design](#system-design)
    - [1. Nginx](#1-nginx)
    - [2. Webpage](#2-webpage)
    - [3. RESTful API](#3-restful-api)
    - [4. RabbitMQ](#4-rabbitmq)
  
## Block Diagram

![Block Diagram](images/block_diagram.png?raw=true)

## System Design

The project is running in docker containers except for the OpenStack controller node and compute node. The reason why using Docker containers is to build and start the project with one `docker-compose up` command.

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

The proxy pass works based on the URL. Requests toward `www.example.com/` will be passed to Webpage container and requests toward `www.example.com/api` will be passed to the RESTful API container.

The hostnames - *webpage* and *api* - are defined in Docker compose file for easy container-wise routing.

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

Nginx can also prevent *Cross-origin resource sharing (CORS)* which is requesting restricted resources from another domain. All requests on the web page are in the same domain and passed by Nginx since it is the gateway. CORS is not necessarily an issue but requires extra effort to enable cross-origin requests.

### 2. Webpage

The fron-end framework used in Webpage container is Angular.

The reason why choosing Angular:

1. Previous experience with AngularJS
2. Component based
3. Angular Material design
4. Angular CLI
5. Built-in unit test and end-to-end test

### 3. RESTful API

This container utilizes Python Flask to provide RESTful API of controlling OpenStack.

- [API Document](api.md)

### 4. RabbitMQ

