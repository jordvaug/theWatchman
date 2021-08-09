import os
import pathlib
from bs4 import BeautifulSoup
from pathlib import Path

def createDisplayDirectory():
    from datetime import datetime

    os.chdir('..')
    cPath = os.getcwd()
    os.chdir('theWatchman')
    now = datetime.now()
    nowStr = now.strftime("%d-%m_%H.%M.%S")
    new_directory = cPath + '\\' + nowStr + '_Scan'

    d = pathlib.PureWindowsPath(new_directory)
    os.mkdir(d)

    with open("./Templates/style.css", 'r') as f:
        content = f.read()

    style = str(d) + "\\style.css"

    s = pathlib.PureWindowsPath(style)

    with open(s, 'w') as f:
        f.write(content)

    return d




def writeDataToDisplay(new_display, soup, url):
    d = pathlib.PureWindowsPath(new_display)

    my_file = Path(str(d))

    if my_file.is_file():
        with open(d, 'r') as f:
            content = f.read()
            new_soup = BeautifulSoup(content, 'html.parser')
    else:
        p = os.getcwd()
        p = str(p) + "\\Templates\\display.html"
        p = pathlib.PureWindowsPath(p)
        with open(p, 'r') as f:
            content = f.read()
            new_soup = BeautifulSoup(content, 'html.parser')
                 
    with open(d, 'w') as file:
        tag = new_soup.find(id="DataIn") 
        title = f"<button class='accordion'>{url}</button><div class='panel'><p>{soup.prettify()}</p></div>"
        title_soup = BeautifulSoup(title, 'html.parser')
        tag.insert_before(title_soup)
        file.write(new_soup.prettify())


def writeHeadersToDisplay(new_display, req):

    d = pathlib.PureWindowsPath(new_display)

    my_file = Path(str(d))

    if my_file.is_file():
        with open(d, 'r') as f:
            content = f.read()
            new_soup = BeautifulSoup(content, 'html.parser')
    else:
        p = os.getcwd()
        p = str(p) + "\\Templates\\display.html"
        p = pathlib.PureWindowsPath(p)
        with open(p, 'r') as f:
            content = f.read()
            new_soup = BeautifulSoup(content, 'html.parser')
            
    with open(d, 'w') as file:
        title = f"<button class='accordion'>{req.url}</button><div class='panel'>"
        tag = new_soup.find(id="HeadersIn")
        txt = ""

        nonos = {'role', 'password', 'token'}
        required_headers = {'X-XSS-Protection', 'Strict-Transport-Security', 'X-Frame-Options', 'X-Content-Type-Options', 'Content-Security-Policy', 'Referrer-Policy'}

        for no in nonos:
            if no in req.headers:
                txt += '<p>Value improperly included in headers: ' + no + '</p>'
        
        for rh in required_headers:
            if rh not in req.headers:
                txt += '<p>Missing required header: ' + rh + '</p>'

        if 'X-XSS-Proctection' in req.headers and req.headers['X-XSS-Proctection'].find('1') != -1:
            txt += '<p>Misconfigured X-XSS-Proctection Header</p><p>https://owasp.org/www-project-secure-headers/#x-xss-protection</p>'

        if 'Allow' in req.headers:
            txt += '<h4>Allowed Methods</h4><br /><p>' + req.headers['Allow'] + '</p>'
            
        if txt != "":
            title += txt
            title += '</div>'
            title_soup = BeautifulSoup(title, 'html.parser')
            tag.insert_before(title_soup)
        file.write(new_soup.prettify())


def writeNmapScanToDisplay(new_display, nm):
    nd = str(new_display) + '\\display.html'
    d = pathlib.PureWindowsPath(nd)
    scan = nm['scan'].items()

    my_file = Path(str(d))

    if my_file.is_file():
        with open(d, 'f') as f:
            content = f.read()
            new_soup = BeautifulSoup(content, 'html.parser')
    else:
        p = os.getcwd()
        p = str(p) + "\\Templates\\display.html"
        p = pathlib.PureWindowsPath(p)
        with open(p, 'r') as f:
            content = f.read()
            new_soup = BeautifulSoup(content, 'html.parser')
            
    with open(d, 'w') as file:
        for host, value in scan:
            title = f"<h3>Host</h3><div><p>Host : {(value['hostnames'][0]['name'])}</p><br />"
            title += f"<br/><p>State: {value['status']['state']}</p>"
            title += f"<hr><br/><h5>TCP Ports</h5><br/>"
            for port, v in value['tcp'].items():
                title += f"<span> port:     {port}</span><br/><span>state:    {v['state']}</span><br/>"
                title += "<hr><br/>"
            title += "</div>"
            tag = new_soup.find(id="NMAPIn")
            title_soup = BeautifulSoup(title, 'html.parser')
            tag.insert_before(title_soup)
            file.write(new_soup.prettify())


