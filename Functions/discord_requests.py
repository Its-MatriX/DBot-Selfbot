import requests


def send_request(bot, method, path, json=None, add_headers={}):
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Origin': 'https://discord.com',
        'Pragma': 'no-cache',
        'Referer': 'https://discord.com/channels/@me',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': bot.http.user_agent,
        'X-Super-Properties': bot.http.encoded_super_properties,
        'Authorization': bot.http.token
    }

    for key in list(add_headers.keys()):
        headers[key] = add_headers[key]

    if json:
        if method == 'GET':
            response = requests.get('https://discord.com/api/v7' + path,
                                    headers=headers,
                                    json=json)

        elif method == 'POST':
            response = requests.post('https://discord.com/api/v7' + path,
                                     headers=headers,
                                     json=json)

        elif method == 'PATCH':
            response = requests.patch('https://discord.com/api/v7' + path,
                                      headers=headers,
                                      json=json)

        elif method == 'PUT':
            response = requests.put('https://discord.com/api/v7' + path,
                                    headers=headers,
                                    json=json)

        elif method == 'HEAD':
            response = requests.head('https://discord.com/api/v7' + path,
                                     headers=headers,
                                     json=json)

        elif method == 'DELETE':
            response = requests.delete('https://discord.com/api/v7' + path,
                                       headers=headers,
                                       json=json)

    else:
        if method == 'GET':
            response = requests.get('https://discord.com/api/v7' + path,
                                    headers=headers)

        elif method == 'POST':
            response = requests.post('https://discord.com/api/v7' + path,
                                     headers=headers)

        elif method == 'PATCH':
            response = requests.patch('https://discord.com/api/v7' + path,
                                      headers=headers)

        elif method == 'PUT':
            response = requests.put('https://discord.com/api/v7' + path,
                                    headers=headers)

        elif method == 'HEAD':
            response = requests.head('https://discord.com/api/v7' + path,
                                     headers=headers)

        elif method == 'DELETE':
            response = requests.delete('https://discord.com/api/v7' + path,
                                       headers=headers)

    return response