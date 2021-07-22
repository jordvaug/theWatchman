import requests
from json.decoder import JSONDecodeError

def scanSwagger(url):
    import json

    if url[-1] == '/':
        url = url[0:-1]

    furl = url + '/api/swagger/v1/swagger.json'

    req = send(furl)

    if req.status_code == 404 or req.status_code == 302:
        print('No swagger found at: ' + furl)
        req = send(url + 'swagger/swagger.json')
        if req.status_code == 404 or req.status_code == 302:
            print('No swagger found at: /swagger/swagger.json')
            req = send(url + 'v1/swagger/swagger.json')
            if req.status_code == 404 or req.status_code == 302:
                print('No swagger found at: /v1/swagger/swagger.json')
                req = send(url + 'swagger/docs/swagger.json')
                if req.status_code == 404 or req.status_code == 302:
                    print('Giving up on finding swagger docs...')
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
                for v in servers:
                    serv = v['url']
                    ep = serv + k
                    if ep not in endpoints:
                        with open('endpoints.txt', 'a') as file:
                            file.write('\n' + p1 + k)
                        u = url + p1 + k
                        for m in v.keys():
                            urls.append(u)
                            urls.append(m.upper())

    return urls



def send(url):
    return requests.get(url, headers={'Content-Type': 'application/json'})