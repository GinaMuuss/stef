import os
import subprocess
from stef.runner import Runner
from stef.logger import Logger


class BashRunner(Runner):
    def __init__(self, solution_base_dir, binary_name, skip_setup=True):
        super().__init__(solution_base_dir, binary_name, skip_setup=skip_setup)

    # guarantees some prerequirements
    # can be overriden, should return 1 if the setup failed
    def prerequirements(self):
        self.prerequirements_run = True
        return True

    def run_command(self, command, workdir=None):
        if workdir is None:
            workdir = self.solution_base_dir
        proc = subprocess.Popen([command], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=workdir)
        outs, errs = proc.communicate()
        output = outs.decode("utf-8")
        stderr = errs.decode("utf-8")
        return proc.returncode, output, stderr

    def _run(self, command_line_arg, input_array):
        inp = "\n".join([" ".join(y) for y in input_array])
        proc = subprocess.Popen(["bash", self.get_bin_path()] + command_line_arg,
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                cwd=self.solution_base_dir)
        outs, errs = proc.communicate(inp.encode('utf-8'))
        output = outs.decode("utf-8")
        stderr = errs.decode("utf-8")
        return proc.returncode, output, stderr
