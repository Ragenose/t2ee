# 1. Introduction
A self-service virtual machine deployment platform which is a web portal that utilizes OpenStack API and services

## 1.1 Purpose
The t2ee provides private servers available to students and staff so that students can learn more about Linux and utilize the potential of Linux servers with their project, and professors can create templates to have a different approach to teaching. 

## 1.2 Scope
### 1.2.1 Project Goal
The goal of the project is to create a web portal - a layer above OpenStack - that can utilize OpenStack API to add additional features including user self-service deployment ability, virtual machine ownership, etc.

### 1.2.2 Deliverable
The deliverable of the project will be source code with Dockerfiles and a docker-compose file so that the entire project will be up running within docker by one command:
```
docker-compose up
```

### 1.2.3 Features
1. RESTful API that utilizes OpenStack SDK to control the OpenStack controller node and publishes time-consuming tasks to the message queue.
2. Database that stores customized data including user credential, virtual machine ownership, virtual machine specification, etc.
3. Message queue that queues time-consuming tasks including virtual machine and image creation.
4. Callback program that consumes messages from the message queue and performs tasks.