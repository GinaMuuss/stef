#!/usr/bin/env python3

import os, os.path
import sys
import argparse
import importlib.util
from stef.logger import Logger
from stef.bashrunner import BashRunner
from stef.dockerrunner import DockerRunner


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('codedir', type=str, help='the directory with the code to test')
    parser.add_argument('testdir', type=str, help='the directory to load the tests from')
    parser.add_argument('--solutionbinary', type=str, help='the solution binary filename in the codedir', default="run.sh")
    parser.add_argument('--testfile', type=str, help='the filename containing the python code for the tests', default="test.py")
    parser.add_argument('--runner', type=str, help='the runnertype to use', default="bash")
    parser.add_argument('--testgroups', type=str, help='only run the selected testgroups, comma separated')
    parser.add_argument('--skip_testgroups', type=str, help="don't run the selected testgroups, comma separated")

    args = parser.parse_args()

    print(f"Testing solution at: {args.codedir}")
    codefile = os.path.join(args.codedir, args.solutionbinary)
    if not os.path.isfile(codefile):
        Logger.log("FATAL", "Solution binary not found, quitting", "FAIL")
        sys.exit(1)

    print(f"Running tests from folder: {args.testdir}")
    testfile = os.path.join(args.testdir, args.testfile)
    if not os.path.isfile(testfile):
        Logger.log("FATAL", "Test file not found, quitting", "FAIL")
        sys.exit(1)
    spec = importlib.util.spec_from_file_location("currenttest", testfile)
    test = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(test)

    if args.runner == "bash":
        runner = BashRunner(args.codedir, args.solutionbinary)
    elif args.runner == "docker":
        runner = DockerRunner(args.codedir, args.solutionbinary)
    else:
        raise Exception(f"Unsupported runner: {args.runner}")

    testgroups, skip_testgroups = None, None
    if args.testgroups is not None and args.testgroups != "":
        testgroups = args.testgroups.split(",")
    if args.skip_testgroups is not None and args.skip_testgroups != "":
        skip_testgroups = args.skip_testgroups.split(",")

    thistest = test.Test()
    thistest.set_testgroups_to_runskip(testgroups, skip_testgroups)

    thistest.run(runner)


if __name__ == "__main__":
    main()
