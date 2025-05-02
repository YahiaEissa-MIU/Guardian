import os
import sys


def create_app_data_dir():
    """Create application data directory if it doesn't exist"""
    if sys.platform == "win32":
        app_data = os.path.join(os.environ['APPDATA'], 'Guardian')
    else:
        app_data = os.path.join(os.path.expanduser('~'), '.guardian')

    if not os.path.exists(app_data):
        os.makedirs(app_data)
    return app_data


# Create necessary directories when the application starts
create_app_data_dir()
