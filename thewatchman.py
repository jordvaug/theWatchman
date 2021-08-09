#! python

from json.decoder import JSONDecodeError
import os
import sys
from urllib import request
from bs4 import BeautifulSoup
import url_builder
import pathlib
import requests
import asyncio
import url_aggregator
from optparse import OptionParser
import report_builder
import target_profiler
from pathlib import Path

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
    new_display = str(cPath) + '\\display.html'
    d = pathlib.PureWindowsPath(new_display)
    report_builder.writeHeadersToDisplay(d, req)


def enumerateEndpoints(endpoints, url, cPath):
    print('Enumerate endpoint list:')
    print()
    for ep in endpoints:
        furl = url + ep
        furl = url_builder.urlParser(furl)
        req = requests.get(furl)
        scanText(req, cPath)
        checkHeaders(req, cPath)


def scanText(req, cPath):
    soup = BeautifulSoup(req.text, 'html.parser')
    new_display = str(cPath) + '\\display.html'
    d = pathlib.PureWindowsPath(new_display)

    if soup.find('Unauthorized Access') or len(str(soup)) == 0:
        print('No Page Found')
    elif req.status_code == 401 or req.status_code == 302 or req.status_code == 404:
        print('No Page Found')
    else:
        report_builder.writeDataToDisplay(d, soup, req.url)

        if soup.find_all('a') != None:
            links = str(cPath) + '\\links.txt'
            my_file = Path(str(links))
            l = pathlib.PureWindowsPath(links)
            if not my_file.is_file():
                with open(l, 'w') as f:
                    f.write('Links Found:\n')
            d = pathlib.PureWindowsPath(new_display)
            with open(l, 'w') as f:
                f.write('\n*********************\n')
                f.write('Links found from: ' + '\n' + req.url + '\n\n')
                for link in soup.find_all('a'):
                    f.write('\n')
                    f.write(str(link.get('href')))


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

    
    parser = OptionParser()
    parser.add_option("-q", "--quiet", action="store_false", dest="verbose", default=False, help="Silence command line output")
    parser.add_option("-H", "--Host",dest='url', type='string', help="Specify target Host")
    parser.add_option("-t", "--Type",dest='appType', type='string', help="Specify target Application type (options: dotnet, wp)")
    (options, args) = parser.parse_args()

    url = options.url

    if url == None:
        print('Must specify target host.')
        print('Example: https://www.example.com')
        exit(0)
    else:
        print(url)

    quiet = options.verbose

    if quiet:
        sys.stdout = open(os.devnull, 'w')

    appType = options.appType

    if appType == None:
        print('No application type specified, trying to determine...')

    while not validators.url(url):
        url = input('Try again, that was not a valid url: ')

    if url[-1] == '/':
        url = url[0:-1]

    try:
        requests.get(url)
    except requests.exceptions.RequestException as e:
        print('That url caused some problems, maybe it isn\'t valid?')
        raise SystemExit(e)

    results = target_profiler.scanHost(url)

    cPath = report_builder.createDisplayDirectory()

    report_builder.writeNmapScanToDisplay(cPath, results)

    endpoints = loadEndpointsList()

    screenshot(url, cPath)

    enumerateEndpoints(endpoints, url, cPath)
    urls = url_aggregator.scanSwagger(url)
    scanEndpointsFromSwagger(urls, cPath)

    if quiet != None:
        sys.stdout = sys.__stdout__

    print('You will find results in a new folder one directory up.')


runScan()







    

    
  