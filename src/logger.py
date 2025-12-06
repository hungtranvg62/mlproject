"""
logger.py

This module is responsible for setting up logging for the project.

Logging is the practice of recording events, messages, and errors that occur
while a program is running. It is an essential tool for understanding the flow
of execution, diagnosing issues, and keeping track of what the code is doing
at different stages.

In a machine learning project, logging is especially useful because it helps:
- Monitor the progress of data processing and model training.
- Capture errors and exceptions for easier debugging.
- Keep a record of experiments and results for reproducibility.
"""

import logging
import os
from datetime import datetime

LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
logs_path = os.path.join(os.getcwd(), "logs", LOG_FILE)
os.makedirs(logs_path, exist_ok = True)

LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,

)

# if __name__ == "__main__":
#     logging.info("Logging has started") # runs only when the file is run directly, not when it is imported