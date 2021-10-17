#!/usr/bin/env bash

# Change these variables to required values
# ENSURE that the remote & branch names are correct ! (no typos)
LOCAL_REPO='/Users/gautamd/School/IIT-Mandi/clubs/SAIC test/Task 4/misc'
REMOTE_NAME='origin'
BRANCH_CHECK='master'
BASE_BRANCH='master'

export TERM='xterm-256color'
log_info() { echo "$(tput setaf 2)[INFO]$(tput sgr0) $@"; }
log_err() { echo "$(tput setaf 1)[ERROR]$(tput sgr0) $@"; }

log_info "Starting `date`"
log_info "Location : $LOCAL_REPO"
log_info "Pull branch $REMOTE_NAME/$BRANCH_CHECK into $BASE_BRANCH"

cd "$LOCAL_REPO"
git checkout "$BASE_BRANCH"

status=$(git status)

if [[ $status != *"nothing to commit, working tree clean"* ]]; then
    log_err "Uncommited/unstashed changes exist. Aborting"
    exit 1
else
    log_info "Confirmed no uncommitted changes !"
fi

log_info "Fetching remote"
git fetch "$REMOTE_NAME"
changed=$(git diff "$BASE_BRANCH" "$REMOTE_NAME/$BRANCH_CHECK")

if [ ! -z "$changed" ]; then

    conflict=$(git merge --no-commit --no-ff "$REMOTE_NAME/$BRANCH_CHECK")

    if [[ $conflict == *"Automatic merge failed"* ]]; then
        git merge --abort
        log_err "Merge conflicts exist. Automatic pull was aborted"
        exit 2
    else
        pulltimestamp=$(date)
        git commit -m "Auto-pull from $REMOTE_NAME/$BRANCH_CHECK at $pulltimestamp"
        log_info "Successfully pulled new changes !"
    fi
else
    log_info "No new changes found. Exiting."
fi
