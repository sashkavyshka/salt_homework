# How to run

To run the server run the server.py file

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

To test it, you have test_api.py file. 
It's a pytest file, you can run all of it or test by test.

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