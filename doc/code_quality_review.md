# Code Quality Review

This document reviews the code quality of this project.

**Table of Contents:**

- [Code Quality Review](#code-quality-review)
  - [Code Formatting](#code-formatting)
  - [Architecture](#architecture)
    - [Backend](#backend)

## Code Formatting

The Snake Case is used for both functions and variables in Python codes. The reason why choosing the Snake Case is to match OpenStack SDK's code format.

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

The Camel Case is used in Angular (TypeScript).

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

The design pattern used for both front-end and backend is module. Module pattern is to organize code into components that accomplish a particular function.

### Backend

The backend python codes are split into multiple layers including custom library of different utilities, configuration files, and testing files.

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

In the lib directory, there are modules that handles different tasks for controlling OpenStack.

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
