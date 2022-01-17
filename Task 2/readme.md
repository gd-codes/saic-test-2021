##### SAIC Induction 2021
# Task 2

The scripts are written in Python, in the package `ipinfo` in this directory. There are 2 seperate scripts -
- `ipinfo.py` which does the scanning and data collection
- `mailer.py` which sends the logs via email.

The scanning itself is still performed only by shell commands (`nmap`, `curl` & `whois`), like in Task 1. Python is just a "wrapper" around those to format the output. I could have written the entire program as a shell script, but the only problem is that I can't yet do advanced text parsing with `sed`/`awk` etc, though I'm familiar with regex. The mail functionality could have also used the `sendmail` executable, but I'd already written an emailing program in Python before, so I just reused and modified [that code](https://github.com/gd-codes/email).

Required libraries :
+ Only `nmap` needs to be installed - I'd already used it for task 1. Lots of options are available on the [website](https://nmap.org/download.html). I assume that `curl` and `whois` are already available, they are very commonly used commands.
+ No other Python modules need to be additionally installed. Only those from the standard library (most importantly `subprocess`, `re`, `smtplib`) are used.

### Documentation

1. To perform the scan, run `sudo python3 ipinfo.py {ADDR}` to scan the target domain. **sudo privileges are required** for `nmap` to perform the full scan. I have used `argparse` to make it behave more like a shell command with flags, you can also use `--help` to se a few other options.
2. This takes some time to run and generates writes the output to `ipinfo/logs/` by default. The format is described below. <br/><br/>

3. To email this, `mailer.py` sends it via Gmail's smtp servers. This is because sending an email without an account is risky (sendmail may use something like *user-computername.local* as the email domain if not provided with an actual host, which usually gets blocked).
4. To setup Gmail, open your google account settings and enable [less secure app access](https://myaccount.google.com/intro/security). (Even though the smtp server uses TLS, this is required). Then the script will be able to authenticate with your gmail account.
5. To run the script, temporarily `export` your username & password as the environment variables `IP_SENDER_ADDR` and `IP_SENDER_AUTH` respectively. Then run `python3 mailer.py --to {addresses}` from the same shell where these variables are defined. (sudo not required for emailing). An example of this is to use `mail.sh` provided in this directory. Unfortnately, this means storing the credentials in plaintext in this file, if the process needs to be automated without you defining these each time.
6. To email at regular intevals, I executed this script with `crontab`. You can see this in the demo video. Each time it runs, it sends the most recently generated logfile. (These paths are stored in a `.RECENT` file in the ipinfo module. *Do not edit !*)

**Note**: I had a little trouble running the `ipinfo.py` scanner script from crontab - in that environment, `subprocess` doesn't find the executable commands, and specifying `shell=True` caused other problems etc. So for now, only the email script runs automatically. You need to run the scanner on an IP when required. You can use the `--email` flag on ipinfo\.py to send a mail immediately, and avoid duplicate reports by having mail run on a seperate schedule.


### Output format
The log file is in JSON, with the following structure :
- Top level : object, with the following keys
- `address` - the IP/domain that was scanned
- `timestamp` - date & time of scan start
- `ports_services` - array of objects with the following keys (one object for each open port found)
    + `port` - port number, int
    + `protocol` - e.g "tcp"
    + `state` - e.g. "open", "filtered" etc
    + `service` - e.g. "http", "ssh" etc
    + `service_version` - software name (e.g. "Apache 2.0 for HTTP")
    + `service_details` - any other info
- `portscan_comments` - text, *present only if `ports_services` is empty list*. Contain's nmap raw output to see why this happened.
- `geolocation` - object with following keys
    + `status` - "success" or "fail"
    + `country`, `countryCode`, `region`, `regionName`, `city`, `zip`, `lat`, `lon`, `timezone`, `isp`, `org`, `as` - included if query succeded
    + `message` - reason of failure, if it failed
- `operating_system` - text, any details about the OS found. *Present only if `ports_services` is not empty*
- `traceroute` - text, hops and trip times to reach the target *Present only if `ports_services` is not empty*
- `domain_whois` - List of objects conatining info returned by a WHOIS query. May be empty if there was no returned info.

### Demo
You can look at `demo.mp4` to see it in action. `private1.json` and `public1.json` are examples of the output when i ran this on my ip address (even without firewalls, i found out my laptop blocks all of nmap's queries) and the VM from task 1.


### What I learnt
- More about port scanning and `nmap`
- refreshed facts on IP and DNS services, WHOIS protocol
- Email MIME format, how to add attachments

etc..

