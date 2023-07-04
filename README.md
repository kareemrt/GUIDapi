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

tbd

## Use Instructions

1. Run the Tornado server, either by
    - directly executing api.py, which requires the dependencies in 'requirements.txt' to be installed
    - creating & running a docker image using the supplied DockerFile
2. Execute CRUD commands via the API, either by
    - using the web-interface
    - passing information to the endpoints directly

## Directory Structure

tbd

## DB Schema

**DB documents contain:**
1. GUID
2. Expiration Time
3. User