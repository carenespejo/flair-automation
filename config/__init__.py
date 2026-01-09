"""
============================================================
 settings.py
============================================================

WHAT THIS FILE IS FOR
----------------------
- Central place for framework configuration values such as:
        - Base URL of the application under test
        - Default explicit wait timeout
        - Browser selection

WHAT YOU SHOULD EDIT
--------------------
- UPDATE THE VALUES in the "USER-CONFIGURABLE SETTINGS" section
        to match your environment and target application.

WHAT YOU SHOULD NOT EDIT
------------------------
- DO NOT MODIFY ANYTHING in the "INTERNAL CONSTANTS" section
        unless you know exactly what you're doing.
        These are used by the framework and tests.
"""

# ============================================================
# USER-CONFIGURABLE SETTINGS
# ============================================================

# TODO: UPDATE THIS TO YOUR APPLICATION'S BASE URL
BASE_URL: str = "https://test.techignitebusiness.com:7012/"

# TODO: UPDATE THIS IF YOU WANT A DIFFERENT DEFAULT TIMEOUT (IN SECONDS)
EXPLICIT_WAIT_TIMEOUT: int = 10

# TODO: UPDATE THIS IF YOU WANT TO USE A DIFFERENT BROWSER
# Supported values in this template: "chrome"
BROWSER: str = "chrome"
# USER-CONFIGURABLE SETTINGS
HEADLESS: bool = False

# ============================================================
# INTERNAL CONSTANTS (DO NOT MODIFY)
# ============================================================

# DO NOT MODIFY THIS FILE BELOW THIS LINE UNLESS YOU KNOW WHAT YOU'RE DOING

DEFAULT_BASE_URL = BASE_URL
DEFAULT_WAIT_TIMEOUT = EXPLICIT_WAIT_TIMEOUT
DEFAULT_BROWSER = BROWSER
DEFAULT_HEADLESS = HEADLESS