import logging

def setup_logging():
    logging.basicConfig(
        filename='app.log',  # Log to a file
        filemode='w',        # Overwrite the log file on each run
        level=logging.INFO,  # Set the threshold level to INFO
        format='%(levelname)s:%(asctime)s:%(message)s'  # Set the format for the log messages
    )

    
    logger = logging.getLogger(__name__)
    return logger
