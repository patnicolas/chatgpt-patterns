__author__ = "Patrick Nicolas"
__copyright__ = "Copyright 2022, 23. All rights reserved."

from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


app = FastAPI()
templates = Jinja2Templates(directory="../input")


@app.get("/", response_class=HTMLResponse)
async def root():
    with open("../input/request.html", 'r') as f:
        content = f.read()
    return content


@app.post('/prompt')
async def set_prompt(fname: str = Form(...)):
    print(f'Prompt {fname}')
    return templates.TemplateResponse("response.html", {"request": fname, "response": "This is the output"})


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='localhost', port=8000)
