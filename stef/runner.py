import os
import shutil
from stef.logger import Logger

class Runner():
    def __init__(self, solution_base_dir, binary_name, skip_setup=False):
        self.prerequierments_run = False
        self.prepared = False
        self.solution_base_dir = solution_base_dir
        self.binary_name = binary_name
        self.skip_setup = skip_setup

    def get_bin_path(self):
        return self.binary_name
        if self.solution_base_dir.endswith("/"):
            return self.solution_base_dir + self.binary_name
        return self.solution_base_dir + "/" + self.binary_name

    def prerequierments(self):
        return True

    def copytree(self, src, dst, symlinks=False, ignore=None):
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, symlinks, ignore)
            else:
                shutil.copy2(s, d)

    # runs the makefile in the current directory, skips if no makefile is found
    def run_make_file(self):
        Logger.log("DEBUG", "running makefile")
        if not self.check_for_file("makefile"):
            Logger.log("STATUS", "No makefile found, skipping", "WARNING")
            return True
        returncode, output, stderr = self.run_command('make')
        if returncode != 0:
            Logger.log(
                "STATUS", "Prerequierments failed, non-zero exit code", "FAIL")
            if output is not None:
                Logger.log("INFO", "StdOut:")
                Logger.log("INFO", output, "STD_OUT")
            if stderr is not None:
                Logger.log("INFO", "StdErr:")
                Logger.log("INFO", stderr, "STD_OUT_ERR")
            return False
        else:
            Logger.log("STATUS", "Makefile ran successfully", "OK")
            return True
    
    def check_for_file(self, filename):
        items = os.listdir(self.solution_base_dir)
        for names in items:
            if names.lower() == filename:
                return True
        return False

    def setup(self):
        if self.skip_setup:
            Logger.log("STATUS", "skipping setup", "WARNING")
            return True
        Logger.log("DEBUG", "started setup")
        if not self.check_for_file("setup.sh"):
            Logger.log("STATUS", "No setup.sh found, skipping", "WARNING")
            return True
        returncode, output, stderr = self.run_command('./setup.sh')
        if returncode != 0:
            Logger.log(
                "STATUS", "Prerequierments failed, non-zero exit code", "FAIL")
            if output is not None:
                Logger.log("INFO", "StdOut:")
                Logger.log("INFO", output, "STD_OUT")
            if stderr is not None:
                Logger.log("INFO", "StdErr:")
                Logger.log("INFO", stderr, "STD_OUT_ERR")
            return False
        else:
            Logger.log("STATUS", "setup.sh ran successfully", "OK")
            return True

    def prepare(self):
        if not self.prepared:
            Logger.log("DEBUG", "started preparing")
            self.prepared = self.prerequierments() and self.setup() and self.run_make_file()
        return self.prepared

    def run(self, command_line_arg, input_array):
        if not self.prerequierments_run and not self.prerequierments():
            Logger.log("STATUS", "Prerequirements failed. The tests will not be executed and you will be awarded 0 points. Please make sure there is either no makefile or the make command terminates with a none-zero exitcode when calling it without any arguments in your basedirectory." ,"FAIL")
            return 1, "", ""
        return self._run(command_line_arg, input_array)

    def _run(self, command_line_arg, input_array):
        raise NotImplementedError()

        