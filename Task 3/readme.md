##### SAIC Induction 2021
# Task 3

Both of the given websites were static frontend sites only, so to host them I used python's `http.server` module because it was simple and fast. (I'm aware that it's not meant for deployment-level security, but I assumed that the focus of the question was more on the container mechanism than which server I used)

I found out while learning about Docker that, to start the app, you can only specify one `CMD` in the Dockerfile. thus, both sites have to be able to start seperately using a single command (which can be a call to a script), so I can't simply call `python -m http.server {port} -d {site}` twice. So I wrote `simplehttpservers.py` which instantiates the server twice, making additional changes to the inherited class so that each site is served separately with its own root in its repo directory (by default, http.server uses the CWD as root, and i can't have 2 cwds in one process). Then each of these is started on 2 seperate threads from the main script.

I chose the ports `1025` and `1026` to run the websites because they are not the dynamic/private use ports which may be taken by browser tabs etc, but they are also not registered for use by any service according to [this list](https://en.wikipedia.org/wiki/List_of_TCP_and_UDP_port_numbers), so it is highly unlikely that they are unavailable. (Even outside the docker conatiner, they can be mapped to the same numbers if needed).

### Running the container
The image is available on docker hub from
```
docker pull gdcodes/saic-sites
```
It can be run using
```
docker run -it -p 1025:1025 -p 1026:1026 --rm gdcodes/saic-sites
```
or any other port mapping required.

The `--rm` flag deletes the container after stopping, it can be omitted). Even the `-i -t` flags can be omitted, the server does not take any input from stdin anyway. These and the `WORKDIR` in the Dockerfile were based on Python's recommendation [here](https://hub.docker.com/_/python).


### What I learnt

I learnt a lot about Docker - this was new to me. I'd heard of conatiners and virtualisation / sandboxing many times before, but didn't actually get into the details. I found out it is similar to Kubernetes, which I'd also seen before in some places but didn't actualy know what it did.

I learnt various Docker-specific terms like images vs. containers and Dockerfile syntax etc.