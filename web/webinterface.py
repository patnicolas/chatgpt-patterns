__author__ = "Patrick Nicolas"
__copyright__ = "Copyright 2022, 23. All rights reserved."

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from chatgpt.chatgptclient import ChatGPTClient
from chatgpt.chatgptmonitor import ChatGPTMonitor


class WebInterface(object):
    """
        Singleton for Http interface for \GET and \POST. Note this is static and therefore does not
        need a constructor __init__
        @version 0.2
    """
    app = FastAPI()
    templates = Jinja2Templates(directory="../input")
    chat_gpt_model = "gpt-3.5-turbo"
    chat_gpt_temperature = 0
    chat_gpt_role = 'user'
    chat_gpt_client = ChatGPTClient.build(chat_gpt_model, chat_gpt_role, chat_gpt_temperature)
    chat_gpt_monitor = ChatGPTMonitor.build('monitor.txt')

    @staticmethod
    @app.get("/", response_class=HTMLResponse)
    async def root():
        with open("../input/request.html", 'r') as f:
            content = f.read()
        return content

    @staticmethod
    @app.post('/prompt', response_class=HTMLResponse)
    async def set_prompt(request: Request, fname: str = Form(...)):
        print(f'Prompt {fname}')
        # Invoke the ChatGPT service
        answer, num_tokens = WebInterface.chat_gpt_client.post(fname)
        # Update the count of tokens and cost/usage
        WebInterface.chat_gpt_monitor.update(num_tokens, WebInterface.chat_gpt_model , 'usage')
        # Return the
        return WebInterface.templates\
            .TemplateResponse("response.html", {"request": request, "response": answer})


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(WebInterface.app, host='localhost', port=8000)
