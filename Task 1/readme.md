##### SAIC Induction 2021
# Task 1

I couldn't finish this task fully, here's a detailed explanation of what I tried :

### Process

1. After initially installing VirtualBox and importing the VM, I had to configure some of the network settings. The default netowrk device was not recognised, and I had to choose from one of the available network interfaces on my laptop and connection methods. Finally, I set it to *bridged, interface en0* which means that it has its own ip on the same local network like my laptop, accessed though this WiFi/ethernet (en0) interface. (After tring other various options, understanding what they do and trying to connect to the device)
2. Next, to find this private ip address i tried some of the following commands : 
    - `ifconfig` to find my own ip and home router subnet address (which was 192.168.1.0/24 in this case, with broadcast to 192.168.1.255)
    - `arp -a ` which gives a list of devices and MAC addresses, usually includes all online on the private network. This identified 10-15 IPs
    - `nmap -sn 192.168.1.0/24` after discovering the nmap command. This did a thorough search and narrowed the possibility to only 3-4 "online hosts".
3. Then after trying these IPs in the browser, it was `192.168.1.3`.
4. I inspected the HTML and JS code in detail. There are no hyperlinks, embeds or any other AJAX code with which network connections might be made after the page loads. So all network traffic is only in the initial loading phase from the server itself (no external sources). There were also no cookies or local/session storage used, which could be manipulated otherwise.
5. I tried finding some info about the server. Trying random URLs to give 404 error pages shows the Apache default error page, along with server version (confirmed that it is an apache server). Unfortunately the links to *index.js* and *index.css* from the HTML page don't reveal anything about any directory structure inside the `public_html`. I inspected the HTTP headers from the browser's network requests DevTools (Google Chrome), and also using `curl -v`. This also doesn't give any additional info. I tried loading some other locations like `/icons` and `/server-status` which are used by Apache servers generally, but they were blocked (403 forbidden). I also tried looking at the output log of `sudo tcpdump` while reloading the page in the browser, but didn't discover anything.
6. I moved on from the HTTP & browser-level inspection to try to find other openings on this device. I descovered that nmap offers a lot more tools for this. I tried `sudo nmap -O` to get the OS details and `nmap -A -T4` & `nmap --top-ports` & `nmap -sU -A -T4` to find out all the open ports using TCP and UDP (-sU). This also revealed a lot of details about the services. (I had also started working on Q2, so I ran that script on this - you can see the output there in `private1.json`).
7. Besides HTTP for the server, standard FTP and SSH ports were also open. ProFTPD was accepting anonymous connections. I used `curl -v ftp://192.168.1.3/` to attempt to connect and see all the headers exchanged. I downloaded the `site.html` file that was available. There didn't seem to be any useful info here (not even in whitespace etc in case something was encoded like that... :P). I tried adjusting the path (with escaped slash %2f) to make curl issue a `CWD ./..` FTP request. It responded with success code, but didn't actually go outside that directory :(
8. I used `curl -T` to transfer a random text file, and it actually uploaded it ! (permanently, this stayed even after rebooting the VM). *This could be a potential vulnerability.* I could upload a script that lists files outside these folders and sends me whatever info i need, although i can't execute it yet using ftp (i'm not sure how otherwise, if i have that much access, i might be able to directly get that info).
9. I didn't try much with SSH. I got the public key fingerprints of the machine from nmap's output, but by now I started focusing more on the other questions. I tried a few random username/password guesses including hackme, saic, etc, *just in case* XD, but if authentication is with a private key string from `ssh-keygen` then these won't work anyway.
10. Later I came back to this task and tried some [nmap scripts](https://nmap.org/nsedoc/categories/safe.html), the *http-\** ones to try to check for git repos, list (ls) files without returning index.html, etc. These didn't show anything useful.
11. I started attempting (unsuccessfully) to spoof my IP to its own address (192.168.1.3) to get in (using `nmap -S` and adding `X-Forwarded-For:` HTTP header), but didn't actually complete it. I could set up port forwarding on my router to allow TCP connections to happen with this. Although i'm not sure if IP spoofing will get me anything new, more info might only be limited to localhost (127.0.0.1) which is within the VM. I also know the least about this.

### Scripts & Tools

- Primarily, the command that was most useful here was `nmap`. This is also the only one I had to install (others are usually present by default, like curl, ping, arp, etc). It can be downloaded using `brew` on MacOS or `apt-get` on *nix, other options on the [website](https://nmap.org/download.html).
- I didn't write any other programs for this (other than the one in Task 2)

### What I learnt
I think most of the things  came across are listed in the long description above, many of them were new to me.
`Nmap` was the most valuable finding - this has a huge number of features to extract info from IP packets in all sorts of ways.

Other than that, I also found out details about a lot more commands like
- `nc` (netcat) for managing TCP/UDP connections
- `netstat` to list ports with connections
- flags and options/args for common commands like `curl`, `dig`, `nslookup`, etc which i had used before but not in detail.


- Also learnt a bit about FTP & SSH protocols (headers, key-auth mechanisms, etc). 
- It made me refresh fome basic facts about TCP/IP protocols, subnetworks, etc.
-  Also about the other methods of connecting a VM to network (using NAT, port forwarding, Host-only connection through VirtualBox, etc).
