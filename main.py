import os
import subprocess
import argparse
import multiprocessing
import pathlib
import re
import logging
import CPUTemp
import time
# import run_cmd


if os.name == 'nt':
    import wmi
else:
    import psutil

cpu = CPUTemp.CPUTemp()

logging.basicConfig(level=logging.INFO)
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
    return cpu.get_cpu_temp()


def get_all_files_with_extensions(list_ext=[], dir=""):
    files = []
    for (dirpath, dirnames, filenames) in os.walk(dir):
        for f in filenames:
            rel_dir = os.path.relpath(dirpath, dir)
            rel_file = os.path.join(rel_dir, f)
            _, file_ext = os.path.splitext(str(rel_file))
            if file_ext in list_ext:
                files.append(os.path.join(dirpath, f))
        if logging.getLogger().level != logging.DEBUG:
            for d in dirnames:
                # Make Sure all required directories are created, even if they exist
                pathlib.Path(args.output_dir, d).mkdir(
                    parents=True, exist_ok=True)
    # Changing the root of the files as the output dir

    return files


logging.info(args.input_dir)
logging.info(args.output_dir)


original_files = get_all_files_with_extensions(extensions, args.input_dir)
new_files = [pathlib.Path(args.output_dir, x) for x in original_files]

# Debug File Values
if logging.getLogger().level == logging.DEBUG:
    for fil in original_files:
        logging.debug(fil)

commands = []
if logging.getLogger().level != logging.DEBUG:
    for i, f in enumerate(original_files):
        origin = str(f)
        dest = str(new_files[i])
        process = subprocess.Popen(["handbrake", "-i", origin, "-o", dest])
        process.wait()
        if check_temp() > 70:
            time.sleep(70)

for cmd in commands:
    print(cmd)
    process = subprocess.Popen(cmd)
    process.wait()
