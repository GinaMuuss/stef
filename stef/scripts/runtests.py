import argparse
import importlib.util
import os
from stef.base import TestType
from stef.bashrunner import BashRunner
from stef.dockerrunner import DockerRunner

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('directory_to_test', type=str, help='the directory with the code to test')
    parser.add_argument('directory_to_load_tests_from', type=str, help='the directory to load the tests from')
    parser.add_argument('--solutionbinary', type=str, help='the solution binary in the solutionpath', default="run.sh")
    parser.add_argument('--runner', type=str, help='the runnertype to use', default="bash")
    parser.add_argument('--testgroups', type=str, help='only run the selected testgroups, comma seperated')
    parser.add_argument('--skip_testgroups', type=str, help='don\'t run the selected testgroups, comma seperated')

    args = parser.parse_args()
    
    testpath = args.directory_to_load_tests_from
    print("Running tests in folder: ", testpath)
    spec = importlib.util.spec_from_file_location("currenttest", testpath + "/test.py")
    test = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(test)

    print("Testing solution at: ", args.directory_to_test)

    if args.runner == "bash":
        runner = BashRunner(args.directory_to_test, args.solutionbinary)
    elif args.runner == "docker":
        runner = DockerRunner(args.directory_to_test, args.solutionbinary)
    else:
        raise Exception("Unsupported runner ", args.runner)

    testgroups, skip_testgroups = None, None
    if args.testgroups != None and args.testgroups != "":
        testgroups = args.testgroups.split(",")
    if args.skip_testgroups != None and args.skip_testgroups != "":
        skip_testgroups = args.skip_testgroups.split(",")

    thistest = test.Test()
    thistest.set_testgroups_to_runskip(testgroups, skip_testgroups)

    thistest.run(runner)

if __name__ == "__main__":
    main()