"""
app.py
------
Flask application for managing user profiles with GET, POST, and PATCH methods.
"""

from flask import Flask, request, jsonify
from utils import get_user_info, list_all_users, create_user_profile, update_user_profile
from constants import (
    METHOD_GET, METHOD_POST, METHOD_PATCH, STATUS_OK, STATUS_CREATED, STATUS_BAD_REQUEST,
    STATUS_NOT_FOUND, STATUS_FORBIDDEN, LOG_MESSAGES
)
from log import log_message

app = Flask(__name__)

@app.route('/api/user/<username>', methods=[METHOD_GET, METHOD_POST, METHOD_PATCH])
def handle_user(username):
    """
    Handles user profile management.

    Args:
        username (str): The username for the requested operation.

    Returns:
        Response: JSON response with user data or status messages.
    """
    log_message('info', f'Started handling request for username: {username}')

    if request.method == METHOD_GET:
        log_message('info', 'Handling GET request')
        try:
            current_user = request.headers.get('X-Current-User')
            is_admin = request.headers.get('X-Is-Admin') == 'true'
            user_info = get_user_info(username, current_user, is_admin)
            return jsonify(user_info), STATUS_OK
        except ValueError as e:
            log_message('error', str(e))
            return jsonify({"error": str(e)}), STATUS_NOT_FOUND
        except PermissionError as e:
            log_message('error', str(e))
            return jsonify({"error": str(e)}), STATUS_FORBIDDEN

    elif request.method == METHOD_POST:
        log_message('info', 'Handling POST request')
        user_data = request.json
        try:
            created_user = create_user_profile(username, user_data)
            return jsonify(created_user), STATUS_CREATED
        except ValueError as e:
            log_message('error', str(e))
            return jsonify({"error": str(e)}), STATUS_BAD_REQUEST

    elif request.method == METHOD_PATCH:
        log_message('info', 'Handling PATCH request')
        updated_data = request.json
        try:
            current_user = request.headers.get('X-Current-User')
            is_admin = request.headers.get('X-Is-Admin') == 'true'
            if not is_admin and current_user != username:
                raise PermissionError(LOG_MESSAGES['unauthorized_update'].format(current_user, username))
            updated_user = update_user_profile(username, updated_data)
            return jsonify(updated_user), STATUS_OK
        except ValueError as e:
            log_message('error', str(e))
            return jsonify({"error": str(e)}), STATUS_BAD_REQUEST
        except PermissionError as e:
            log_message('error', str(e))
            return jsonify({"error": str(e)}), STATUS_FORBIDDEN

    log_message ('info', f'Finished handling request for username: {username}')
    return jsonify({"error": "Invalid method"}), STATUS_BAD_REQUEST

if __name__ == '__main__':
    app.run(debug=True)
