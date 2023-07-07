# Name: Kareem T
# Date: 07/05/2023
# Modu: cache.py
# Desc: Module for interacting with cache (to send/retrieve data)
import redis

# Connection ============================================================

r = redis.Redis(host='localhost', port=6379) # Connect to Redis server

# Cache Functions =======================================================

def store(guid, json_data):
    '''Store record in cache using guid'''
    print(json_data, type(json_data))
    r.hmset(guid, json_data)

def retrieve(guid):
    '''Retrieve record from cache using guid'''
    data = r.hgetall(guid)
    decoded = {}
    for key, value in data.items():
        dec_key = key.decode('utf-8')
        dec_val = value.decode('utf-8')
        decoded[dec_key] = dec_val
    return decoded

def exists(guid):
    '''Check whether record exists in cache'''
    return r.hexists(guid, 'guid')

def delete(guid):
    '''Delete record from cache'''
    r.delete(guid)

def wipe_cache():
    '''Clean entire cache'''
    r.flushdb()

def close_cache():
    '''Close cache connection'''
    r.close()
