import os
import shutil
import unittest

import yaml

from file_operations.file_operations import (
    copy_all_files,
    copy_and_replace_yaml,
    delete_file,
)


class TestFileOperations(unittest.TestCase):

    def setUp(self):
        self.test_dir = "test_dir"
        self.target_dir = "temp_target"
        os.makedirs(self.test_dir, exist_ok=True)
        os.makedirs(self.target_dir, exist_ok=True)

        self.src_file = os.path.join(self.test_dir, "test.yaml")
        self.dst_file = os.path.join(self.test_dir, "test_copy.yaml")

        with open(self.src_file, "w") as file:
            yaml.dump({"key1": "value1", "key2": "value2"}, file)

        with open(os.path.join(self.test_dir, "file1.tf"), "w") as f:
            f.write("This is file 1.")
        with open(os.path.join(self.test_dir, "file2.tf"), "w") as f:
            f.write("This is file 2.")

    def tearDown(self):
        shutil.rmtree(self.test_dir)
        shutil.rmtree(self.target_dir)

    def test_copy_and_replace_yaml(self):
        replacements = {"key1": "new_value1", "key2": "new_value2"}
        copy_and_replace_yaml(self.src_file, self.dst_file, replacements)

        with open(self.dst_file, "r") as file:
            data = yaml.safe_load(file)

        self.assertEqual(data["key1"], "new_value1")
        self.assertEqual(data["key2"], "new_value2")

    def test_delete_file(self):
        file_to_delete = os.path.join(self.test_dir, "delete_me.yaml")
        with open(file_to_delete, "w") as file:
            file.write("delete me")

        self.assertTrue(os.path.exists(file_to_delete))

        delete_file(file_to_delete)

        self.assertFalse(os.path.exists(file_to_delete))

    def test_copy_files(self):
        copy_all_files(self.test_dir, self.target_dir)

        self.assertTrue(os.path.exists(os.path.join(self.target_dir, "file1.tf")))
        self.assertTrue(os.path.exists(os.path.join(self.target_dir, "file2.tf")))

        with open(os.path.join(self.target_dir, "file1.tf"), "r") as f:
            self.assertEqual(f.read(), "This is file 1.")

        with open(os.path.join(self.target_dir, "file2.tf"), "r") as f:
            self.assertEqual(f.read(), "This is file 2.")


if __name__ == "__main__":
    unittest.main()
