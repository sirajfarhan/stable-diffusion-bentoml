import time
import requests
from urllib.request import urlretrieve
import shutil

from dreambooth import train

baseUrl = 'http://54.193.141.160:1337'

while True:
    ipAddress = requests.request('GET', 'https://api.ipify.org').text

    url = baseUrl + '/api/fine-tunes?populate[inputImages][fields][1]=url&filters[ipAddress][$eq]=' + ipAddress + '&filters[status][$eq]=initiated'

    response = requests.request('GET', url).json()

    

    if len(response['data']) > 0:
        instance = response['data'][0]
        requests.put(baseUrl + '/api/fine-tunes/' + str(instance['id']), json= { 'data': { 'status': 'processing' } })
        
        input_images = response['data'][0]['attributes']['inputImages']['data']

        for input_image in input_images:
            url = input_image['attributes']['url']

            urlretrieve(url, './training/' + url.split('/')[len(url.split('/'))-1])

        train()

        # shutil.make_archive('./models/v1_5', 'zip', './models/v1_5')

        # files = {'files': ('v1_5.zip', open('./models/v1_5.zip', 'rb'))}
        # response = requests.post(baseUrl + '/api/upload', files=files)

        # requests.put(baseUrl + '/api/fine-tunes/' + str(instance['id']), json= { 'data': { 'status': 'completed', 'fineTunedModel':  response.json()[0]['id'] } })

        break
    else:
        print('IP NOT FOUND')

    time.sleep(20)

    break



 
