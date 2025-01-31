import os
import shutil

import yaml


def copy_and_replace_yaml(src, dst, replacements):
    shutil.copy(src, dst)
    with open(dst, 'r') as file:
        data = yaml.safe_load(file)
    for key, value in replacements.items():
        if key in data:
            data[key] = value
    with open(dst, 'w') as file:
        yaml.safe_dump(data, file)

def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
    else:
        print(f"The file {file_path} does not exist.")