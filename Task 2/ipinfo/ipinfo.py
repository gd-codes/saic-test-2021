
import datetime
import subprocess
import json
import re
import os
import argparse
import warnings

os.chdir(os.path.dirname(os.path.abspath(__file__)))

parser = argparse.ArgumentParser()
parser.add_argument('ip', help="IP address to scan")
parser.add_argument("--udp", help="""Scan UDP ports & services in addition to TCP.
May increase execution time > 10x""", action='store_true')
parser.add_argument("-o", "--outfile", help="""Write output log to specified file
Default is {cwd}/logs/{timestamp}.json""",  metavar="PATH", type=argparse.FileType('w'))
args = parser.parse_args()


data = {"address" : args.ip,
        "timestamp" : datetime.datetime.now().isoformat()}


def get_ports_os():
    global args, data
    cmd = ['nmap', '-sS', '-A', '-T4', args.ip]
    if args.udp :
        cmd.insert(2, '-sU')
    executed = subprocess.run(cmd, stdout=subprocess.PIPE)
    res = executed.stdout.decode('utf-8')

    if 'try -Pn' in res and 'Note: Host seems down' in res :
        cmd.insert(1, '-Pn')
        executed = subprocess.run(cmd, stdout=subprocess.PIPE)
        res = executed.stdout.decode('utf-8')

    port_os_info = re.split(re.compile(r'\n\b(?=MAC)'), res)
    data['ports_services'] = parse_portservices(port_os_info[0])

    if len(port_os_info) > 1:
        os_tr = port_os_info[1].split('TRACEROUTE')
        data['operating_system'] = os_tr[0]
        if len(os_tr) > 1 :
            data['traceroute'] = parse_traceroute(os_tr[1])

    if len(data['ports_services']) == 0 :
        data['portscan_comments'] = res


def parse_portservices(txt):
    pat1 = re.compile(r'(\d+)\/(\w+)\s*(\w+)\s*(\w+)\s*(.*)\n\|')
    pat2 = re.compile(r"(\d+\/\w+\s*\w+\s*\w+\s*.*\n\|)")

    infos = re.split(pat2, txt)[::2][1:]
    ports_services = []

    for match, info in zip(re.findall(pat1, txt), infos):
        m = {'port' : int(match[0]),
             'protocol' : match[1],
             'state' : match[2],
             'service' : match[3],
             'service_version' : match[4],
             'service_details': info.replace('\n|', '\n')}
        ports_services.append(m)

    return ports_services


def parse_traceroute(txt):
    pat = re.compile(
    r'HOP\s*RTT\s*ADDRESS\s*(\n(\d+)\s*([\d\.]+\s*\w*)\s*([\d\.a-fA-F\:]+))+')
    res = re.search(pat, txt)
    if res is not None:
        return res.group()
    else :
        return ""


def get_geoloc():
    global args, data
    cmd = ['curl', f'http://ip-api.com/json/{args.ip}']
    executed = subprocess.run(cmd, stdout=subprocess.PIPE, 
                                   stderr=subprocess.PIPE)
    res = executed.stdout.decode('utf-8')
    data['geolocation'] = json.loads(res)


def get_whois():
    global args, data
    cmd = ['whois', f'{args.ip}']
    executed = subprocess.run(cmd, stdout=subprocess.PIPE, 
                                   stderr=subprocess.PIPE)
    res = executed.stdout.decode('utf-8')
    data['domain_whois'] = parse_whois(res)


def parse_whois(text):
    c, d = [], {}
    for l in text.split('\n'):
        if l.strip():
            if l[0]=='%' or l[0]=='#':
                if  d : c.append(d)
                d = {}
                continue
            k = l.split(':')
            if k[0] in d:
                d[k[0]] += ''.join([x.strip() for x in k[1:]]) + '\n'
            else :
                d[k[0]] = ''.join([x.strip() for x in k[1:]]) + '\n'
    return c


def can_get_os():
    cmd = ['nmap', '-O', args.ip]
    try :
        executed = subprocess.run(cmd, stdout=subprocess.PIPE, timeout=1)
    except subprocess.TimeoutExpired:
        return False
    if 'requires root privileges' in executed.stdout.decode('utf-8'):
        return False
    else :
        return True
    


if __name__ == '__main__':

    print("Starting at", data['timestamp'])
    if not can_get_os():
        print("Attempting to find OS information...")
    else :
        warnings.warn("Root privileges required. Skipping Port scan & OS info.",
                    UserWarning)
    print("Scanning Ports...")
    get_ports_os()
    print("Getting geolocation data...")
    get_geoloc()
    print("Performing whois lookup...")
    get_whois()

    if args.outfile is None:
        logdate = datetime.datetime.now().isoformat().replace(':','')
        if not os.path.isdir('./logs'):
            os.mkdir('logs')
        args.outfile = open(f"./logs/Log_{logdate}.json", 'w')

    with args.outfile as of:
        json.dump(data, of, indent=4)

    print("Saved", os.path.abspath(args.outfile.name))
    with open('./.RECENT', 'a') as recentfile:
        recentfile.write(os.path.abspath(args.outfile.name))
        recentfile.write('\n')

