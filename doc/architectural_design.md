# Architectural Design

This document explains the architectural and system design of this project.

**Table of Content:**

- [Architectural Design](#architectural-design)
  - [Block Diagram](#block-diagram)
  - [System Design](#system-design)
    - [1. Nginx](#1-nginx)
    - [2. Webpage](#2-webpage)
    - [3. RESTful API](#3-restful-api)
    - [4. RabbitMQ](#4-rabbitmq)
    - [5. MQ Callback](#5-mq-callback)
    - [6. MongoDB](#6-mongodb)
    - [7. OpenStack](#7-openstack)
    - [8. Apache Guacamole](#8-apache-guacamole)
  
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

The front-end framework used in Webpage container is Angular.

The reason why choosing Angular:

1. Previous experience with AngularJS
2. Component-based
3. Angular Material design
4. Angular CLI
5. Built-in unit test and end-to-end test

### 3. RESTful API

This container utilizes Python Flask to provide RESTful API of controlling OpenStack.

- [API Document](api.md)

### 4. RabbitMQ

There are time-consuming tasks such as creating virtual machines or creating an image from a virtual machine and it is not a good idea to keep the client waiting for the response while the RESTful API is performing those tasks. Instead, there is another container - *MQ Callback* - which is dedicated to performing those time-consuming tasks.

RabbitMQ is the message broker between RESTful API and Callback container. If there is no problem with the request, the RESTful API simply publishes a message to the message queue and responses to the client that *"OK, it is all set"*. Then the Callback container consumes the message and performs the task with whatever the time it needs.

### 5. MQ Callback

This container will connect to the RabbitMQ and start to consume messages. It will perform time-consuming tasks relates to instances and images.

### 6. MongoDB

This container runs MongoDB that contains customized data for this project to provide additional features including virtual machine ownership and customized image information and ownership.

### 7. OpenStack

OpenStack is installed and configured on two physical used PCs. One is the controller node including roles like public-facing API, web interface, scheduler, database, message queue, etc. The other one is the compute node which runs hypervisor and runs actually virtual machines. The project has the configuration file in `/api/config/openstack.yaml` to define the OpenStack controller node's public-facing APIs and authentication. The two python containers - api and callback - use `openstacksdk` package to communicate with OpenStack.

### 8. Apache Guacamole

Apache Guacamole is a clientless remote protocol gateway running on browsers. It was originally designed to open SSH/VNC connection via one button on the instance cards. But due to time constraints, Guacamole will not be integrated into the project instead it will just run as a standalone container to open SSH or VNC connection.
