from fastapi import *

from fastapi.responses import *

# from pydantic import BaseModel

from mongoengine import *

import cfg

connect(**cfg.OSSdb)

app = FastAPI()

class FileStorage(Document):
    # fname = StringField()
    content = FileField()

@app.post('/upload')
async def upload_(authkey: str, f: UploadFile = File(...)):
    if authkey != cfg.upload_key:
        return HTTPException(401)
    fs = FileStorage()
    print(f.filename)
    print(f.content_type)
    
    
    fs.content.put(f.file)
    fs.save()
    return {'url': cfg.oss_host + 'download/' + str(fs.pk)}

    # bs = FileStorage(content=f.file.read())

@app.get('/download/{fspk}')
async def download_(fspk: str):
    fs = FileStorage.objects(pk=fspk).first()
    if not fs:
        return HTTPException(404)
    else:
        return Response(fs.content.read())

# uvicorn irori-OSS:app --host 0.0.0.0 --port 11111 --ssl-keyfile ssl/A.key --ssl-certfile ssl/A.crt
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)
