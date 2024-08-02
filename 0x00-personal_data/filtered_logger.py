#!/usr/bin/env python3
"""Alx Backend User Data module"""
from typing import List
import re
import logging
import logging
import csv


def filter_datum(
        fields: List[str], redaction: str,
        message: str, separator: str) -> str:
    """Obfuscates data on a log line by redaction"""
    # return re.sub(r'({})'.format(separator.join(fields)), redaction, message)
    for field in fields:
        message = re.sub(
            r'{}=(.*?){}'.format(field, separator),
            '{}={}{}'.format(field, redaction, separator), message)
    return message


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """The constructor of the RedactingFormatter class"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Filters values in incoming log records"""
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


PII_FIELDS = ('email', 'phone', 'ssn', 'password', 'ip')


def get_logger() -> logging.Logger:
    """Returns a logging.Logger object"""
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False

    formatter = RedactingFormatter(PII_FIELDS)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    return logger
