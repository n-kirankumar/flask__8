"""
constants.py
-------------
Contains constants for the application, including status codes, HTTP methods, and log messages.
"""

VALID_COUNTRY_LIST = ['USA', 'India', 'UK', 'Canada']
EXCLUDED_NUMBERS = ['1234567890', '0987654321']
VALID_GENDERS = ['male', 'female', 'other']
VALID_BLOOD_GROUPS = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']

# HTTP Status Codes
STATUS_OK = 200
STATUS_CREATED = 201
STATUS_BAD_REQUEST = 400
STATUS_NOT_FOUND = 404
STATUS_FORBIDDEN = 403

# HTTP Methods
METHOD_GET = 'GET'
METHOD_POST = 'POST'
METHOD_PATCH = 'PATCH'

LOG_MESSAGES = {
    'invalid_email': "Invalid email: {}",
    'valid_email': "Valid email: {}",
    'invalid_age': "Invalid age: {}",
    'valid_age': "Valid age: {}",
    'invalid_mobile': "Invalid mobile number: {}",
    'valid_mobile': "Valid mobile number: {}",
    'invalid_gender': "Invalid gender: {}",
    'valid_gender': "Valid gender: {}",
    'invalid_blood_group': "Invalid blood group: {}",
    'valid_blood_group': "Valid blood group: {}",
    'user_not_found': "User not found: {}",
    'unauthorized_access': "Unauthorized access: {} trying to access {}",
    'user_info': "User info: {}, {}",
    'user_exists': "User already exists: {}",
    'user_created': "User created: {}, {}",
    'user_updated': "User updated: {}, {}",
    'unauthorized_update': "Unauthorized update: {} trying to update {}",
    'unauthorized_list_users': "Unauthorized list users: {}",
    'list_all_users': "Listing all users: {}"
}
