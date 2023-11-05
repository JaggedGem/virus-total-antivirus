import logging

# Create a logger
my_logger = logging.getLogger(__name__)

# Set the log level to DEBUG
my_logger.setLevel(logging.DEBUG)

# Create a file handler
handler = logging.FileHandler('app.log')

# Set the log level of the handler to DEBUG
handler.setLevel(logging.DEBUG)

# Create a formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Set the formatter for the handler
handler.setFormatter(formatter)

# Add the handler to the logger
my_logger.addHandler(handler)