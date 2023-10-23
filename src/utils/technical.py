"""
Technical tools.
"""

import os
import logging


def setup_logger(
    name: str,
    level_of_log=logging.INFO,
    print_logs: bool = False,
    log_file_name: str = "last_session.log",
) -> logging.Logger:
    """
    Set up a logger with the specified name, log file, log level,
    and print option.

    Args:
        name (str): Name of the logger.
        log_file_name (str): Name of the log file.
        level_of_log (int, optional): Log level
            (default is logging.INFO).
        print_logs (bool, optional): Whether to print logs to console
            (default is False).

    Returns:
        logging.Logger: Configured logger object.
    """

    logs_path = os.path.join(os.getcwd(), "logs")

    if not os.path.exists(logs_path):
        os.makedirs(logs_path)

    this_log_path = os.path.join(logs_path, log_file_name)
    if not os.path.isfile(this_log_path):
        with open(this_log_path, "w", encoding="utf-8"):
            pass

    logger = logging.getLogger(name)
    message_format = logging.Formatter(
        "%(asctime)s - %(name)s %(levelname)s: %(message)s",
        "%Y-%m-%d %H:%M:%S",
    )
    file_handler = logging.FileHandler(this_log_path)
    file_handler.setFormatter(message_format)
    logger.setLevel(level_of_log)
    logger.addHandler(file_handler)

    if print_logs is True:
        logger.addHandler(logging.StreamHandler())

    return logger


class Constant:
    """
    Constant module includes predefined constants for the sports
    betting application.

    This module defines various constants used throughout the
    application for calculations, testing, and configuration.

    Constants:
    ----------
    1. TAX_VALUE (float): The default tax value for calculating
        returns on bets. Default is 0.12 (12%).
    2. TEST_STAKE (float): The default stake value used for
        testing purposes. Default is 100.00.
    3. TOTAL_MIN_RETURN (float): The minimum return value expected
        from a bet. Default is 0.00.
    4. CLUSTER_STRINGS_THRESHOLD (float): The threshold value for
        string clustering in the application.  It is used in the
        `cluster_strings` method. Default is 0.001.

    References:
    -----------
    - AgglomerativeClustering Documentation:
    https://scikit-learn.org/stable/modules/generated/sklearn.cluster.AgglomerativeClustering.html
    """
    TAX_VALUE = 0.12
    TEST_STAKE = 100.00
    TOTAL_MIN_RETURN = 0.00
    CLUSTER_STRINGS_THRESHOLDS = 0.001
    # https://scikit-learn.org/stable/modules/generated/sklearn.cluster.AgglomerativeClustering.html
