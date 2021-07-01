import requests
import json
import os.path

model_id = "7ed7a301-a1f4-4569-a64e-ada51a943af3"
api_key = "8L-9tbv6fKmyptHc8ZJ9DYDv8loZwYyw"

url = 'https://app.nanonets.com/api/v2/ObjectDetection/Model/' + model_id + '/LabelFile/'

for i in os.listdir("plates/"):
    data = {'file': open(os.path.join("plates/",i), 'rb'),    'modelId': ('', model_id)}
    response = requests.post(url, auth=requests.auth.HTTPBasicAuth(api_key, ''), files=data)
    try:
        y = json.loads(response.text)
        print(f"{i}: ",y['result'][0]['prediction'][0]['ocr_text'])
    except:
        print("Error: {}".format(i))