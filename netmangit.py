import git

# Set the token secret
token_secret = "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"

# Initialize a Git repository object
repo = git.Repo()

# Function to compare modified files and print the difference
def compare_files():
    # Get the remote repository object
    remote = repo.remote()

    # Fetch the latest changes from the remote repository
    remote.fetch()

    # Get the names of the modified files in the local repository
    local_diff = repo.git.diff("--name-only", "--diff-filter=M", "HEAD").splitlines()

    # Get the names of the modified files in the remote repository
    remote_diff = repo.git.diff("--name-only", "--diff-filter=M", "{}/HEAD".format(remote.name)).splitlines()

    # Find the difference between the two lists of modified files
    difference = list(set(local_diff) - set(remote_diff))

    # Print the difference
    print("Modified files that haven't been pushed to GitHub:")
    for filename in difference:
        print(filename)

# Add all files in the current directory to the staging area
repo.git.add(".")

# Commit the changes with a message
commit_msg = "Update from Python script"
repo.git.commit("-m", commit_msg)

# Push the changes to the remote repository with the token secret
remote_url = repo.remote().url
remote_url_with_secret = remote_url.replace("://", "://" + token_secret + "@")
repo.git.push(remote_url_with_secret)

# Compare modified files and print the difference
compare_files()
