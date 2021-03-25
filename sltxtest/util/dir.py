import os
import tempfile
import unittest


def retrieve_tmpdir():
    return tempfile.mkdtemp('sltxxtest')


def assert_dir_files(test: unittest.TestCase, directory: str, contents: dict) -> None:
    """
    Will check if directory contains all the given files with the given content
    Args:
        test (unittest.TestCase): The testcase to use
        directory (str): given directory to check
        contents (dict): mapping 'filename -> content'

    Returns:
        flag indicating all files are as expected
    """
    for file, content in contents.items():
        current_file = os.path.join(directory, file)
        test.assertTrue(os.path.isfile(current_file), 'File: "' + file + '" is expected to exist (' + directory + ")")
        with open(current_file, mode='r') as f:
            test.assertListEqual(f.readlines(), content)
