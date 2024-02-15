import requests
import pyperclip
import dotenv
import os
import base64
import sys


if len(sys.argv) != 2:
    print('Usage: {} <filename>'.format(sys.argv[0]))
    sys.exit(1)

filename = sys.argv[1]

dotenv.load_dotenv()
api_key = os.getenv('APIKEY')

params = {'key': api_key}

with open(filename, 'rb') as img_file:
    encoded_img = base64.b64encode(img_file.read())

data = {'image': encoded_img}

url = 'https://api.imgbb.com/1/upload'

result = requests.post(url, params=params, data=data)

url = result.json()['data']['url']
pyperclip.copy(url)
print('{} copied to clipboard'.format(url))
