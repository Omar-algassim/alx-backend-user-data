#!/usr/bin/env python3
"""filter loggin module"""
import re
from typing import List
import logging

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """filter values in incoming log records using filter_datum"""
        meassage = super(RedactingFormatter, self).format(record)
        return filter_datum(self.fields,
                            self.REDACTION,
                            meassage,
                            self.SEPARATOR)


def get_logger() -> logging.Logger:
    """return the loggeer"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)

    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    """that returns the log message obfuscated"""
    for field in fields:
        message = (
            re.sub(f"(?P<field>{field}=)([^{'|'.join(separator)}$]*)",
                   r"\g<field>{}".format(redaction),
                   message))
    return message
