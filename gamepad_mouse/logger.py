import logging
import os
from datetime import datetime


def setup_logger() -> logging.Logger:
    """Setup logger for the application"""
    os.makedirs('logs', exist_ok=True)

    log_filename = f'logs/mouse_movement_{
        datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)
