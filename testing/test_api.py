# -*- coding: utf-8 -*-
"""
Test to check api calls
"""

import requests
import pytest
import json
import socket


URL = "http://0.0.0.0:8000"
data = {
    "data": [{"key": "key1", "val": "val1", "valType": "str"}]}

term_data= {
    "data": [{"key" : "terminate", "val": "val1", "valType": "str"}]}


credentials_data = {
    "username": "test",
    "password": "1234"
}
wrong_data = {
    "username": "tests",
    "password": "1235"
}


def get_token(log_data):
    """
    Helper function to authorize to the server
    Arg:
        (dict) log_data: to connect to the server
    Returns:
        (str) token: the token or the empty string
    """

    response = requests.post(f"{URL}/api/auth/", json=log_data)

    if response.status_code == 200:
        token = response.json()["access_token"]
        print(f'Authenticated successfully! The token is: {token}')
        return token
    else:
        print(f"Didn't get token! Response code: {response.status_code}")
        return ""


def get_objects_ids(headers):
    """
    Helper function to get objects from the server
    Returns:
        (list) objects
    """
    print('Getting a list of all object ids')
    object_ids = []
    res = requests.get(f"{URL}/api/data/", headers=headers)
    objects = json.loads(res.text)
    for obj in objects:
        object_ids.append(obj['object_id'])
    print(f"All the ids! {object_ids}")
    return object_ids


def create_obj(headers):
    """
    Helper function to create an object
    Returns:
        (obj) object
    """
    res = requests.post(f"{URL}/api/data/", json=data, headers=headers)
    print(json.dumps(res.json(), indent=4, default=str))
    object = json.loads(res.text)
    return object


def stop_server(headers):
    """
    Helper function to stop the server
    Returns:
        (obj) object
    """
    res = requests.post(f"{URL}/api/data/", json=term_data, headers=headers)
    print(json.dumps(res.json(), indent=4, default=str))
    return True

def delete_obj(object_id, headers):
    """
    Helper function to delete an object
    Args:
        object_id (int): the object to delete
        headers(dict): to connect to the server
    Returns:
        (int) response code
    """
    res = requests.delete(f"{URL}/api/data/{object_id}", headers=headers)
    return res.status_code


def test_wrong_auth():
    """Test to check that not authenticated user cannot perform any actions

    :return: None

    """

    # Get access token
    access_token = get_token(wrong_data)
    assert access_token == "", "Could authorize to the server with wrong data!"


def test_auth():
    """Test to check that an authenticated user can do actions

    :return: None

    """

    # Get access token
    access_token = get_token(credentials_data)
    assert access_token != "", "Couldn't authorize to the server!"


def test_get():
    """Test the GET endpoint

    :return: None

    """
    access_token = get_token(credentials_data)

    objects = ""
    if access_token:
        # Send request to endpoint
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        }

        # Endpoint: /api/data
        # Method: GET
        print('Getting a list of all objects')
        res = requests.get(f"{URL}/api/data/", headers=headers)
        objects = json.loads(res.text)
        print(f"Here are the objects! {objects}")
        for obj in objects:
            print("Here is the output!")
            print(json.dumps(obj, indent=4, default=str))
    else:
        pytest.xfail("Couldn't authorize")

    assert objects != "", "ERROR: GET method didn't bring anything!"


def test_create_obj():
    """Test the CREATE endpoint

    :return: None

    """
    access_token = get_token(credentials_data)
    if access_token:
        # Send request to endpoint
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        }

        # Endpoint: /api/data/<object_id>
        # Method: CREATE
        print(f'Creating a new object {data}')
        got_obj = create_obj(headers)

        object_id = got_obj['object_id']
        print(f"id of created objects: {object_id}")

        example_obj = {"data": data["data"], "object_id": object_id}

    else:
        pytest.xfail("Couldn't authorize")

    assert example_obj == got_obj, "Object created is different from object sent!"


def test_get_last_obj():
    """Test the GET endpoint with object number, returning the latest obj

    :return: None

    """
    access_token = get_token(credentials_data)
    if access_token:
        # Send request to endpoint
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        }
        object_id = get_objects_ids(headers)[-1]
        # Endpoint: /api/data/<object_id>
        # Method: GET
        print(f'Get the last created obj, which has the id: {object_id}')
        res = requests.get(f"{URL}/api/data/{object_id}", headers=headers)
        got_obj = json.loads(res.text)
        print(json.dumps(res.json(), indent=4, default=str))
        example_obj = {"data": data["data"], "object_id": object_id}
    else:
        pytest.xfail("Couldn't authorize")

    assert example_obj == got_obj, "Object got is different from object saved!"


def test_delete_last_obj():
    """Test the DELETE endpoint with object number

    :return: None

    """
    access_token = get_token(credentials_data)
    status_code = 0
    if access_token:
        # Send request to endpoint
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        }

        object_id = get_objects_ids(headers)[-1]
        print(f'Deleting the most recent object, id: {object_id}')
        status_code = delete_obj(object_id, headers)
        print(status_code)

    else:
        pytest.xfail("Couldn't authorize")

    assert status_code == 200, "The return code is different from expected!"


def test_server_stop():
    """Test that there is no response if the server is not running

    :return: None

    """
    access_token = get_token(credentials_data)
    status_code = 0
    down = False
    if access_token:
        # Send request to endpoint
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        }
        object_id = 0
        # Endpoint: /api/data/<object_id>
        # Method: GET
        print(f'Trying to stop the server, sending {term_data}')

        try:
            got_obj = stop_server(headers)
        except socket.error as e:
            print("The server is really down")
            down = True
    else:
        pytest.xfail("Couldn't authorize")

    assert down, "The server isn't down!"


def test_get_after_shutdown():
    """Test the GET endpoint when server is down

    :return: None

    """
    down = False
    try:
        access_token = get_token(credentials_data)
    except socket.error as e:
        print("The server is really down")
        down = True

    assert down, "ERROR: The server isn't really down!"
