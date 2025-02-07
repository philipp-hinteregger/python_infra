import os
import shutil

import yaml


def copy_and_replace_yaml(src, dst, replacements):
    shutil.copy(src, dst)
    with open(dst, "r") as file:
        data = yaml.safe_load(file)
    for key, value in replacements.items():
        if key in data:
            data[key] = value
    with open(dst, "w") as file:
        yaml.safe_dump(data, file)


def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
    else:
        print(f"The file {file_path} does not exist.")


def copy_all_files(source_dir, target_dir):
    if not os.path.exists(source_dir):
        print(f"Source directory {source_dir} does not exist.")
        return

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    for filename in os.listdir(source_dir):
        print(f"Copying file {filename}...")
        source_file = os.path.join(source_dir, filename)
        target_file = os.path.join(target_dir, filename)
        shutil.copy(source_file, target_file)

    print(f"All files from {source_dir} have been copied to {target_dir}.")
