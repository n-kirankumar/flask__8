"""
utils.py
---------
Contains utility functions for validating user data, retrieving user information, and decorators for authentication.
"""

import re
from log import log_message
from constants import (
    VALID_COUNTRY_LIST, EXCLUDED_NUMBERS, VALID_GENDERS, VALID_BLOOD_GROUPS, LOG_MESSAGES
)


def validate_email(email):
    """
    Validates the given email address.

    Args:
        email (str): The email address to validate.

    Raises:
        ValueError: If the email format is invalid.

    Returns:
        bool: True if the email is valid, False otherwise.
    """
    log_message('info', f'Started validating email: {email}')

    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regex, email):
        log_message('error', LOG_MESSAGES['invalid_email'].format(email))
        raise ValueError(LOG_MESSAGES['invalid_email'].format(email))

    log_message('info', LOG_MESSAGES['valid_email'].format(email))
    log_message('info', f'Finished validating email: {email}')
    return True


def validate_age(age):
    """
    Validates the given age.

    Args:
        age (int): The age to validate.

    Raises:
        ValueError: If the age is invalid.

    Returns:
        bool: True if the age is valid, False otherwise.
    """
    log_message('info', f'Started validating age: {age}')

    if not (0 < age < 120):
        log_message('error', LOG_MESSAGES['invalid_age'].format(age))
        raise ValueError(LOG_MESSAGES['invalid_age'].format(age))

    log_message('info', LOG_MESSAGES['valid_age'].format(age))
    log_message('info', f'Finished validating age: {age}')
    return True


def validate_mobile(mobile):
    """
    Validates the given mobile number.

    Args:
        mobile (str): The mobile number to validate.

    Raises:
        ValueError: If the mobile number is invalid or excluded.

    Returns:
        bool: True if the mobile number is valid, False otherwise.
    """
    log_message('info', f'Started validating mobile number: {mobile}')

    if mobile in EXCLUDED_NUMBERS:
        log_message('error', LOG_MESSAGES['excluded_mobile'].format(mobile))
        raise ValueError(LOG_MESSAGES['excluded_mobile'].format(mobile))

    mobile_regex = r'^\d{10}$'
    if not re.match(mobile_regex, mobile):
        log_message('error', LOG_MESSAGES['invalid_mobile'].format(mobile))
        raise ValueError(LOG_MESSAGES['invalid_mobile'].format(mobile))

    log_message('info', LOG_MESSAGES['valid_mobile'].format(mobile))
    log_message('info', f'Finished validating mobile number: {mobile}')
    return True


def validate_gender(gender):
    """
    Validates the given gender.

    Args:
        gender (str): The gender to validate.

    Raises:
        ValueError: If the gender is invalid.

    Returns:
        bool: True if the gender is valid, False otherwise.
    """
    log_message('info', f'Started validating gender: {gender}')

    if gender not in VALID_GENDERS:
        log_message('error', LOG_MESSAGES['invalid_gender'].format(gender))
        raise ValueError(LOG_MESSAGES['invalid_gender'].format(gender))

    log_message('info', LOG_MESSAGES['valid_gender'].format(gender))
    log_message('info', f'Finished validating gender: {gender}')
    return True


def validate_blood_group(blood_group):
    """
    Validates the given blood group.

    Args:
        blood_group (str): The blood group to validate.

    Raises:
        ValueError: If the blood group is invalid.

    Returns:
        bool: True if the blood group is valid, False otherwise.
    """
    log_message('info', f'Started validating blood group: {blood_group}')

    if blood_group not in VALID_BLOOD_GROUPS:
        log_message('error', LOG_MESSAGES['invalid_blood_group'].format(blood_group))
        raise ValueError(LOG_MESSAGES['invalid_blood_group'].format(blood_group))

    log_message('info', LOG_MESSAGES['valid_blood_group'].format(blood_group))
    log_message('info', f'Finished validating blood group: {blood_group}')
    return True


