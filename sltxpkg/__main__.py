import argparse
import os  # list directory
import shutil  # clean working dir
import sys  # cmd line args
from concurrent import futures

from sltxpkg import dep, generate, globals as sg
from sltxpkg.config import (assure_dirs, load_configuration,
                         load_dependencies_config, write_to_log)
from sltxpkg.dep import install_dependencies
from sltxpkg.globals import (C_AUTODETECT_DRIVERS, C_CLEANUP, C_CREATE_DIRS,
                          C_DRIVER_LOG, C_DRIVER_PATTERNS, C_DRIVERS,
                          C_TEX_HOME, C_WORKING_DIR, DEFAULT_CONFIG, C_RECURSIVE)


def valid_file(arg: str):
    if arg is None or arg.strip() == "":
        raise ValueError("arg vas none or empty")
    if not os.path.isfile(arg):
        raise FileNotFoundError("\"" + arg + "\" must be an existing file")
    return arg


parser = argparse.ArgumentParser(
    description="sltx, a Simple LaTeX-INSTaller utility", prog="sltx")
parser.add_argument('-g', '--generate', dest='gen', action='store_true',
                    help="generate a github action file for automated installation.")
parser.add_argument('-c', '--config', dest='config', metavar='config.yml',
                    required=False, type=valid_file,
                    help="the file to load the configuration from.")
parser.add_argument('-d', '--dependencies', dest='dep', metavar='dep.yml',
                    required=False, type=valid_file,
                    help="the file to load the dependencies from.")
parser.add_argument('-t', '--threads', metavar='N', dest='threads', type=int,
                    help="number of threads to run the installation. Default is 1.",
                    default=1)

if(len(sys.argv) <= 1):
    parser.parse_args(['-h'])

sg.args = parser.parse_args()

if sg.args.gen:
    generate.generate()
    exit(0)

# TODO: if no deps or no generate call
if os.path.isfile(DEFAULT_CONFIG):
    print("Automatically loading '{DEFAULT_CONFIG}'".format(**locals()))
    load_configuration(DEFAULT_CONFIG)


if sg.args.config is not None:
    load_configuration(sg.args.config)
if sg.args.dep is not None:
    sg.dependencies = load_dependencies_config(sg.args.dep, sg.dependencies)

assure_dirs()

if "target" not in sg.dependencies or "dependencies" not in sg.dependencies:
    print("The dependency-file must supply a 'target' and an 'dependencies' key!")
    sys.exit(1)

write_to_log("====Dependencies for:" + sg.dependencies["target"]+"\n")
print()
print("Dependencies for:", sg.dependencies["target"])
print("Installing to:", sg.configuration[C_TEX_HOME])
print()

install_dependencies(0, sg.dependencies, first=True)

# all installed
if sg.configuration[C_CLEANUP]:
    print("> Cleaning up the working directory, as set.")
    shutil.rmtree(sg.configuration[C_WORKING_DIR])
print("Loaded:", dep.loaded)
if not sg.configuration[C_RECURSIVE]:
    print("Recursion was disabled.")
print("Dependency installation for",
      sg.dependencies["target"], "completed.")