import logging

# Get or create a logger
logger = logging.getLogger(__name__)

# Set log level
logger.setLevel(logging.DEBUG)  # Set the minimum log level you want to capture

# Create a StreamHandler for console output
console_handler = logging.StreamHandler()

# Define the log message format
formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
console_handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(console_handler)

# Log messages
# logger.debug('A debug message')  # This will print because level is DEBUG
# logger.info('An info message')  # This will print because level is DEBUG
# logger.warning('Something is not right.')  # This will print
# logger.error('A Major error has happened.')  # This will print
# logger.critical('Fatal error. Cannot continue')  # This will print
