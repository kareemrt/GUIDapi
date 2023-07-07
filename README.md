## Simple REST-API Example
### Author: Kareem Taha | Date: 07/02/2023

API with web-interface to perform CRUD (Create, Read, Update, Delete) operations for a GUID database

## Constraints

- Cache layer to retrieve recently used GUI's
- Commands for *CRUD* operations
- **GUID Format: 32 hexadecimal characters (uppercase)**
- **Input/Ouput format: JSON**
- DB must contain *'expiration time'* (**UNIX format**): 30 days from creation if unspecified
- Validations: GUID format, Expiration format

## Architecture

![image](<templates/architecture.png>)

## Use Instructions

1. Initialize the database server (MongoDB) and the cache server (Redis) to connect to; this can be checked by running database.py/cache.py
1. Run the Tornado server, either by
    - directly executing api.py, which requires the dependencies in 'requirements.txt' to be installed
    - creating & running a docker image using the supplied DockerFile (untested)
2. Execute CRUD commands via the API, either by
    - using the web-interface
    - passing information to the endpoints directly

## Directory Structure

- templates: Folder containing HTML file(s) & design architecture
- api.py: Central framework of web-app/API
- validation.py: Tests to properly authorize user actions given proper formats
- database.py: Module to perform CRUD operations with database (MongoDB)
- cache.py: Module to perform CRUD operations with cache, for quick data retrieval
- requirements.txt: Required project dependencies
- DockerFile: A template to be used by docker to re-create the necessary runtime environment (docker container)

## DB Schema

**DB documents contain:**
1. GUID ('guid') - primary key
2. Expiration Time ('expire')
3. User ('user')