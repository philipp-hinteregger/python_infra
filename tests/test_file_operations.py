import os
import shutil
import unittest

import yaml

from file_operations.file_operations import (
    copy_and_replace_yaml,
    delete_file,
    copy_all_files,
)


class TestFileOperations(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for testing
        self.test_dir = "test_dir"
        os.makedirs(self.test_dir, exist_ok=True)

        # Create a sample YAML file
        self.src_file = os.path.join(self.test_dir, "test.yaml")
        with open(self.src_file, "w") as file:
            yaml.dump({"key1": "value1", "key2": "value2"}, file)

        self.dst_file = os.path.join(self.test_dir, "test_copy.yaml")

        with open(os.path.join(self.test_dir, "file1.tf"), "w") as f:
            f.write("This is file 1.")
        with open(os.path.join(self.test_dir, "file2.tf"), "w") as f:
            f.write("This is file 2.")

        # Create a temporary target directory
        self.target_dir = "temp_target"
        os.makedirs(self.target_dir, exist_ok=True)

    def tearDown(self):
        # Remove the temporary directory after tests
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
        # Create a file to delete
        file_to_delete = os.path.join(self.test_dir, "delete_me.yaml")
        with open(file_to_delete, "w") as file:
            file.write("delete me")

        # Ensure the file exists
        self.assertTrue(os.path.exists(file_to_delete))

        # Delete the file
        delete_file(file_to_delete)

        # Ensure the file is deleted
        self.assertFalse(os.path.exists(file_to_delete))

    def test_copy_files(self):
        # Call the copy_files function
        copy_all_files(self.test_dir, self.target_dir)

        # Check if files are copied correctly
        self.assertTrue(os.path.exists(os.path.join(self.target_dir, "file1.tf")))
        self.assertTrue(os.path.exists(os.path.join(self.target_dir, "file2.tf")))

        with open(os.path.join(self.target_dir, "file1.tf"), "r") as f:
            self.assertEqual(f.read(), "This is file 1.")

        with open(os.path.join(self.target_dir, "file2.tf"), "r") as f:
            self.assertEqual(f.read(), "This is file 2.")


if __name__ == "__main__":
    unittest.main()
