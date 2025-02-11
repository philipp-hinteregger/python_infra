import unittest
from unittest.mock import MagicMock, patch

from git_operations.git import git_commit_and_push


class TestGitCommitAndPush(unittest.TestCase):

    @patch("git.Repo")
    def test_git_commit_and_push(self, mock_repo):
        mock_repo_instance = MagicMock()
        mock_branch = MagicMock()
        mock_remote = MagicMock()

        mock_repo.return_value = mock_repo_instance
        mock_repo_instance.create_head.return_value = mock_branch
        mock_repo_instance.remote.return_value = mock_remote

        repo_path = "/path/to/random/repo"
        commit_message = "Test commit message"
        branch_name = "test-branch"

        git_commit_and_push(repo_path, branch_name, commit_message)

        mock_repo.assert_called_once_with(repo_path)
        mock_repo_instance.create_head.assert_called_once_with(branch_name)
        mock_branch.checkout.assert_called_once()
        mock_repo_instance.git.add.assert_called_once_with(A=True)
        mock_repo_instance.index.commit.assert_called_once_with(commit_message)
        mock_repo_instance.remote.assert_called_once_with(name="origin")
        mock_remote.push.assert_called_once_with(refspec=f"{branch_name}:{branch_name}")


if __name__ == "__main__":
    unittest.main()
