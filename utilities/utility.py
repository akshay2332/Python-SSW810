"""
Utility Package for common functionality
"""

import ntpath
import os


def file_reading_gen(path, fields, sep=',', header=False):
    """
    A generator function to read field-separated text files and yield a
    tuple with all of the values from a single line.
    """

    # implement your code here
    if path is None or path == "" or not os.path.exists(path):
        raise FileNotFoundError(f"File Not found in the path {path}")

    file_name = ntpath.basename(path)
    try:
        file_pointer = open(path, "r")
    except Exception:
        raise FileNotFoundError(f"File Not found in the  path {path}")
    else:
        line_count = 1
        with file_pointer:
            for line in file_pointer:

                if header:
                    # Do not read the current line but start reading for next line
                    header = False
                    line_count += 1
                    continue

                contents = line.split(sep)
                length_fields = len(contents)

                if length_fields != fields:
                    raise ValueError(
                        f"ValueError: ‘{file_name}’ has {length_fields} fields on line"
                        f" {line_count} but expected {fields}")

                line_count += 1
                yield tuple(content.strip() for content in contents)
