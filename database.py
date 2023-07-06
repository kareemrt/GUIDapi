# Name: Kareem T
# Date: 07/04/2023
# Modu: database.py
# Desc: Module performing CRUD operations for MongoDB database.
import pymongo

# DB Connection
client = pymongo.MongoClient("mongodb://localhost:27017") # Establish a connection to MongoDB
db = client["mydb"] # Access the database
collection = db["id"] # Access the collection / table

def find_guid(guid) -> dict:
    '''Check whether a guid exists in the database'''
    return collection.find_one({"guid": guid}, {'_id': 0})

def create_guid(json_data):
    '''Insert a json record into the databse'''
    # Check record is complete
    keys = ['user','guid','expire']
    for key in keys: assert key in json_data
    # Insert / Return relevant info
    new_data = {key: json_data[key] for key in keys}
    result = collection.insert_one(new_data)
    if result.acknowledged: return {'guid': json_data['guid'], 'expire': json_data['expire'], 'user': json_data['user']}

def update_guid(json_data):
    '''Update existing guid'''
    filter = {'guid': json_data['guid']} # Filter
    # Update based on supplied info
    new_data = {'guid': json_data['guid']}
    if 'user' in json_data: 
        if json_data['user'].strip() != '': new_data['user'] = json_data['user']
    if 'expire' in json_data: new_data['expire'] = json_data['expire']
    update = {'$set': new_data}
    result = collection.update_one(filter, update)
    return result.modified_count > 0 # Return status

def delete_guid(guid):
    '''Delete the DB document of a given GUID'''
    result = collection.delete_one({'guid': guid})
    return result.deleted_count > 0

def clean_db():
    '''ADMIN function to wipe database'''
    return collection.delete_many({})

#clean_db()