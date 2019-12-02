import os
import sys
import argparse
import pathlib
import re
parser = argparse.ArgumentParser()
parser.add_argument("--input_dir","-i",help="Input directory's name")
parser.add_argument("--output_dir","-o",help="Output directory's name")
extensions=["*.avi","*.mp4",".mkv","m4v"]
args = parser.parse_args()

def get_all_files_extensions(list_ext=[], dir=""):
    files=[]
    for (dirpath,dirnames,filenames) in os.walk(dir):
        for f in filenames:
            rel_dir = os.path.relpath(dirpath, dir)
            rel_file = os.path.join(rel_dir, f)
            if fext in list_ext:
                files.append(rel_file)
    return files

print(get_all_files_extensions(extensions,args.input_dir))

