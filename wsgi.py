#!/usr/bin/python3
import os
import sys
import logging
from borrowers import app as application


# logging.basicConfig(stream=sys.stderr)
logging.basicConfig(filename='/var/log/borrowers/borrowers.log',
                    level=logging.INFO)
sys.path.insert(0, "/var/www/html/borrowers")
