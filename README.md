# How to run

The script runs on Python 3.9

To run the server run the server.py file
### Create a virtual environment
On Linux:
```bash
python3 -m venv /path/to/new/virtual/environment
```
On Windows:
```bash
python -m venv c:\path\to\myenv
```
#### Activate venv
On Linux
```bash
./venv/bin/activate
```
On Windows
```bash
.\venv\Scripts\activate
```
### Run the server.py
Install dependencies
```bash
$ pip install -r requirements.txt
```

Change to the server directory
```bash
$ cd test-server
```

Run server.py
```bash
$ python server.py
```
The server will be available at `http://localhost:8000`

 # API Reference

 ## Authentication
 You must authenticate with the API to gain access first.
 The following endpoint will return an access token which should be added to the `Authorization` header

 Username and password will be provided.

 | Endpoint  | Method | Params                                                             | Response                                                           | Example |
|-----------|--------|--------------------------------------------------------------------|--------------------------------------------------------------------|---------|
| /api/auth | POST   | Json Body: ``` {   "username": "test",   "password": "1234" }  ``` |  ``` { "access_token":"ververylongstringwithnumbersandstuff" } ``` |         |


 ### *All endpoints require the following headers*
 ```
 "Content-Type": "application/json"
 "Authorization": "Bearer {your_token_here}"
 ```

## Endpoints

| Endpoint              | Method | Params                                                                                                                 | Returns              | Example |
|-----------------------|--------|------------------------------------------------------------------------------------------------------------------------|----------------------|---------|
| /api/data             | GET    |                                                                                                                        | List of Data         |         |
| /api/data             | POST   | json body: ```json {   "data": [     {       "key": "key1",       "val": "val1",       "valType": "str"     }   ] }``` | The created object   |         |
| /api/data/<object_id> | GET    | object_id: int - Representing the object id                                                                            | Data                 |         |
| /api/data/<object_id> | DELETE | object_id: int - Representing the object id  to delete                                                                 | `200` Empty Response |         |

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
Example of server logging:
```commandline
[2023-01-12 11:40:23 +0200] - (sanic.access)[INFO][127.0.0.1:60614]: POST http://localhost:8000/api/auth/  401 66
[2023-01-12 11:40:25 +0200] - (sanic.access)[INFO][127.0.0.1:60618]: POST http://localhost:8000/api/auth/  200 144
[2023-01-12 11:40:27 +0200] - (sanic.access)[INFO][127.0.0.1:60622]: POST http://localhost:8000/api/auth/  200 144
[2023-01-12 11:40:29 +0200] - (sanic.access)[INFO][127.0.0.1:60624]: GET http://localhost:8000/api/data/  200 75
[2023-01-12 11:40:31 +0200] - (sanic.access)[INFO][127.0.0.1:60628]: POST http://localhost:8000/api/auth/  200 144
[{'key': 'key1', 'val': 'val1', 'valType': 'str'}]
key
val
valType
[2023-01-12 11:40:33 +0200] - (sanic.access)[INFO][127.0.0.1:60630]: POST http://localhost:8000/api/data/  200 68
[2023-01-12 11:40:35 +0200] - (sanic.access)[INFO][127.0.0.1:60634]: POST http://localhost:8000/api/auth/  200 144
[2023-01-12 11:40:37 +0200] - (sanic.access)[INFO][127.0.0.1:60636]: GET http://localhost:8000/api/data/  200 144
[2023-01-12 11:40:39 +0200] - (sanic.access)[INFO][127.0.0.1:60638]: GET http://localhost:8000/api/data/2  200 68
[2023-01-12 11:40:41 +0200] - (sanic.access)[INFO][127.0.0.1:60642]: POST http://localhost:8000/api/auth/  200 144
[2023-01-12 11:40:44 +0200] - (sanic.access)[INFO][127.0.0.1:60644]: GET http://localhost:8000/api/data/  200 144
[2023-01-12 11:40:46 +0200] - (sanic.access)[INFO][127.0.0.1:60646]: DELETE http://localhost:8000/api/data/2  200 3
[2023-01-12 11:40:48 +0200] - (sanic.access)[INFO][127.0.0.1:60650]: POST http://localhost:8000/api/auth/  200 144
[{'key': 'terminate', 'val': 'val1', 'valType': 'str'}]
key
Got the terminate signal
Stopping the server, pid=47544

```
# Testing
### Now we assume that the server is running

