import os
import subprocess


def create_branch_commit_push(repo_path, branch_name, commit_message):
    original_dir = os.getcwd()
    try:
        os.chdir(repo_path)

        subprocess.run(["git", "checkout", "-b", branch_name], check=True)
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        subprocess.run(["git", "push", "-u", "origin", branch_name], check=True)

        print(
            f"Branch '{branch_name}' created, changes committed, and pushed to origin."
        )
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
    finally:
        os.chdir(original_dir)
