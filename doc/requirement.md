# 1. Introduction
A self-service virtual machine deployment platform which is a web portal that utilizes OpenStack API and services

## 1.1. Purpose
The t2ee provides private servers available to students and staff so that students can learn more about Linux and utilize the potential of Linux servers with their project, and professors can create templates to have a different approach to teaching. 

## 1.2. Scope
### 1.2.1. Project Goal
The goal of the project is to create a web portal - a layer above OpenStack - that can utilize OpenStack API to add additional features including user self-service deployment ability, virtual machine ownership, etc.

### 1.2.2. Deliverable
The deliverable of the project will be source code with Dockerfiles and a docker-compose file so that the entire project will be up running within docker by one command:
```bash
docker-compose up
```

### 1.2.3. Features
1. Users should be able to create an account and login with that account.  

2. Users should be able to create virtual machines with only a few steps.

3. Users should be able to manage their own virtual machines and perform tasks including booting, shutting down, rebooting and deleting virtual machines.

4. Users should be able to transfer the ownership of one own virtual machine to another user.
   
5. Users should be able to perform all the above tasks without knowledge of OpenStack.

### 1.2.4. Functionality
1. RESTful API that utilizes OpenStack SDK to control the OpenStack controller node and publishes time-consuming tasks to the message queue.
   
2. Database that stores customized data including user credential, virtual machine ownership, virtual machine specification, etc.
   
3. Message queue that queues time-consuming tasks including virtual machine and image creation.
   
4. Callback program that consumes messages from the message queue and performs tasks.
   
5. The web page that interacts with users, sends HTTP requests to the RESTful API and gathers responses.

6. Nginx HTTP server that reverse proxies HTTP requests from client-side (Browser) toward proper HTTP handler including the web page and RESTful API.
   
7. All the above functionalities should be running in Docker containers.
   
### 1.2.5. Milestones
1. Milestone 1: The OpenStack environment including one controller node and one compute node should be set up and running properly.

2. Milestone 2: The RESTful API should be running and interacting with the OpenStack controller node properly.

3. Milestone 3: The frond end web page should be running and interacting with the RESTful API properly. 

## 1.3. Background
> OpenStack is a cloud operating system that controls large pools of compute, storage, and networking resources throughout a datacenter, all managed and provisioned through APIs with common authentication mechanisms.
>  -- <cite>[OpenStack Org] [1]</cite>

Here are definitions that will be used in this project:
1. Instance: A virtual machine that runs inside OpenStack

2. Image: A single file that containes bootable operating system. An image can be used to create instances with pre-configured options and images can be created from instances.

## 1.4. Rationale

## 1.4. Assumption
This project assumes OpenStack is already set up prior to project deployment and administrator credential, OpenStack API address, default instance deployment information are written in the configuration file of the project.

Here is a sample configuration file:
``` yaml
region_name: RegionOne
auth:
    auth_url: http://t2ee:5000/v3/
    username: admin
    password: t2ee
    project_name: t2ee
    user_domain_name: Default
    project_domain_name: Default
    identity_api_version: 3
    image_api_version: 2
```

And a instance deployment configuration file:
```yaml
image:
  [CentOS7, Ubuntu16.04]

flavor:
  [small, medium, large]

network:
  [provider1]
```

## 1.5. Constraint
Instances are not mapped to DNS records, which means users need to access the virtual machines by IP addresses. This is due to the fact that the project does not have access to campus's DNS server and instances simply get IP address from campus's DHCP server.


[1]: https://www.openstack.org/software/
