from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn


app = FastAPI()

md = {}

class Msg(BaseModel):
    m: str

@app.post('/i')
async def _(m: Msg):
    model = md['model']
    tk = md['tk']
    his = md['his'][:100]
    resp, nhis = model.chat(tk, m.m, history=his)
    print(resp)
    print(nhis)
    md['his'] = nhis
    return resp

if __name__ == "__main__":
    from transformers import AutoTokenizer, AutoModel
    tokenizer = AutoTokenizer.from_pretrained("THUDM/chatglm-6b", trust_remote_code=True)
    model = AutoModel.from_pretrained("THUDM/chatglm-6b", trust_remote_code=True).half().cuda()
    md['model'] = model
    md['tk'] = tokenizer
    md['his'] = []
    uvicorn.run(app, port=11111)