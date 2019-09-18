"""Copyright since 2019, EPAM Systems

   This file is part of OSCI.

   OSCI is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   OSCI is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with OSCI.  If not, see <http://www.gnu.org/licenses/>."""


import gzip
import json
import os


def unpack_file(file_path):
    """
    unpacks json file from *.gz archive
    :param file_path: path to file
    """
    if file_path.endswith("gz"):
        with gzip.GzipFile(file_path, "rb") as f_in, \
                open(file_path.strip('.gz'), "wb") as f_out:
            f_out.write(f_in.read())
        os.remove(file_path)
    else:
        raise FileNotFoundError


def format_json_file(file_path, clear_src=False):
    """
    transforms the content from the file
    :param clear_src: set True if required to delete all src files after formatting
    :param file_path: path to the file
    """
    lines = []
    with open(file_path, encoding='utf-8') as infile:
        for line in infile:
            lines.append(json.loads(line))
    with open(file_path.strip('.json') + '-formatted.json', 'w') as outfile:
        json.dump(lines, outfile)
    if clear_src is True:
        os.remove(file_path)


def clear_directory(directory):
    """
    clears up the folder
    :param directory: path to the directory
    """
    files = os.listdir(directory)
    for file in files:
        os.remove(os.path.join(directory, file))
    os.rmdir(directory)
