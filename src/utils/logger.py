import logging
import sys
from pathlib import Path

def setup_logger(log_file=None, log_level=logging.INFO):
    """Setup logger with console and file handlers."""
    # Create logger
    logger = logging.getLogger()
    logger.setLevel(log_level)
    
    # Create formatters
    console_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)
    
    # Create file handler if log file is provided
    if log_file:
        log_dir = Path(log_file).parent
        log_dir.mkdir(exist_ok=True)
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)
    
    return logger

def get_logger(name, log_file=None, log_level=logging.INFO):
    """Get a module logger."""
    # If root logger is not configured, set it up
    if not logging.getLogger().handlers:
        setup_logger(log_file, log_level)
    
    return logging.getLogger(name)