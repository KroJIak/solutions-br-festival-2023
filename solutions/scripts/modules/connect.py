from imageWorking import *
import requests

class connectGetTrackingObjects():
    def __init__(self, host='localhost', port=8080):
        if host == 'localhost': self.host = f'http://127.0.0.1:{port}/'
        else: self.host = host
        self.postEndpoint = 'get-object'

    def postImage(self, img):
        imgString = encodeImage(img)
        try:
            response = requests.post(url=f'{self.host}{self.postEndpoint}', data=imgString)
            if response.status_code != 200:
                print(f'Bad code: {response.status_code}')
                return None
        except:
            print('Bad connection')
            return None
        return response.content
