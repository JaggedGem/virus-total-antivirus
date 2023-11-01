# bundle.py
import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import json
import logger

# rest of the code...

# main_linker.py
import os
import json
import tkinter as tk
from tkinter import Entry, Label, Button, messagebox
import sys
import logger

# rest of the code...

# logger.py
import logging

# Create a logger
logger = logging.getLogger(__name__)

# Set the log level
logger.setLevel(logging.INFO)

# Create a file handler
handler = logging.FileHandler('app.log')

# Set the log level of the handler
handler.setLevel(logging.INFO)

# Create a formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Set the formatter for the handler
handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(handler)

# main.py
import json
import requests
import hashlib
import sys
import tkinter as tk
import os
import time
import logger

# rest of the code...
