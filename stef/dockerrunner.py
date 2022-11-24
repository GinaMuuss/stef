import tempfile
import docker
import os
import shutil
from stef.runner import Runner
from stef.logger import Logger


class DockerRunner(Runner):
    def __init__(self, solution_base_dir, binary_name, skip_setup=False):
        super().__init__(solution_base_dir, binary_name, skip_setup=skip_setup)
        self.image_name = "testframework_test"
        self.build_path = tempfile.mkdtemp()
        print(f"Docker build path: {self.build_path}")
        self.docker_client = docker.from_env()

    # guarantees some prerequirements
    # can be overriden, should return 1 if the setup failed
    def prerequirements(self):
        Logger.log("DEBUG", "Starting prerequirements")
        self.prerequirements_run = self.build_docker_image()
        Logger.log("DEBUG", "prerequirements finished")
        return self.prerequirements_run

    def build_docker_image(self):
        Logger.log("DEBUG", "moving files into place")
        shutil.copyfile(os.path.join(os.path.abspath(os.path.dirname(__file__)), "Dockerfile"), self.build_path + "/Dockerfile")
        self.copytree(self.solution_base_dir, self.build_path)
        Logger.log("DEBUG", "building docker image")
        self.docker_image, _ = self.docker_client.images.build(path=self.build_path, tag=self.image_name)
        Logger.log("DEBUG", f"creating docker container from image {self.docker_image.short_id}")
        self.docker_container = self.docker_client.containers.create(self.docker_image, command='sleep 100000', detach=True)
        Logger.log("DEBUG", f"starting docker container {self.docker_container.short_id}")
        if self.docker_container is None:
            return False
        self.docker_container.start()
        return True

    def run_command(self, command, workdir="/evaluation/solution/"):
        returncode, (outs, errs) = self.docker_container.exec_run(command, stderr=True, stdout=True, workdir=workdir, demux=True)
        output = outs.decode("utf-8") if outs is not None else ""
        stderr = errs.decode("utf-8") if errs is not None else ""
        return returncode, output, stderr

    def _run(self, command_line_arg, input_array):
        inp = "\n".join([" ".join(y) for y in input_array])
        command_line_arg_str = " ".join(command_line_arg)
        returncode, outs, errs = self.run_command(['sh', '-c', f'echo {inp} | ./run.sh {command_line_arg_str}'])
        return returncode, outs, errs
