#!/usr/bin/env python3

# write a python script to manage discourse via api calls.
# It should generate a list of users, and then for each user:
# 1. check if the user exists
# 2. if not, create the user
# 3. if so, update the user
# 4. add the user to a group
# The script should read the apikey from a file, and the list of users from a file.
# The script should be able to be run multiple times without creating duplicate users.

import requests
import json
import os
import sys

# get the api key from a file
def get_api_key():
    with open('apikey.txt', 'r') as f:
        apikey = f.read().strip()
    return apikey

# get the list of users from a file
def get_users():
    with open('users.txt', 'r') as f:
        users = f.read().strip().split('\n')
    return users

# check if a user exists
def check_user_exists(username, apikey):
    url = 'https://discourse.example.com/users/{0}.json?api_key={1}&api_username=system'.format(username, apikey)
    r = requests.get(url)
    if r.status_code == 200:
        return True
    else:
        return False
    
# create a user
def create_user(username, apikey):
    url = 'https://discourse.example.com/admin/users.json'
    data = {
        'name': username,
        'username': username,
        'email': username + '@example.com',
        'password': 'password',
        'active': 'true',
        'approved': 'true',
        'api_key': apikey,
        'api_username': 'system'
    }
    r = requests.post(url, data=data)
    if r.status_code == 200:
        return True
    else:
        return False

# update a user
def update_user(username, apikey):
    url = 'https://discourse.example.com/admin/users/{0}/preferences.json'.format(username)
    data = {
        'email': username + '@example.com',
        'api_key': apikey,
        'api_username': 'system'
    }
    r = requests.put(url, data=data)
    if r.status_code == 200:
        return True
    else:
        return False

# add a user to a group
def add_user_to_group(username, apikey):
    url = 'https://discourse.example.com/admin/groups/1/members.json'
    data = {
        'usernames': username,
        'api_key': apikey,
        'api_username': 'system'
    }
    r = requests.put(url, data=data)
    if r.status_code == 200:
        return True
    else:
        return False

# main function
def main():
    apikey = get_api_key()
    users = get_users()
    for username in users:
        if not check_user_exists(username, apikey):
            if create_user(username, apikey):
                print('User {0} created.'.format(username))
            else:
                print('User {0} failed to create.'.format(username))
        else:
            if update_user(username, apikey):
                print('User {0} updated.'.format(username))
            else:
                print('User {0} failed to update.'.format(username))
        if add_user_to_group(username, apikey):
            print('User {0} added to group.'.format(username))
        else:
            print('User {0} failed to add to group.'.format(username))
            
if __name__ == '__main__':
    main()
