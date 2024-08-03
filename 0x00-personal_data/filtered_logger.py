#!/usr/bin/env python3
"""Alx Backend User Data module"""
import mysql.connector
from typing import List
import re
import logging
import logging
import csv
import os


def filter_datum(
        fields: List[str], redaction: str,
        message: str, separator: str) -> str:
    """Obfuscates data on a log line by redaction"""
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


PII_FIELDS = ('email', 'phone', 'ssn', 'password', 'name')


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


def get_db() -> csv.reader:
    """Returns a csv.reader object"""
    return csv.reader(open('db.csv', 'r'))


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Returns a connector to the database"""
    username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    database = os.getenv('PERSONAL_DATA_DB_NAME')

    connection = mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=database
    )

    return connection


def main():
    logger = get_logger()
    db_connection = get_db()
    cursor = db_connection.cursor()

    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]

    for data in rows:
        row_dict = {columns[i]: data[i] for i in range(len(data))}
        row_str = "; ".join(f"{key}={val}" for key, val in row_dict.items())
        filtered = filter_datum(
            PII_FIELDS, RedactingFormatter.REDACTION, row_str,
            RedactingFormatter.SEPARATOR,
        )
        logger.info(filtered)
    cursor.close()
    db_connection.close()


if __name__ == "__main__":
    main()
