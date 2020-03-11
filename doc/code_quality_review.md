# Code Quality Review

This document reviews the code quality of this project.

**Table of Contents:**

- [Code Quality Review](#code-quality-review)
  - [Code Formatting](#code-formatting)

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
