#!/usr/bin/env bash

# Change these variables to required values
# ENSURE that the remote & branch names are correct ! (no typos)
LOCAL_REPO='./misc'
REMOTE_NAME='origin'
BRANCH_CHECK='master'
BASE_BRANCH='master'

cd "$LOCAL_REPO"
git checkout "$BASE_BRANCH"

git fetch "$REMOTE_NAME"

git merge --ff-only "$REMOTE_NAME/$BRANCH_CHECK"


# Framework specific deployment options
# Call only the function required depending on the project

build_jekyll() {
    # Refer https://jekyllrb.com/docs/deployment/automated/
    SERVER_HTML_DIR='./site'
    bundle install
    bundle exec jekyll build -s . -d "SERVER_HTML_DIR"
}

# For example, assuming this is a jekyll project
build_jekyll
