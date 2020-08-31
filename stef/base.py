from enum import Enum
from stef.logger import Logger

class TestType(Enum):
    hidden = "hidden"
    shown = "shown"

    def __str__(self):
        return self.value

class TestBase():
    def __init__(self, testname, testtype, testgroups_to_run=None, testgroups_to_skip=None):
        self.testname = testname
        self.current_test_num = 0
        self.points = {}
        self.max_points = {}
        self.testgroups = []
        self.solution_pre_string = "SOLUTION"
        if not isinstance(testtype, TestType):
            raise Exception("Not a testtype")
        self.testtype = testtype
        self.testgroups_to_run = testgroups_to_run
        self.testgroups_to_skip = testgroups_to_skip

    def set_testgroups_to_runskip(self, testgroups_to_run=None, testgroups_to_skip=None):
        self.testgroups_to_run = testgroups_to_run
        self.testgroups_to_skip = testgroups_to_skip

    def parseOutput(self, string):
        actual_out = [x for x in string.split("\n")]
        output = []
        for line in actual_out:
            splitline = line.partition(":")
            if splitline[2] == None or splitline[2] == "":
                output.append(["UNKNOWN", splitline[0]])
            else:
                output.append([splitline[0].strip(), splitline[2].strip()])
        return output

    def getSolution(self, output):
        solution = list(filter(lambda x: x[0] == self.solution_pre_string, output))
        solution = list(map(lambda x: x[1].split(" "), solution))
        return solution

    def start_tests(self):
        Logger.log("INFO", "Started Tests: '" + self.testname + "'")

    def next_test(self):
        Logger.log("INFO", "Running test: #" + str(self.current_test_num), "NEW_TEST")
        self.current_test_num += 1
        
    def test(self, command_line_arg, input_array, expected_output, points):
        self.current_max_points += points
        success = self._run_tests_with_runner(command_line_arg, input_array, expected_output)
        if success:
            self.current_points += points
            Logger.log_points(points, points)
        else:
            Logger.log_points(0, points)

    # input_array and expected_output should be a twodimensional arrays, where the inner arrays each represent a line.
    # The values of the inner array will be sperated by spaces
    # will run the given binary with bash as some none root user
    def _run_tests_with_runner(self, command_line_arg, input_array, expected_output):
        self.next_test()

        returncode, output, stderr = self.runner.run(command_line_arg, input_array)

        actual_out = self.parseOutput(output)
        solution = self.getSolution(actual_out)

        if returncode != 0:
            Logger.log("STATUS", "Test failed, non-zero exit code", "FAIL")
            if stderr is not None:
                Logger.log("INFO", "StdErr:")
                Logger.log("INFO", stderr)
            if output is not None:
                Logger.log("INFO", "StdOut:")
                Logger.log("INFO", output)
            return False
        if solution != expected_output:
            Logger.log("STATUS", "Test failed", "FAIL")
            Logger.log("INFO", "command line arg: " + " ".join(command_line_arg))
            Logger.log("INFO", "input:")
            for line in input_array:
                Logger.log("INFO", " ".join(line))
            Logger.log("INFO", "expected output:")
            for line in expected_output:
                Logger.log("INFO", " ".join(line))
            Logger.log("INFO", "parsed solution output:")
            for line in solution:
                Logger.log("INFO", " ".join(line))
            if output is not None and output != "":
                Logger.log("DEBUG", "Full output trace stdout:")
                Logger.log("DEBUG", output, "SUB_OUT")
            else:
                Logger.log("DEBUG", "Stdout was empty")
            if stderr is not None and stderr != "":
                Logger.log("DEBUG", "Full output trace stderr:")
                Logger.log("DEBUG", stderr, "SUB_OUT_ERR")
            else:
                Logger.log("DEBUG", "Stderr was empty")
            return False
        else:
            Logger.log("STATUS", "Test sucessfull", "OK")
            return True

    def reset_points(self):
        self.current_points = 0
        self.current_max_points = 0

    # Method will call all the defined test groups
    # will be called by the run method
    def run_all_testgroups(self):
        self.start_tests()
        for testgroup in self.testgroups:
            Logger.log("INFO", "Running testgroup: " + testgroup["name"])
            self.reset_points()
            testgroup["function"]()
            if testgroup["point_id"] not in self.points:
                self.points[testgroup["point_id"]] = 0
            self.points[testgroup["point_id"]]  += self.current_points

            if testgroup["point_id"] not in self.max_points:
                self.max_points[testgroup["point_id"]] = 0
            self.max_points[testgroup["point_id"]]  += self.current_max_points

            Logger.log("POINTS", "Testgroup points:" ,"POINTS")
            Logger.log_points(self.current_points, self.current_max_points)

    

    def evaluate(self):
        Logger.log("POINTS", "==========Test evaluation==========", "POINTS")
        sumpoint = 0
        summaxpoint = 0
        for i in self.points:
            Logger.log("POINTS", "Points for testgroup: '" + i + "'", "POINTS")
            Logger.log_points(self.points[i], self.max_points[i])
            sumpoint += self.points[i]
            summaxpoint += self.max_points[i]
        Logger.log("POINTS", "Overall result:", "POINTS")
        Logger.log_points(sumpoint, summaxpoint)
        if sumpoint == summaxpoint:
            Logger.log("INFO", "Well done!", "PRAISE")

    def run(self, runner):
        if self.testgroups_to_run != None:
            self.testgroups = filter(lambda x: x["name"] in self.testgroups_to_run, self.testgroups)

        if self.testgroups_to_skip != None:
            self.testgroups = filter(lambda x: x["name"] not in self.testgroups_to_skip, self.testgroups)

        self.runner = runner
        if self.runner.prepare():
            self.run_all_testgroups()
            self.evaluate()