import git

# Set the GitHub repository URL
github_repo_url = "git@github.com:prathz111/NetmanLab5.git"

# Initialize a Git repository object
repo = git.Repo(".")

def add_and_commit_changes(commit_msg):
    # Add all files in the current directory to the staging area
    repo.git.add(".")
    # Commit the changes with a message
    repo.git.commit("-m", commit_msg)

def push_changes():
    # Push the changes to the remote repository using the default SSH transport mechanism
    repo.remote().push()

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
