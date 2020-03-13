# Code Quality Review

This document reviews the code quality of this project.

**Table of Contents:**

- [Code Quality Review](#code-quality-review)
  - [Code Formatting](#code-formatting)
  - [Architecture](#architecture)
    - [Backend](#backend)
    - [Front-end](#front-end)
  - [Coding Best Practices](#coding-best-practices)
  - [Non Functional Requirements](#non-functional-requirements)
    - [Maintainability](#maintainability)
      - [Readability](#readability)
      - [Testability](#testability)
      - [Debuggability](#debuggability)
      - [Configurability](#configurability)
    - [Reusability](#reusability)
    - [Reliability](#reliability)
    - [Security](#security)

## Code Formatting

The **Snake Case** is used for both functions and variables in Python codes. The reason why choosing the Snake Case is to match OpenStack SDK's code format.

Examples:

```python
def start_instance(conn, instance_name):
    instance = conn.compute.find_server(instance_name)  
    if(instance.status == "ACTIVE"):
        return True
    else:
        conn.compute.start_server(instance)
    try:
        conn.compute.wait_for_server(instance, status='ACTIVE',wait=10)
    except conn.compute.ResourceTimeout:
        return False
    else:
        return True
```

The **Camel Case** is used in Angular (TypeScript).

Examples:

```typescript
onDeploySubmit() {
    console.log(this.f.image.value);
    // stop here if form is invalid
    if (this.deployForm.invalid) {
      return;
    }
    this.vmService.deployInstance(
      this.f.instance_name.value,
      this.f.root_password.value,
      this.f.image.value,
      this.f.flavor.value
    ).subscribe(
      data=>{
        alert("Successful Deployed");
      }
    )
  }
```

All codes are properly aligned and have proper white space indentation. All codes are able to fit in the standard 14-inch laptop screen without the need of scrolling horizontally and all commented codes are removed.

## Architecture

The design pattern used for both front-end and backend is the **module**. The module pattern is to organize code into components that accomplish a particular function.

### Backend

The backend python codes are split into multiple layers including the custom library of different utilities, configuration files, and testing files.

```.
api/
├── api.Dockerfile
├── callback
│   ├── Image.py
│   ├── __init__.py
│   └── Instance.py
├── callback.Dockerfile
├── config
│   ├── compute.yaml
│   ├── credential.yaml
│   ├── database.yaml
│   └── openstack.yaml
├── CreateDatabase.py
├── lib
│   ├── ConnectionUtilities.py
│   ├── CredentialUtilities.py
│   ├── DatabaseUtilities.py
│   ├── ImageUtilities.py
│   ├── __init__.py
│   ├── InstanceUtilities.py
│   ├── LifecycleUtilities.py
│   ├── SecretUtilities.py
│   └── StatusUtilites.py
├── mq.py
├── requirements.txt
├── run.py
├── start.sh
└── test
    ├── __init__.py
    ├── test_database.py
    ├── test_image.py
    ├── test_instance.py
    ├── test_secret.py
    ├── test_update_user.py
    └── test_user.py
```

In the lib directory, there are modules that handle different tasks for controlling OpenStack.

For example: This `create_instance` function can create the instance based on the parameters and return `None` or an OpenStack Instance object.

```python
def create_instance(conn, image_name, flavor_name, network_name, instance_name, root_password="", keypair=None):
    image = conn.compute.find_image(image_name)
    flavor = conn.compute.find_flavor(flavor_name)
    network = conn.network.find_network(network_name)

    if(keypair is not None):
        instance = conn.compute.create_server(
            name = instance_name, image_id = image.id, flavor_id = flavor.id,
            networks = [{"uuid": network.id}], key_name = keypair)
        conn.compute.wait_for_server(instance, status='ACTIVE', wait=60)
        return instance
    else:
        instance = conn.compute.create_server(
            name = instance_name, image_id = image.id, flavor_id = flavor.id,
            networks = [{"uuid": network.id}])
        return instance
    return None
```

Then the other functions can utilize the modules to control OpenStack to perform certain tasks.

For example: This `mq_create_instance` function will run once there is a create instance message being published and it will use the `create_instance` function to create a instance in OpenStack.

```python
def mq_create_instance(username, instance_name, image, flavor, root_password):
    conn = create_connection_from_config()
    if(check_instance_name_available(conn, instance_name) is True):
        keypair = get_keypair(username)
        instance = create_instance(conn, image, flavor, get_network_name(), instance_name, root_password=root_password, keypair=keypair)
        add_instance_to_user(username, instance_name, instance.id)
        conn.compute.wait_for_server(instance, status='ACTIVE', wait=60)
        # Wait for 30 second to let instance boot up
        time.sleep(30)
        # Try to set the root password if it fails
        for i in range(0,10):
            time.sleep(10)
            try:
                conn.compute.change_server_password(instance, root_password)
            except openstack.exceptions.HttpException:
                continue
            else:
                break
    conn.close()
```

### Front-end

Angular apps are **modular**, the front-end webpage is split into different components that define the screen elements and use services to provide specific functionality not directly related to views.

```.
src
├── app
│   ├── app-routing.module.ts
│   ├── app.component.css
│   ├── app.component.html
│   ├── app.component.spec.ts
│   ├── app.component.ts
│   ├── app.module.ts
│   ├── deploy
│   │   ├── deploy.component.css
│   │   ├── deploy.component.html
│   │   ├── deploy.component.spec.ts
│   │   └── deploy.component.ts
│   ├── helpers
│   │   ├── auth.guard.spec.ts
│   │   ├── auth.guard.ts
│   │   ├── basic-auth.interceptor.ts
│   │   └── error.interceptor.ts
│   ├── home
│   │   ├── home.component.css
│   │   ├── home.component.html
│   │   ├── home.component.spec.ts
│   │   ├── home.component.ts
│   │   ├── home.directive.spec.ts
│   │   ├── home.directive.ts
│   │   └── instance
│   │       ├── image-create.html
│   │       ├── instance.component.css
│   │       ├── instance.component.html
│   │       ├── instance.component.spec.ts
│   │       ├── instance.component.ts
│   │       └── transfer-ownership.html
│   ├── image
│   │   ├── image-item
│   │   │   ├── image-deploy.html
│   │   │   ├── image-item.component.css
│   │   │   ├── image-item.component.html
│   │   │   ├── image-item.component.spec.ts
│   │   │   └── image-item.component.ts
│   │   ├── image.component.css
│   │   ├── image.component.html
│   │   ├── image.component.spec.ts
│   │   ├── image.component.ts
│   │   ├── image.directive.spec.ts
│   │   └── image.directive.ts
│   ├── login
│   │   ├── login.component.css
│   │   ├── login.component.html
│   │   ├── login.component.spec.ts
│   │   └── login.component.ts
│   ├── material.ts
│   ├── models
│   │   ├── instance.ts
│   │   ├── user.spec.ts
│   │   └── user.ts
│   ├── services
│   │   ├── authentication.service.spec.ts
│   │   ├── authentication.service.ts
│   │   ├── image.service.spec.ts
│   │   ├── image.service.ts
│   │   ├── setting.service.spec.ts
│   │   ├── setting.service.ts
│   │   ├── userinfo.service.spec.ts
│   │   ├── userinfo.service.ts
│   │   ├── vm.service.spec.ts
│   │   └── vm.service.ts
│   └── setting
│       ├── setting.component.css
│       ├── setting.component.html
│       ├── setting.component.spec.ts
│       └── setting.component.ts
├── assets
│   └── img
│       └── account_circle-24px.svg
├── environments
│   ├── environment.prod.ts
│   └── environment.ts
├── favicon.ico
├── index.html
├── main.ts
├── polyfills.ts
├── styles.css
└── test.ts
```

## Coding Best Practices

There is no hard coding and all constants like URL, IP addresses are stored in configuration files.

For example: The information needed to connect to OpenStack is stored in `api/config/openstack.yaml`.

```yaml
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

Then the `create_connection_from_config` function can read from the configuration file and create the OpenStack connection.

```python
def create_connection_from_config(file="config/openstack.yaml"):
    opts = options(file)
    return openstack.connection.Connection(
        auth_url = opts.auth_url,
        username = opts.username,
        password = opts.password,
        project_name = opts.project_name,
        region_name = opts.region_name,
        project_domain_name = opts.project_domain_name,
        user_domain_name = opts.user_domain_name,
        identity_api_version = opts.identity_api_version,
        image_api_version = opts.image_api_version
    )
```

There are function comment headers for Python custom library to explain what it does and what are the parameters and return values. However, there are not a lot of in-line comments that explain why I am doing this.

There are not multiple if/else blocks.

The project tries to use as much framework features (both OpenStack SDK and Angular) as possible to avoid writing custom code.

## Non Functional Requirements

### Maintainability

#### Readability

The code is short and uses as much framework features as possible. However, the lack of inline comments may reduce overall readability.

#### Testability

The Python custome library are designed to be testable. The library is written into small functions that aim to accompulish specific tasks and is easy to perform **unit test**. However, the front-end code might not be as testable as the Python code. But it can still be easily tested on components.

#### Debuggability

There is no log used to keep track of any failures happen on runtime. Debugging will rely on error message which is not the best practice.

#### Configurability

The configurable values are stored in separate YAML files or in Docker file which require no change in the code.

### Reusability

The same code is not repeated more than twice. Generic functions and services are reused over different components.

### Reliability

Try and catch code block is used for error handling.

```python
try:
    conn.compute.wait_for_server(instance, status='SHUTOFF',wait=10)
except conn.compute.ResourceTimeout:
    return False
else:
    return True
```

### Security

