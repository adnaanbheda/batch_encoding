import os
import sys
import argparse
import pathlib
import re
import logging

logging.basicConfig(level=logging.DEBUG)
parser = argparse.ArgumentParser()
parser.add_argument("--input_dir", "-i", required=True,
                    help="Input directory's name")
parser.add_argument("--output_dir", "-o", required=True,
                    help="Output directory's name")
extensions = [".avi", ".mp4", ".mkv", ".m4v"]
args = parser.parse_args()


def get_all_files_with_extensions(list_ext=[], dir=""):
    files = []
    for (dirpath, dirnames, filenames) in os.walk(dir):
        for f in filenames:
            rel_dir = os.path.relpath(dirpath, dir)
            rel_file = os.path.join(rel_dir, f)
            _, file_ext = os.path.splitext(str(rel_file))
            if file_ext in list_ext:
                files.append(rel_file)
    return files


logging.info(args.input_dir)
logging.info(args.output_dir)
files = get_all_files_with_extensions(extensions, args.input_dir)
logging.debug(files[0])
files = [pathlib.Path(args.output_dir, x) for x in files]
logging.debug(files[0])
for fil in files:
    logging.debug(fil)
