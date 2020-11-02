# Coffee Shop Full Stack

## Overview

This is coffee shop project to help the managers and baristas receive and manage their drinks


## Setup

Check the README.md file in frontend and backend for details about setup and running this project:

1. [`./backend/`](./backend/README.md)
2. [`./frontend/`](./frontend/README.md)

## Auth0 Setup

We are using 3rd party authentication service, which is Auth0, for more details check backend [README.md](./backend/README.md).

## Stack

This is a full-stack project that uses flask micro-framework on the backend and Angular with Ionic UI toolkit on the frontend.

## API Endpoint

GET /drinks
- fetches all drinks in the home page, this is a public endpoint so does not require permission.
- it fetches less details about drinks (less format)
- response: { 
              "success": true,
              "drinks": 
              [
                  { "id": 1,
                   [
                       { 
                         "color": "#FFA000",
                         "parts": 3 
                        }
                    ]
                   }
              ]
            }

GET /drinks-detail
- fetches all drinks in the home page, this endpoint requires "get:drinks-detail" permission.
- it fetches more details about drinks (long format)
- response: { 
              "success": true,
              "drinks": 
              [
                  { 
                    "id": 1,
                   [
                       { 
                         "name": "coffee",
                         "color": "#FFA000",
                         "parts": 3 
                        }
                    ]
                   }
              ]
            }

Fore more details check [`./backend/`](./backend/README.md).


## Running tests

Using a collection in Postman application provided in 'backend/udacity-fsnd-udaspicelatte.postman_collection.json'
Note: make sure you have provided the correct jwt tokens for barista and manager in the authorization tab.

## Authors

Mostafa Bohram, mostafabohram@gmail.com


