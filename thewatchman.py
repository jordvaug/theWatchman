#! python

from json.decoder import JSONDecodeError
import os
from urllib import request
from bs4 import BeautifulSoup
import url_builder
import pathlib
import requests
import asyncio

def loadEndpointsList():
    with open('endpoints.txt') as f:
        endpoints = f.read().splitlines()
    return endpoints


def scanEndpointsFromSwagger(urls, cPath):
    for indx in range(0, len(urls), 2):
        url = url_builder.urlParser(urls[indx])
        req = hitEndpoint(url, urls[indx+1])
        checkHeaders(req, cPath)
        scanText(req, cPath)

        
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

    with open("./Templates/scripts.js", 'r') as f:
        content = f.read()

    scripts = str(d) + "\\scripts.js"

    scr = pathlib.PureWindowsPath(scripts)

    with open(scr, 'w') as f:
        f.write(content)

    return d


def scanSwagger(url):
    import json

    if url[-1] == '/':
        furl = url + 'api/swagger/v1/swagger.json'
    else:
        furl = url + '/api/swagger/v1/swagger.json'

    req = hitEndpoint(furl, 'GET')

    if req.status_code == 404:
        return []

    try:
        data = json.loads(req.text)
    except JSONDecodeError as e:
        print('That request was not json I could decode, ensure this site has a swagger api')

    p1 = ''

    servers = data['servers']

    for v in servers:
        p1 = v['url']

    urls = []

    with open('endpoints.txt', 'r') as f:
        endpoints = f.read().splitlines()
        paths = data['paths']
        for k, v in paths.items():
            ep = '/api' + k
            if ep not in endpoints:
                with open('endpoints.txt', 'a') as file:
                    file.write('\n' + p1 + k)
                u = url + p1 + k
                for m in v.keys():
                    urls.append(u)
                    urls.append(m.upper())
    return urls

def hitEndpoint(url, method):
    import requests

    data = {}
    headers = {'Content-Type': 'application/json'}

    if method == "GET":
        return requests.get(url, headers=headers)
    elif method == 'POST':
        return requests.post(url, headers=headers)
    elif method == "PUT":
        return requests.put(url, headers=headers)
    elif method == 'DELETE':
        return requests.get(url, headers=headers)
    elif method == 'OPTIONS':
        return requests.options(url, headers=headers)
    elif method == "HEAD":
        return requests.head(url, headers=headers)

def checkHeaders(req, cPath):
    headers = req.headers

    new_display = str(cPath) + '\\display.html'

    d = pathlib.PureWindowsPath(new_display)

    with open(d, 'r') as f:
        contents = f.read()

    writeHeadersToDisplay(d, req.url, headers)

def enumerateEndpoints(endpoints, url, cPath):
    for ep in endpoints:
        furl = url + ep
        furl = url_builder.urlParser(furl)
        req = requests.get(furl)
        scanText(req, cPath)


def scanText(req, cPath):
    soup = BeautifulSoup(req.text, 'html.parser')
    new_display = str(cPath) + '\\display.html'
    d = pathlib.PureWindowsPath(new_display)

    if soup.find('Unauthorized Access') or len(str(soup)) == 0:
        print('No Page Found')
    elif req.status_code == 401 or req.status_code == 302 or req.status_code == 404:
        print('No Page Found')
    else:
        writeDataToDisplay(d, soup, req.url)

        if soup.find_all('a') is not 'None':
            with open('links.txt', 'w') as f:
                f.write('\n*********************\n')
                f.write('Links found from: ' + '\n' + req.url + '\n\n')
                for link in soup.find_all('a'):
                    f.write('\n')
                    f.write(str(link.get('href')))

def writeDataToDisplay(new_display, soup, url):
    from pathlib import Path

    d = pathlib.PureWindowsPath(new_display)

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
        title = f"<button class='accordion'>{url}</button><div class='panel'><p>{soup.prettify()}</p></div>"
        tag = new_soup.find(id="DataIn")
        title_soup = BeautifulSoup(title, 'html.parser')
        tag.insert_before(title_soup)
        file.write(new_soup.prettify())

def writeHeadersToDisplay(new_display, url, headers):
    from pathlib import Path

    d = pathlib.PureWindowsPath(new_display)

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
        title = f"<button class='accordion'>{url}</button><div class='panel'>"
        tag = new_soup.find(id="HeadersIn")

        nonos = {'role', 'password', 'token'}
        required_headers = {'X-XSS-Protection', 'Strict-Transport-Security', 'X-Frame-Options', 'X-Content-Type-Options', 'Content-Security-Policy', 'Referrer-Policy'}

        for no in nonos:
            if no in headers:
                title += '<p>Value improperly included in headers: ' + no + '</p>'
        
        for rh in required_headers:
            if rh not in headers:
                title += '<p>Missing required header: ' + rh + '</p>'

        if 'X-XSS-Proctection' in headers and headers['X-XSS-Proctection'].find('1') != -1:
            title += '<p>Misconfigured X-XSS-Proctection Header</p><p>https://owasp.org/www-project-secure-headers/#x-xss-protection</p>'

        title += '</div>'
        title_soup = BeautifulSoup(title, 'html.parser')
        tag.insert_before(title_soup)
        file.write(new_soup.prettify())


async def loadJS(url, cPath):
    from pyppeteer import launch

    new_display = str(cPath) + '\\screenshot.png'
    img = pathlib.PureWindowsPath(new_display)

    browser = await launch()
    page = await browser.newPage()
    await page.goto(url)
    await page.screenshot({'path': img})

    await browser.close()

def screenshot(url, cPath):

    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    asyncio.get_event_loop().run_until_complete(loadJS(url, cPath))


def runScan():
    import validators
    
    print('===============================================')
    print('                 TheWatchman                   ')
    print('===============================================')

    url = input('Enter the domain you want to scan (ex https://example.com: ')

    while not validators.url(url):
        url = input('Try again, that was not a valid url: ')

    if url[-1] == '/':
        url = url[0:-1]

    try:
        r = requests.get(url)
    except requests.exceptions.RequestException as e:
        print('That url caused some problems, maybe it isn\'t valid?')
        raise SystemExit(e)

    endpoints = loadEndpointsList()
    cPath = createDisplayDirectory()

    screenshot(url, cPath)
    enumerateEndpoints(endpoints, url, cPath)
    urls = scanSwagger(url)
    scanEndpointsFromSwagger(urls, cPath)
    print('You will find results in a new folder one directory up.')

runScan()








    

    
  