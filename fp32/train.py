import time
import requests
from urllib.request import urlretrieve

from dreambooth import train

baseUrl = 'https://1337-sirajfarhan-sdbackend-apb8yr43sdm.ws-eu74.gitpod.io'

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

            requests.put(baseUrl + '/api/fine-tunes/' + str(instance['id']), json= { 'data': { 'status': 'completed' } })

        # train()


        break
    else:
        print('IP NOT FOUND')

    time.sleep(20)

    break



 
