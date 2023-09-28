#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 10:36:18 2023

@author: tristan
"""

import os
import logging
import datetime

import streamlit.config as config


def configure_logger(log_dir='logs'):
    """Creates a logger for the program."""
    # Create a directory for logs (if it doesn't exist)
    os.makedirs(log_dir, exist_ok=True)

    # Get today's date as a string in the format 'YYYY-MM-DD'
    today_date = datetime.datetime.now().strftime('%Y-%m-%d')

    # Construct the log file path with today's date
    log_file_path = os.path.join(log_dir, f'{today_date}_dashfoot.log')

    logger = logging.getLogger(__name__)

    # Read the logger level from Streamlit's configuration
    streamlit_log_level = config.get_option("logger.level")

    # Map Streamlit's log level to Python's logging level
    log_level_mapping = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
    }

    # Set the logger's level based on the Streamlit configuration
    logger.setLevel(log_level_mapping.get(streamlit_log_level.lower(), logging.INFO))

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # File handler
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setFormatter(formatter)

    # Check if file handler is already added to avoid duplicates
    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger
