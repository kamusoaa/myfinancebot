
import httpx
from fastapi import FastAPI, Request, Response

app = FastAPI()

URL_1C = "https://myfinances.1cmycloud.com/applications/k0zjava/api/telegramBot/messages/"
URL_TELEGRAM = "https://api.telegram.org"

@app.post("/proxy/v1/myfinancebot/tg-to-1c")
async def tg_to_1c(request: Request):

    body = await request.body()
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            URL_1C,
            content=body,
            headers={"Content-Type": request.headers.get("Content-Type", "application/json")}
        )
        return Response(content=response.content, status_code=response.status_code)

@app.post("/proxy/v1/myfinancebot/proxy/1c-to-tg")
async def one_c_to_tg(request: Request):

    # Чтобы не усложнять, 1С должна слать запрос на:
    # /proxy/1c-to-tg?path=botTOKEN/sendMessage
    
    path = request.query_params.get("path")
    body = await request.body()
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{URL_TELEGRAM}/{path}",
            content=body,
            headers={"Content-Type": "application/json"}
        )
        return Response(content=response.content, status_code=response.status_code)