# Copyright (c) 2019 Leiden University Medical Center
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
Contains general functions that are not specific to biowdl_input_converter.
"""

import csv
from pathlib import Path
from typing import Dict, Generator


def csv_to_dict_generator(csv_file: Path) -> Generator[Dict[str, str], None, None]:  # noqa: E501
    """
    Converts a csv_file into a generator. The generator yields each row
    (except the header) as a dictionary. {header_column1: value,
    header_column2: value etc.}
    :param csv_file: A pathlib.Path pointing to the csv file.
    :return: a generator that yields rows as Dict[str,str].
    """
    with csv_file.open("r") as csvfile:
        dialect = csv.Sniffer().sniff("".join(
            [csvfile.readline() for _ in range(10)]), delimiters=";,\t")
        csvfile.seek(0)
        reader = csv.reader(csvfile, dialect)
        try:
            header = next(reader)
        # A proper generator never raises a stop iteration. Instead it returns.
        except StopIteration:
            return
        for row in reader:
            row_dict = {heading: row[index]
                        for index, heading in enumerate(header)}
            yield row_dict
