from fastapi import FastAPI, Request, Response
from ModuleImageWorking import *
from traceback import format_exc
import uvicorn

app = FastAPI()
serverData = {'img': None}

@app.post('/set-image')
async def setImage(request: Request):
    global serverData
    imgString = await request.body()
    try:
        serverData['img'] = decodeImage(imgString)
        return {'status': 200}
    except:
        return f'[ERROR]: {format_exc()}'

@app.get('/get-image')
async def getImage():
    global serverData
    try:
        img = encodeImage(serverData['img'])
        return Response(img)
    except:
        return f'[ERROR]: {format_exc()}'

if __name__ == '__main__':
    uvicorn.run('server:app', host='0.0.0.0', port=8080, reload=True, log_level='info', workers=5)