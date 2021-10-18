##### SAIC Induction 2021
# Task 4

This script is a bash script that performs the required actions. There are 2 versions of it. Both of them can be configured in the following way :
At the start of the script, there are 4 variables :
- `LOCAL_REPO` : file path to the git repository on the machine
- `BASE_BRANCH` : Local branch into which changes must be pulled.
- `REMOTE_NAME` and `BRANCH_CHECK` : the remote branch to check for changes.

The script works by fetching the remote and determining whether there are changes based on the output of `git diff`. 
- `autopull.sh`. This is the one that I initially wrote. It also performs other checks and *does not pull* if (i) there are uncommited changes in the local branch or (ii) there is a potential merge conflict with the remote version. 
If there are changes, it will pull without fast forwarding the HEAD or creating a merge commit. This can be easily undone using `git merge --abort` in case this step warns about conflicts. In case there are no conflicts, commit to save the pulled changes.
- `autopull_simple.sh` I wrote this later when I realised that the script may actually be used on a server etc where there are no edits being made locally most of the time, so those checks are unnecessary. It **assumes that changes can always be pulled as a fast forward** since the local repo is never edited, so there will be no conflicts or uncommited changes. Other than that, the process is the same. It takes care of a disadvantage of the first script, which is that the successful pulls always required a commit, so it appeared over time that this branch is constantly moving N commits ahead of the remote, though those are only merge commits. With a `--ff-only` strategy, this is avoided.

`demo.mp4` shows the action of `autopull.sh`. To run the script, make it executable (`chmod +x`) and just run it from the Terminal.
It is best to run it periodically using `crontab` or a similar daemon so that checks occur often enough.

**Deployment**

For deploying the pulled changes, everything depends on which framework is being used (commands to run differ for Django, Flask, etc..). I couldn't write steps for everything, so I just included the build process for Jekyll, because it is simple and I'm familiar with it from STAC's Blog, where I've used it. (*Technically*, jekyll is static, but it still requires a build process from the markdown files). In `autopull_simple.sh`, there is a `build_jekyll` function in which you need to set the path of the directory into which the site will be generated.

### What I learnt
- Shell script expansions and string matching (for performing the checks in the 1st script).
- I also read about deployment procedures for other frameworks. For example, To use Django with an Apache server, the main step is to install a wsgi extension for apache and call it with the path to django's `wsgi.py` in the server's configuration. But there are more steps which were a bit complicated to learn at the last minute.
- About Git webhooks - I'd heard of these before and at first I thought of using this to identify when a change was made. But it requires having another port open listening for HTTP requests from github etc, which can still be more complex and resource consuming than fetching and checking every 30 mins etc from crontab or something like that.

