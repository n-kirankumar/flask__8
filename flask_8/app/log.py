"""
log.py
-------
Contains functions for logging messages.
"""

import logging

# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def log_message(level, message):
    """
    Logs a message with a specified level.

    Args:
        level (str): The logging level ('info', 'error').
        message (str): The message to log.
    """
    if level == 'info':
        logging.info(message)
    elif level == 'error':
        logging.error(message)
    else:
        logging.warning(f"Unknown log level: {level}. Message: {message}")
