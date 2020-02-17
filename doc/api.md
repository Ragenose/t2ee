# RESTful API Document

Document of RESTful API call.

**Table of Content:**
- [RESTful API Document](#restful-api-document)
  - [User related](#user-related)
    - [Create User](#create-user)
    - [User Login](#user-login)
    - [Update User Password](#update-user-password)
    - [Update User Key Pair](#update-user-key-pair)
  - [Instance related](#instance-related)
    - [Create Instance](#create-instance)
    - [Delete Instance](#delete-instance)
    - [Change Instance Lifecycle](#change-instance-lifecycle)

## User related

### Create User

Used for user signup.

* **URL**

    `/api/user/create`

* **Method:**

  `POST`

* **Header Params**

    None

* **URL Params**

   None

* **Data Params**

  ```json
  {
    username: "example_username",
    password: "example_password",
    email: "example_email"
  }
  ```

* **Success Response:**

  * **Code:** 200 \
    **Content:**

    ```json
    { username : "example_username" }
    ```

* **Error Response:**

    If the request lacks certain data.

  * **Code:** 400 Bad Request\
    **Content:** `Bad Request`

  OR

    The data format is correct, but it cannot create the account due to duplicated username.

  * **Code:** 403 Forbidden\
    **Content:** `Creating failed`

* **Notes:**

  The password should be hashed from the front-end.

---

### User Login

Used for user login authentication

* **URL**

  `/api/user/login`

* **Method:**

  `POST`

* **Header Params**

    `Authorization: Basic <credentials>`

* **URL Params**

   None

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200\
    **Content:** 
    ```json
    { username : "example_username }
    ```

* **Error Response:**

  When authentication failed.

  * **Code:** 401 UNAUTHORIZED\
    **Content:** `Invalid Credential`

---

### Update User Password

Update the user's password

* **URL**

  `/api/user/update/password`

* **Method:**

  `POST`

* **Header Params**

    `Authorization: Basic <credentials>`

* **URL Params**

   None

* **Data Params**

  ```json
  {
    password: "example_password"
  }
  ```

* **Success Response:**

  * **Code:** 200\
    **Content:** 
    ```json
    { status : "OK" }
    ```

* **Error Response:**
* 
  When authentication failed.

  * **Code:** 401 UNAUTHORIZED\
    **Content:** `Invalid Credential`
    
  When password data has the wrong type

  * **Code:** 400 BAD REQUEST\
    **Content:** `Bad Request, insufficient data`
  
  When update password failed
  
  * **Code:** 400 BAD REQUEST\
    **Content:** `Update password failed`

---

### Update User Key Pair

Update the user's key pair

* **URL**

  `/api/user/keypair/update`

* **Method:**

  `POST`

* **Header Params**

    `Authorization: Basic <credentials>`

* **URL Params**

   None

* **Data Params**

  ```json
  {
    pubkey: "example_pubkey"
  }
  ```

* **Success Response:**

  * **Code:** 200\
    **Content:** 
    ```json
    { status : "OK" }
    ```

* **Error Response:**
* 
  When authentication failed.

  * **Code:** 401 UNAUTHORIZED\
    **Content:** `Invalid Credential`
    
  When password data has the wrong type

  * **Code:** 400 BAD REQUEST\
    **Content:** `Bad Request, insufficient data`

## Instance related

### Create Instance

Deploy an Instance

* **URL**

  `/api/instance/create`

* **Method:**

  `POST`

* **Header Params**

    `Authorization: Basic <credentials>`

* **URL Params**

   None

* **Data Params**

  ```json
  {
    flavor: "example_flavor",
    instance_name: "example_instance_name",
    image: "example_image",
    root_password: "example_root_password"
  }
  ```

* **Success Response:**

  * **Code:** 200\
    **Content:** 
    ```json
    { status : "OK" }
    ```

* **Error Response:**
* 
  When authentication failed.

  * **Code:** 401 UNAUTHORIZED\
    **Content:** `Invalid Credential`
    
  When insufficient data provided

  * **Code:** 400 BAD REQUEST\
    **Content:** `Bad Request, insufficient data`

---

### Delete Instance

Delete an Instance

* **URL**

  `/api/instance/delete/<instance_name>`

* **Method:**

  `DELETE`

* **Header Params**

    `Authorization: Basic <credentials>`

* **URL Params**

   None

* **Data Params**

None

* **Success Response:**

  * **Code:** 200\
    **Content:** 
    ```json
    { status : "OK" }
    ```

* **Error Response:**
* 
  When authentication failed.

  * **Code:** 401 UNAUTHORIZED\
    **Content:** `Invalid Credential`

---

### Change Instance Lifecycle

Change instance lifecycle (start/shutdown/reboot)

* **URL**

  `/api/instance/lifecycle/<type>/<instance_name>`

* **Method:**

  `POST`

* **Header Params**

    `Authorization: Basic <credentials>`

* **URL Params**

   None

* **Data Params**

    None

* **Success Response:**

  * **Code:** 200\
    **Content:** 
    ```json
    { status : "OK" }
    ```

* **Error Response:**
* 
  When authentication failed.

  * **Code:** 401 UNAUTHORIZED\
    **Content:** `Invalid Credential`
    
  When invalid type on the URL

  * **Code:** 400 UNAUTHORIZED\
    **Content:** `Invalid operation`

  When operation failed

  * **Code:** 400 BAD REQUEST\
    **Content:** `Failed`

---