#!/usr/bin/env python3
"""Alx Backend User Data module"""
from typing import List
import re

def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str) -> str:
    """Obfuscates data on a log line by redaction"""
    # return re.sub(r'({})'.format(separator.join(fields)), redaction, message)
    for field in fields:
        message = re.sub(r'{}=(.*?){}'.format(field, separator),
                         '{}={}{}'.format(field, redaction, separator), message)
    return message
