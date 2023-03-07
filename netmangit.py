import os
import git

# Set the access token
access_token = "YOUR_ACCESS_TOKEN_HERE"

# Set the Git askpass helper environment variable to avoid being prompted for a password
os.environ["GIT_ASKPASS"] = "git_askpass_helper"

# Initialize a Git repository object
repo = git.Repo()

# Add all files in the current directory to the staging area
repo.git.add(".")

# Commit the changes with a message
commit_msg = "Update from Python script"
repo.git.commit("-m", commit_msg)

# Push the changes to the remote repository with the access token
remote_url = repo.remote().url
remote_url_with_token = remote_url.replace("://", "://{}@".format(access_token))
repo.git.push(remote_url_with_token)

# Compare modified files in the local repository against the GitHub repository and print the difference
def compare_files():
    remote = repo.remote()
    remote.fetch()
    local_diff = repo.git.diff("--name-only", "--diff-filter=M").splitlines()
    remote_diff = repo.git.diff("--name-only", "--diff-filter=M", "{}/HEAD".format(remote.name)).splitlines()
    print("Modified files in local repository but not in remote repository:")
    print(set(local_diff) - set(remote_diff))

compare_files()
