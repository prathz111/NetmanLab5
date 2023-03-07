"""
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
"""
import git

# Set the token secret
token_secret = "YOUR_TOKEN_SECRET_HERE"

# Initialize a Git repository object
repo = git.Repo()

# Add all files in the current directory to the staging area
repo.git.add(".")

# Commit the changes with a message
commit_msg = "Update from Python script"
repo.git.commit("-m", commit_msg)

# Function to compare modified files in local repository with GitHub repository
def compare_files():
    # Get the list of modified files in the local repository
    modified_files = repo.git.diff("--name-only", "--diff-filter=M", "HEAD").splitlines()

    # Get the list of modified files in the remote repository
    remote = repo.remote()
    remote.fetch()
    remote_diff = repo.git.diff("--name-only", "--diff-filter=M", "{}/HEAD".format(remote.name)).splitlines()

    # Find the files that are in the local repository but not in the remote repository
    new_files = list(set(modified_files) - set(remote_diff))

    # Print the difference
    if new_files:
        print("The following files have been modified locally and need to be pushed to GitHub:")
        for file in new_files:
            print(file)
    else:
        print("No new files to push to GitHub.")

# Function to push modified files to GitHub
def push_files():
    # Get the list of modified files in the local repository
    modified_files = repo.git.diff("--name-only", "--diff-filter=M", "HEAD").splitlines()

    # Push each modified file to the remote repository
    for file in modified_files:
        remote_url_with_secret = remote.url.replace("://", "://{}@".format(token_secret))
        repo.git.push("{} {}".format(remote_url_with_secret, file))

    print("All modified files have been pushed to GitHub.")

# Compare modified files and push them to GitHub if any exist
compare_files()
push_files()