To test it, you have test_api.py file. 
It's a pytest file, you can run all of it or test by test.

The list of tests is:

* test_wrong_auth
* test_auth
* test_get
* test_create_obj
* test_get_last_obj
* test_delete_last_obj
* test_server_stop
* test_get_after_shutdown

 ## To run
* Open another terminal window
* Run in the same venv, as the server
* Change to the testing directory
```bash
$ cd testing
```


 To run all tests altogether:
 ```pytest test_api.py -s -v```
 
 To run test by test:
```pytest test_api.py::<test_name> -s -v```

They are designed to run separately as well.

Example of test run:
```commandline
(venv) C:\Users\sasha\PycharmProjects\Homework\testing>pytest -v -s test_api.py
================================================= test session starts =================================================
platform win32 -- Python 3.9.12, pytest-6.2.2, py-1.11.0, pluggy-0.13.1 -- C:\Users\sasha\salt\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\sasha\PycharmProjects\Homework\testing
plugins: sanic-1.6.2
collected 8 items

test_api.py::test_wrong_auth Didn't get token! Response code: 401
PASSED
test_api.py::test_auth Authenticated successfully! The token is: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjpudWxsLCJleHAiOjE2NzM1MTgyMjV9.cyt1BV8ZlEIabEkPyRiBhPSB-zKXfEhpDBWRbClgXhM
PASSED
test_api.py::test_get Authenticated successfully! The token is: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjpudWxsLCJleHAiOjE2NzM1MTgyMjd9.tZVXC3aECTa2td1GMJ_hwXj5nbva1we9JiU9MOd369I
Getting a list of all objects
Here are the objects! [{'object_id': 1, 'data': [{'key': 'terminate', 'val': 'val1', 'valType': 'str'}]}]
Here is the output!
{
    "object_id": 1,
    "data": [
        {
            "key": "terminate",
            "val": "val1",
            "valType": "str"
        }
    ]
}
PASSED
test_api.py::test_create_obj Authenticated successfully! The token is: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjpudWxsLCJleHAiOjE2NzM1MTgyMzF9.rZ9idXRvTK-SjFidgBfxpdVgx6NioW1NQdU924cbfqg
Creating a new object {'data': [{'key': 'key1', 'val': 'val1', 'valType': 'str'}]}
{
    "object_id": 2,
    "data": [
        {
            "key": "key1",
            "val": "val1",
            "valType": "str"
        }
    ]
}
id of created objects: 2
PASSED
test_api.py::test_get_last_obj Authenticated successfully! The token is: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjpudWxsLCJleHAiOjE2NzM1MTgyMzV9.EfMB-RnRsAaGsZnjEd2-WiMG6Q3Tcc_7z0RrX2YvLWY
Getting a list of all object ids
All the ids! [1, 2]
Get the last created obj, which has the id: 2
{
    "object_id": 2,
    "data": [
        {
            "key": "key1",
            "val": "val1",
            "valType": "str"
        }
    ]
}
PASSED
test_api.py::test_delete_last_obj Authenticated successfully! The token is: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjpudWxsLCJleHAiOjE2NzM1MTgyNDF9.chuOa_uG-7L0SEsDGkZwZwrRDpFnHhax-3AdiWptJ-U
Getting a list of all object ids
All the ids! [1, 2]
Deleting the most recent object, id: 2
200
PASSED
test_api.py::test_server_stop Authenticated successfully! The token is: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjpudWxsLCJleHAiOjE2NzM1MTgyNDh9.PmrAcZhBvRQ0VngYUyDM7NQvJjcXge4hakn9zc8rquM
Trying to stop the server, sending {'data': [{'key': 'terminate', 'val': 'val1', 'valType': 'str'}]}
The server is really down
PASSED
test_api.py::test_get_after_shutdown The server is really down
PASSED

================================================= 8 passed in 32.53s ==================================================

```