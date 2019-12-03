import os
import subprocess
import argparse
import multiprocessing
import pathlib
import re
import logging
import CPUTemp
import time
if os.name == 'nt':
    import wmi
else:
    import psutil

cpu = CPUTemp.CPUTemp()

logging.basicConfig(level=logging.DEBUG)
parser = argparse.ArgumentParser()
parser.add_argument("--input_dir", "-i", required=True,
                    help="Input directory's name")
parser.add_argument("--output_dir", "-o", required=True,
                    help="Output directory's name")
extensions = [".avi", ".mp4", ".mkv", ".m4v"]
args = parser.parse_args()


def work(cmd):
    return subprocess.call(cmd, shell=False)


def check_temp():
    if cpu.get_cpu_temp() > 65:
        time.sleep(10)


def get_all_files_with_extensions(list_ext=[], dir=""):
    files = []
    for (dirpath, dirnames, filenames) in os.walk(dir):
        for f in filenames:
            rel_dir = os.path.relpath(dirpath, dir)
            rel_file = os.path.join(rel_dir, f)
            _, file_ext = os.path.splitext(str(rel_file))
            if file_ext in list_ext:
                files.append(rel_file)
        for d in dirnames:
            # Make Sure all required directories are created, even if they exist
            pathlib.Path(args.output_dir, d).mkdir(parents=True, exist_ok=True)
    # Changing the root of the files as the output dir

    return files


logging.info(args.input_dir)
logging.info(args.output_dir)


original_files = get_all_files_with_extensions(extensions, args.input_dir)
new_files = [pathlib.Path(args.output_dir, x) for x in files]

# Debug File Values
if logging.getLevelName == logging.DEBUG:
    for fil in files:
        logging.debug(fil)

for i, f in enumerate(original_files):
    subprocess.call(["handbrake", "-i", f, "-o", new_files[i]])
    if check_temp() > 70:
        time.sleep(70)
