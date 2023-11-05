from modules.kerasWorking import signDetector
from modules.imageWorking import *
from fastapi import FastAPI, Request
from traceback import format_exc
import uvicorn

sd = signDetector('traficSignModel/keras_model.h5', 'traficSignModel/labels.txt')
app = FastAPI()

@app.post('/get-object')
async def getObject(request: Request):
    imgString = await request.body()
    try:
        img = decodeImage(imgString)
        classObject, scoreObject = sd.findObjects(img)
        return {'class': classObject, 'score': scoreObject}
    except:
        return f'[ERROR]: {format_exc()}'

if __name__ == '__main__':
    uvicorn.run('ex2-server:app', host='0.0.0.0', port=8080, reload=True, log_level='info', workers=5)
