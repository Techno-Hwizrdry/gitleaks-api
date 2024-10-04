# GitLeaks API
A Python3/FastAPI wrapper to turn [GitLeaks](https://github.com/gitleaks/gitleaks) into a RESTful API.

# Prerequisites
This script requires python3 (version 3.7 or later), python3-pip, python3-devel, and virtualenv.

The prerequisites can be installed on a Debian based linux machine, like so:

`sudo apt-get install git python3 python3-pip python3-devel && sudo pip3 install virtualenv`

You must also have GitLeaks installed as well.  See the `GitLeaks` section below.

## GitLeaks
Below are the installation options for GitLeaks and their corresponding install instructions: 

```bash
# MacOS
brew install gitleaks

# Docker (DockerHub)
docker pull zricethezav/gitleaks:latest
docker run -v ${path_to_host_folder_to_scan}:/path zricethezav/gitleaks:latest [COMMAND] [OPTIONS] [SOURCE_PATH]

# Docker (ghcr.io)
docker pull ghcr.io/gitleaks/gitleaks:latest
docker run -v ${path_to_host_folder_to_scan}:/path ghcr.io/gitleaks/gitleaks:latest [COMMAND] [OPTIONS] [SOURCE_PATH]

# From Source (make sure `go` is installed)
git clone https://github.com/gitleaks/gitleaks.git
cd gitleaks
make build
```

Make sure that the execute permissions on the gitleaks executable is enabled for 'other'.

## Setup
Once those prerequisites have been installed, git clone this repo, cd into it, and set up the virtual environment:

`cd /path/to/gitleaks_api && ./setup_virtualenv.sh`

setup_virtualenv.sh will set gitleaks_api as the virtual environment, activate it, and call pip3 to download and install all the python3 dependencies for this script.  These dependencies are listed in requirements.txt.

Next, copy and paste the SSH fingerprints from [GitHub](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/githubs-ssh-key-fingerprints) and [GitLab](https://docs.gitlab.com/ee/user/gitlab_com/index.html#ssh-host-keys-fingerprints) into your `~/.ssh/known_hosts` file.

# Running the API
Via the FastAPI development server:

`cd /path/to/gitleaks_api/src && fastapi run`

# Usage
All of the endpoints only respond to HTTP POST requests.

## /detect/
To use the `/detect/` endpoint, you must pass it a git link.  The git link can either be a SSH link or a HTTPS link, as seen in the following example curl commands:

`curl -X POST -d "git@github.com:example/example_repo.git" http://127.0.0.1:8000/detect`

`curl -X POST -d "https://github.com/example/example_repo.git" http://127.0.0.1:8000/detect`