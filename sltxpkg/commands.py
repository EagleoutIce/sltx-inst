import os  # list directory
import re
import shutil  # clean working dir
import sys
from concurrent import futures
from pathlib import Path

from importlib_resources import files

import sltxpkg.lithie.compile.cooker as cooker
from sltxpkg import dep, generate, util as su, config as sc, globals as sg
from sltxpkg.config import (assure_dirs, load_configuration,
                            load_dependencies_config, write_to_log)
from sltxpkg.dep import install_dependencies
from sltxpkg.globals import (C_CLEANUP, C_CREATE_DIRS, C_DOWNLOAD_DIR,
                             C_DRIVER_LOG, C_DRIVER_PATTERNS, C_DRIVERS,
                             C_RECURSIVE, C_TEX_HOME, C_USE_DOCKER,
                             C_WORKING_DIR, DEFAULT_CONFIG)
from sltxpkg.lithie import commands as lithiecmd

import sltxpkg.data

def cmd_auto_setup():
    sc.assure_dirs()
    cleanse_caches()

    if sg.args.auto_deps:
        dep_path = str(files(sltxpkg.data).joinpath('sltx-dep.yaml'))
        sg.dependencies = load_dependencies_config(
            dep_path, sg.dependencies)
        sg.args.dep = os.path.basename(dep_path)
        install_dependencies()

    # TODO: allow option to install local dependencies too using the shipped sltx-dep?
    lithiecmd._install(sg.configuration[sg.C_DOCKER_PROFILE])


def cmd_dependency():
    if sg.args.dep is None or sg.args.dep == "":
        print("You must supply a dependency 'file'.")
        exit(1)

    if sg.args.dep is not None:
        sg.dependencies = load_dependencies_config(
            sg.args.dep, sg.dependencies)

    assure_dirs()

    target = su.get_tex_home() if sg.args.local_path is None else sg.args.local_path
    install_dependencies(target=target)

def cmd_version():
    print("This is sltx, a simple latex helper-utility")
    print("Tex-Home", su.get_tex_home())
    print("Version:", su.get_version())


def cmd_docker():
    lithiecmd.install()


def cmd_raw_compile():
    cooker.cook()


def cmd_compile():
    if(sg.configuration[C_USE_DOCKER]):
        print("Using docker to compile")
        lithiecmd.compile()
    else:
        print("Docker was disabled, using local compilation.")
        cmd_raw_compile()


def cmd_gen_gha():
    generate.generate()


def should_be_excluded(file: str):
    if sg.args.exclude_patterns is None:
        return False

    for exclude_pattern in sg.args.exclude_patterns:
        if re.match(exclude_pattern, file):
            return True
    return False


def cleanse_caches():
    cache_dir = sg.configuration[sg.C_CACHE_DIR]
    if os.path.isdir(cache_dir):
        print("Cleaning all the caches... (" + cache_dir + ")")
        # avoids deleting the cache dir itself
        for root, dirs, files in os.walk(cache_dir):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                shutil.rmtree(os.path.join(root, name))
    else:
        print("No caches \"" + cache_dir + "\" were found. Skipping...")


def cmd_cleanse():
    sc.assure_dirs()
    # Delete all current log files
    # TODO: make this dry. avoid specifying the log files signature multiple times (see Recipe)
    print("Cleaning local logs...")
    clean_patterns = ['sltx-log-*.tar.gz', 'sltx-drivers.log']
    for clean_pattern in clean_patterns:
        for f in Path(".").glob(clean_pattern):
            if should_be_excluded(str(f)):
                print("File", f, "excluded.")
            else:
                f.unlink()
    if sg.args.cleanse_all:
        thome = su.get_tex_home()
        if os.path.isdir(thome):
            print("Cleaning sltx-texmf-tree... (" + thome + ")")
            shutil.rmtree(thome)
        else:
            print("The local sltx-texmf tree in \"" +
                  thome + "\" was not found. Skipping...")

    if sg.args.cleanse_all or sg.args.cleanse_cache:
        cleanse_caches()
