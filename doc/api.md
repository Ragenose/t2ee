# RESTful API Document

Document of RESTful API call.

**Table of Content:**
- [RESTful API Document](#restful-api-document)
  - [User related](#user-related)
    - [Create User](#create-user)
    - [User login](#user-login)

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
  
### User login

Used for user login authentication

* **URL**

  `/api/user/login`

* **Method:**
  
  <_The request type_>

  `POST`

* **Header Params**

    `Authorization: Basic <credentials>`

* **URL Params**

   None

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200\
    **Content:** `{ username : "example_username }`

* **Error Response:**

  When authentication failed.

  * **Code:** 401 UNAUTHORIZED\
    **Content:** `Invalid Credential`
