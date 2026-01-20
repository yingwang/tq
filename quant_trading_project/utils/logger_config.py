"""
Logging configuration for the quantitative trading project
"""
import logging
import os
from datetime import datetime


def setup_logger(name: str, log_file: str = None, level: int = logging.INFO) -> logging.Logger:
    """
    Set up a logger with both file and console handlers
    
    Args:
        name: Name of the logger
        log_file: Path to log file (optional, defaults to logs directory)
        level: Logging level (default INFO)
    
    Returns:
        logging.Logger: Configured logger instance
    """
    # Create logs directory if it doesn't exist
    logs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs')
    os.makedirs(logs_dir, exist_ok=True)
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Prevent adding multiple handlers if logger already exists
    if logger.handlers:
        return logger
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    
    # File handler
    if log_file is None:
        log_filename = f"trading_{datetime.now().strftime('%Y%m%d')}.log"
        log_file = os.path.join(logs_dir, log_filename)
    
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    
    # Add handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger


def log_exception(logger: logging.Logger, func_name: str = ""):
    """
    Decorator to log exceptions in functions
    
    Args:
        logger: Logger instance
        func_name: Optional function name for logging
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                error_msg = f"Exception in {func.__name__ if not func_name else func_name}: {str(e)}"
                logger.error(error_msg, exc_info=True)
                raise
        return wrapper
    return decorator