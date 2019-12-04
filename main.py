import os
import subprocess
import argparse
import multiprocessing
import pathlib
import re
import logging
import CPUTemp
import time
import pickle
# import run_cmd

files_done={}
if os.name == 'nt':
    import clr
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
                files.append(rel_file)
        structure = os.path.join(
            args.output_dir, dirpath[len(args.input_dir):])
        if not os.path.isdir(structure):
            os.mkdir(structure)
        else:
            print("Folder does already exits!")
    # Changing the root of the files as the output dir

    return files


logging.info(args.input_dir)
logging.info(args.output_dir)

files_done[args.input_dir]=[]

files = get_all_files_with_extensions(extensions, args.input_dir)
original_files = [pathlib.Path(args.input_dir, x) for x in files]
new_files = [pathlib.Path(args.output_dir, x) for x in files]

logging.info(original_files[0])
logging.info(new_files[0])

commands = []
for i, f in enumerate(original_files):
    origin = str(f)
    dest = str(new_files[i])
    process = subprocess.Popen(["handbrake", "-i",origin,"-o",dest])
    process.wait()
    if check_temp() > 70:
        time.sleep(70)

for cmd in commands:
    print(cmd)
    process = subprocess.Popen(cmd)
    process.wait()


pickle.dumps(files_done,)