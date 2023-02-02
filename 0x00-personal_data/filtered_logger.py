#!/usr/bin/env python3
"""
Module to obfuscate logs to protect person data
"""


import mysql.connector
import logging
import os
import re
from typing import List


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """Function to obfuscate logs"""
    for field in fields:
        pat = field + '=[^{}]*'.format(separator)
        message = re.sub(pat, field + '=' + redaction, message)
    return message


def get_logger() -> logging.Logger:
    """Function to get a logger"""

    logging.Logger(name='user_data').setLevel(logging.INFO)
    user_data = logging.getLogger('user_data')
    user_data.propagate = False
    formatter = RedactingFormatter(PII_FIELDS)
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    user_data.addHandler(handler)
    return user_data


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Get a conector object to a database"""
    db = mysql.connector.connect(
        host=os.getenv("PERSONAL_DATA_DB_HOST"),
        user=os.getenv("PERSONAL_DATA_DB_USERNAME"),
        password=os.getenv("PERSONAL_DATA_DB_PASSWORD"),
        database=os.getenv("PERSONAL_DATA_DB_NAME")
    )
    return db


def main():
    """Main function that retrieve logs from a database"""

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    titles = [title[0] for title in cursor.description]
    for row in cursor:
        msg = ''
        for title, row_info in zip(titles, row):
            msg += "{}={};".format(title, row_info)
        record = logging.LogRecord("user_data", logging.INFO, None, None,
                                   msg, None, None)
        formatter = RedactingFormatter(titles)
        print(formatter.format(record))
    cursor.close()
    db.close()


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Constructor mmethod for class"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Format output for logging"""
        formatter = logging.Formatter(self.FORMAT)
        record.msg = filter_datum(list(self.fields), '***', record.msg, ';')
        return formatter.format(record)


if __name__ == "__main__":
    main()
