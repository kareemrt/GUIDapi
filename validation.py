# Name: Kareem T
# Date: 07/04/2023
# Modu: validation.py
# Desc: Module performing server-side format validation of user input, does NOT include database queries.
import datetime
import secrets
import re
import json

# Format Tests ==================================================================

def is_unix(time) -> bool:
    '''Check whether user supplied time is in UNIX format and yet to happen'''
    try:
        given_time = datetime.datetime.utcfromtimestamp(float(time)) # Convert user time to datetime
        current_time = datetime.datetime.utcnow() # Get current time
        return given_time > current_time # Check given time is after current
    except (ValueError, OverflowError, OSError): # Input time cannot be converted
        return False

def is_32_bit_hex(guid) -> bool:
    '''Check whether GUID is a 32-bit uppercase hexadecimal '''
    pattern = r"^[0-9A-F]{32}$"
    return bool(re.match(pattern, guid))

def is_json(received_data):
    '''Check whether user input is in JSON format'''
    try: json_data = json.loads(received_data) # Retrieve and parse the JSON data
    except json.JSONDecodeError: return False
    return json_data

# Complicity Checks =============================================================

def can_create(received_data, subpath):
    '''Test validity for whether user can perform CREATE operation'''

    # Format Check
    json_data = is_json(received_data)
    if not json_data: return 'Error! - Create Error: Invalid JSON format'  
    if 'user' not in json_data: return 'Error! - Create Error: No user specified!' # Not specified on API
    if json_data['user'].strip() == '': return 'Error! - Create Error: No user specified!' # Not specified on web-interface

    # Expiration Checks
    if 'expire' not in json_data: json_data['expire'] = generate_expiration() # Not specified on API
    if json_data['expire'].strip() == '': json_data['expire'] = generate_expiration() # Not specified on web-interface
    if not is_unix(time = json_data['expire']): return 'Error! - Create Error: Invalid expiration time format (must be UNIX format)' # Check time format
    
    # GUID Checks (existence/format)
    if subpath == '': subpath = generate_guid()
    if not is_32_bit_hex(subpath): return 'Error! - Create Error: Invalid GUID format (must be 32-bit Hexadecimal Uppercase)'
    json_data['guid'] = subpath
    return json_data

def can_update(received_data, subpath):
    '''Test validity for whether user can perform UPDATE operation'''

    # JSON Check
    json_data = is_json(received_data)
    if not json_data: return 'Error! - Update Error: Invalid JSON format'  

    # Expiration Checks
    if 'expire' in json_data:
        if json_data['expire'].strip() == '': del json_data['expire'] # remove empty fields (web app creates fields even if empty)
        elif not is_unix(time = json_data['expire']): return 'Error! - Update Error: Invalid expiration time (must be UNIX format)' # Check time format

    # User Check
    if 'user' in json_data:
        if json_data['user'].strip() == '': del json_data['user'] # remove empty fields

    # GUID Checks (existence/format)
    if not is_32_bit_hex(subpath): return 'Error! - Create Error: Invalid GUID format (must be 32-bit Hexadecimal Uppercase)'
    json_data['guid'] = subpath
    return json_data

# Generator Functions ===========================================================

def generate_expiration() -> int:
    '''Returns a datetime object 30 days ahead (in case user does not supply expiration)'''
    current_time = datetime.datetime.utcnow() # Get current time (datetime)
    generated_time = current_time + datetime.timedelta(days=30) # Get datetime 30 days out
    generated_unix_time = int(generated_time.timestamp()) # Convert the new datetime back to Unix time (int)
    return str(generated_unix_time)

def generate_guid() -> str:
    '''Returns 32 random uppercase hexadecimals'''
    return secrets.token_bytes(16).hex().upper()