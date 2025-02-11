import git


def git_commit_and_push(repo_path, branch_name, commit_message):
    try:
        repo = git.Repo(repo_path)
        new_branch = repo.create_head(branch_name)
        new_branch.checkout()
        repo.git.add(A=True)
        repo.index.commit(commit_message)
        origin = repo.remote(name="origin")
        origin.push(refspec=f'{branch_name}:{branch_name}')

        print("Changes committed and pushed successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
