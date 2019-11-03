import json
import os


class Utils(object):

    @staticmethod
    def write_env_file(envs, file_path):
        file_dir = os.path.dirname(file_path)
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        with open(file_path, "w") as f:
            for key, value in envs.items():
                f.write("export {}={}\n".format(key, value))
        return True

    @staticmethod
    def write_yaml_file(data, file_path):
        file_dir = os.path.dirname(file_path)
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        with open(file_path, "w") as f:
            f.write(json.dumps(data) + '\n')
        return True
