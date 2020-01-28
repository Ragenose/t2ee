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
1. Users should be able to create an account and login with that account.  

2. Users should be able to create virtual machines with only a few steps.

3. Users should be able to manage their own virtual machines and perform tasks including booting, shutting down, rebooting and deleting virtual machines.

4. Users should be able to transfer the ownership of one own virtual machine to another user.
   
5. Users should be able to perform all the above tasks without knowledge of OpenStack.

### 1.2.4 Functionality
1. RESTful API that utilizes OpenStack SDK to control the OpenStack controller node and publishes time-consuming tasks to the message queue.
   
2. Database that stores customized data including user credential, virtual machine ownership, virtual machine specification, etc.
   
3. Message queue that queues time-consuming tasks including virtual machine and image creation.
   
4. Callback program that consumes messages from the message queue and performs tasks.
   
5. The web page that interacts with users, sends HTTP requests to the RESTful API and gathers responses.

6. Nginx HTTP server that reverse proxies HTTP requests from client-side (Browser) toward proper HTTP handler including the web page and RESTful API.
   
7. All the above functionalities should be running in Docker containers.
   
### 1.2.5 Milestones
1. Milestone 1: The OpenStack environment including one controller node and one compute node should be set up and running properly.

2. Milestone 2: The RESTful API should be running and interacting with the OpenStack controller node properly.

3. Milestone 3: The frond end web page should be running and interacting with the RESTful API properly. 