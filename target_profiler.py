import json
import nmap
import socket
import re

def scanHost(url):
    print('Profile Target....')

    #prepare url for socket use
    if re.search('https:', url, re.IGNORECASE):
        url = url.replace("https:", "")
    if re.search('http:', url, re.IGNORECASE):
        url = url.replace("http:", "")
    if re.search('/', url, re.IGNORECASE):
        url = url.replace("/", "")

    print('-----------------------------------------')
    print('Scanning: ')
    print(url)

    ip = socket.gethostbyname(url)
    nm = nmap.PortScanner()
    #-sC performs script scan with script set to default, some scripts are intrusive
    results = nm.scan(hosts=ip, arguments='-sC -A -p T:80,443,3000,5000,8080,8445')
    lport = []

    for port, res in results['scan'][ip]['tcp'].items():
        if res['state'] == 'open':
            lport.append(port)

    #lport holds the open ports from scan list
    print('Open Ports:')
    print(lport)

    if re.search('Microsoft', json.dumps(results), re.IGNORECASE):
        appType = 'dotnet'
    else:
        appType = 'unknown'

    print()
    print('Application Type in use (best guess): ')
    print(appType)
    print('-----------------------------------------')

    return results