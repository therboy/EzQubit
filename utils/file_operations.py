# utils/file_operations.py

"""
Provides utility functions for file operations.
"""

import os
import json

def save_json(data, file_path):
    """
    Saves data to a JSON file.

    Args:
        data (dict): The data to save.
        file_path (str): The path to the JSON file.
    """
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

def load_json(file_path):
    """
    Loads data from a JSON file.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        dict: The loaded data.
    """
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data
