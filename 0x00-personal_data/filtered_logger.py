#!usr/bin/env python3
"""filter loggin module"""
import re
from typing import List


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
