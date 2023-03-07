import git

# Set the token secret and GitHub repository URL
token_secret = "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"
github_repo_url = "https://github.com/prathz111/NetmanLab5"

# Initialize a Git repository object
repo = git.Repo()

def add_and_commit_changes(commit_msg):
    # Add all files in the current directory to the staging area
    repo.git.add(".")
    # Commit the changes with a message
    repo.git.commit("-m", commit_msg)

def push_changes():
    # Push the changes to the remote repository with the token secret
    remote_url = repo.remote().url
    remote_url_with_secret = remote_url.replace("://", "://{}@".format(token_secret))
    repo.git.push(remote_url_with_secret)

def compare_and_push_changes():
    # Fetch the latest changes from the remote repository
    repo.remotes.origin.fetch()
    # Compare modified files in the local repository against the GitHub repository and print the difference
    local_changes = set([item.a_path for item in repo.index.diff(None)])
    remote_changes = set([item.a_path for item in repo.index.diff("origin/{}".format(repo.active_branch.name))])
    changes_to_push = local_changes.intersection(remote_changes)
    if changes_to_push:
        print("The following modified files will be pushed to GitHub:")
        for filename in changes_to_push:
            print("- {}".format(filename))
        add_and_commit_changes("Update from Python script")
        push_changes()
    else:
        print("There are no modified files to push to GitHub.")
# Call the compare_and_push_changes function
compare_and_push_changes()
