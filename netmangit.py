import git

# Set the token secret
token_secret = "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"

# Initialize a Git repository object
repo = git.Repo()

# Add all files in the current directory to the staging area
repo.git.add(".")

# Commit the changes with a message
commit_msg = "Update from Python script"
repo.git.commit("-m", commit_msg)

# Push the changes to the remote repository with the token secret
remote_url = repo.remote().url
remote_url_with_secret = remote_url.replace("://", "://{}@".format(token_secret))
repo.git.push(remote_url_with_secret)
