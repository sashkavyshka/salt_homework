# Homework for Salt Security

THis is a homework for Salt Security.
This is a test that:
1. Spins up an echo server
2. Tests sending GET requests to the server and validating the status code of the
response
3. Tests shutting down the echo server
4. Tests sending GET requests to the server and validating that no response was
received

## How to run on GitHub Actions

If you're using GitHub Actions, Server job and Pytest Job run in parallel, and Pytest job is waiting for 60 sec to test that the server is down.

## How to run locally

To run the server locally you need to run the server.py file

### Run the server.py
Change to the repository directory
```bash
$ cd test-server
```

Install dependencies
```bash
$ pip install -r requirements.txt
```

Run server.py
```bash
$ python server.py
```
The server will be available at `http://localhost:8000` for 1 minute, then it closes automatically. 

 # Server structure
 The server is written using sanic package, and can get and return simple data objects using the object id or it can return the whole list of objects. You can aalso post a new object to it.
 
 # API Reference

 ## Authentication
 You must authenticate with the API to gain access first.
 The following endpoint will return an access token which should be added to the `Authorization` header

 Username and password are "test" and "1234"

 | Endpoint  | Method | Params                                                             | Response                                                           | Example |
|-----------|--------|--------------------------------------------------------------------|--------------------------------------------------------------------|---------|
| /api/auth | POST   | Json Body: ``` {   "username": "test",   "password": "1234" }  ``` |  ``` { "access_token":"ververylongstringwithnumbersandstuff" } ``` |         |


 ### *All endpoints require the following headers*
 ```
 "Content-Type": "application/json"
 "Authorization": "Bearer {your_token_here}"
 ```

## Endpoints

| Endpoint              | Method | Params                                                                                                                 | Returns            | Example |
|-----------------------|--------|------------------------------------------------------------------------------------------------------------------------|--------------------|---------|
| /api/data             | GET    |                                                                                                                        | List of Data   |         |
| /api/data             | POST   | json body: ```json {   "data": [     {       "key": "key1",       "val": "val1",       "valType": "str"     }   ] }``` | The created object |         |
| /api/data/<object_id> | GET    | object_id: int - Representing the object id                                                                            | Data           |         |
| /api/data/<object_id> | DELETE | object_id: int - Representing the object id  to delete                                                                 | `204` Empty Response |         |

# Data
The object that is returned from the above endpoints.
```json
{
  "object_id": 65656,
  "data": [
    {
      "key": "key1",
      "val": "val1",
      "valType": "str"
    }
  ]
}
```
### Now we assume that the server is running

To test it locally, you have test_api.py file. It's a pytest file, you can run all of it or test by test.
If you're using GitHub Actions, you have Pytest job for it, it starts simultaneously with the Server job.

The list of tests is:

* test_wrong_auth
* test_auth
* test_get
* test_create_obj
* test_get_last_obj
* test_delete_last_obj
* test_server_not_running
* test_get_after_shutdown

 ## To run
 To run all tests altogether:
 ```pytest test_api.py -s -v```
 
 To run test by test:
```pytest test_api.py::<test_name> -s -v```

They are designed to run separately as well.
