import os
import shutil
import subprocess
import unittest
from unittest.mock import patch

from git_operations.git_operations import create_branch_commit_push


class TestGitOperations(unittest.TestCase):
    def setUp(self):
        self.repo_path = "./temp_git_repo"
        os.makedirs(self.repo_path, exist_ok=True)

        subprocess.run(["git", "init"], cwd=self.repo_path, check=True)

        with open(os.path.join(self.repo_path, "temp_file.txt"), "w") as f:
            f.write("Temporary file content.")

    def tearDown(self):
        shutil.rmtree(self.repo_path)

    @patch("subprocess.run")
    def test_create_branch_commit_push(self, mock_subprocess_run):
        branch_name = "test-branch"
        commit_message = "Test commit"

        create_branch_commit_push(self.repo_path, branch_name, commit_message)

        mock_subprocess_run.assert_any_call(
            ["git", "checkout", "-b", branch_name], check=True
        )
        mock_subprocess_run.assert_any_call(["git", "add", "."], check=True)
        mock_subprocess_run.assert_any_call(
            ["git", "commit", "-m", commit_message], check=True
        )
        mock_subprocess_run.assert_any_call(
            ["git", "push", "-u", "origin", branch_name], check=True
        )


if __name__ == "__main__":
    unittest.main()