def validate_user_data(func):
    """
    Decorator function to validate user data (email, age, mobile, gender, blood group).

    Args:
        func (function): The function to wrap.

    Returns:
        function: The wrapped function.
    """

    def wrapper(*args, **kwargs):
        log_message('info', 'Started validating user data')
        user_data = kwargs.get('user_data', {})
        email = user_data.get('email')
        age = user_data.get('age')
        mobile = user_data.get('mobile')
        gender = user_data.get('gender')
        blood_group = user_data.get('blood_group')

        if email:
            validate_email(email)
        if age:
            validate_age(age)
        if mobile:
            validate_mobile(mobile)
        if gender:
            validate_gender(gender)
        if blood_group:
            validate_blood_group(blood_group)

        result = func(*args, **kwargs)
        log_message('info', 'Finished validating user data')
        return result

    return wrapper


@validate_user_data
def get_user_info(username, current_user, is_admin, user_data=None):
    """
    Retrieves information for the specified user.

    Args:
        username (str): The username of the user whose information is to be retrieved.
        current_user (str): The username of the current user making the request.
        is_admin (bool): Whether the current user is an admin.

    Raises:
        PermissionError: If the current user is not authorized to view the user's information.
        ValueError: If the user is not found.

    Returns:
        dict: The user's information.
    """
    log_message('info', f'Started retrieving user info for: {username}')

    from data import data

    if username not in data["records"]:
        log_message('error', LOG_MESSAGES['user_not_found'].format(username))
        raise ValueError(LOG_MESSAGES['user_not_found'].format(username))

    if not is_admin and current_user != username:
        log_message('error', LOG_MESSAGES['unauthorized_access'].format(current_user, username))
        raise PermissionError(LOG_MESSAGES['unauthorized_access'].format(current_user, username))

    user_info = data["records"][username]
    log_message('info', LOG_MESSAGES['user_info'].format(username, user_info))
    log_message('info', f'Finished retrieving user info for: {username}')
    return user_info


def list_all_users(current_user, is_admin):
    """
    Lists all users.

    Args:
        current_user (str): The username of the current user making the request.
        is_admin (bool): Whether the current user is an admin.

    Raises:
        PermissionError: If the current user is not authorized to list all users.

    Returns:
        dict: A dictionary of all users.
    """
    log_message('info', f'Started listing all users by: {current_user}')

    from data import data

    if not is_admin:
        log_message('error', LOG_MESSAGES['unauthorized_list_users'].format(current_user))
        raise PermissionError(LOG_MESSAGES['unauthorized_list_users'].format(current_user))

    all_users = data["records"]
    log_message('info', LOG_MESSAGES['list_all_users'].format(current_user))
    log_message('info', f'Finished listing all users by: {current_user}')
    return all_users


def create_user_profile(username, user_data):
    """
    Creates a new user profile.

    Args:
        username (str): The username of the new user.
        user_data (dict): The data for the new user.

    Raises:
        ValueError: If the user already exists or the data is invalid.

    Returns:
        dict: The newly created user profile.
    """
    log_message('info', f'Started creating user profile for: {username}')

    from data import data

    if username in data["records"]:
        log_message('error', LOG_MESSAGES['user_exists'].format(username))
        raise ValueError(LOG_MESSAGES['user_exists'].format(username))

    user_data['role'] = 'user'
    data["records"][username] = user_data
    log_message('info', LOG_MESSAGES['user_created'].format(username, user_data))
    log_message('info', f'Finished creating user profile for: {username}')
    return user_data


def update_user_profile(username, updated_data):
    """
    Updates an existing user profile.

    Args:
        username (str): The username of the user to update.
        updated_data (dict): The updated data for the user.

    Raises:
        ValueError: If the user is not found or the data is invalid.

    Returns:
        dict: The updated user profile.
    """
    log_message('info', f'Started updating user profile for: {username}')

    from data import data

    if username not in data["records"]:
        log_message('error', LOG_MESSAGES['user_not_found'].format(username))
        raise ValueError(LOG_MESSAGES['user_not_found'].format(username))

    data["records"][username].update(updated_data)
    log_message('info', LOG_MESSAGES['user_updated'].format(username, updated_data))
    log_message('info', f'Finished updating user profile for: {username}')
    return data["records"][username]
