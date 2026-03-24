import httpx
import logging
from fastapi import FastAPI, Request, Response

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ProxyBot")

app = FastAPI()

URL_1C = "https://myfinances.1cmycloud.com/applications/k0zjava/api/telegramBot/messages/"
URL_TELEGRAM = "https://api.telegram.org"

@app.post("/proxy/tg-to-1c")
async def tg_to_1c(request: Request):

    body = await request.body()
    
    logger.info("--- ВХОДЯЩИЙ ИЗ TG ---")
    logger.info(f"Body: {body.decode('utf-8', errors='ignore')}")

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                URL_1C,
                content=body,
                headers={"Content-Type": "application/json"},
                timeout=20.0
            )
            logger.info(f"Ответ от 1С: {response.status_code}")
            return Response(content=response.content, status_code=response.status_code)
        except Exception as e:
            logger.error(f"Ошибка связи с 1С: {e}")
            return {"error": "1C_UNREACHABLE", "details": str(e)}

@app.post("/proxy/1c-to-tg")
async def one_c_to_tg(request: Request):

    # 1С должна передать в параметрах путь, например: ?path=botTOKEN/sendMessage
    path = request.query_params.get("path")
    body = await request.body()
    
    logger.info(f"--- ИСХОДЯЩИЙ ИЗ 1С (Путь: {path}) ---")
    logger.info(f"Body: {body.decode('utf-8', errors='ignore')}")

    if not path:
        return {"error": "MISSING_PATH_PARAMETER"}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{URL_TELEGRAM}/{path}",
                content=body,
                headers={"Content-Type": "application/json"},
                timeout=20.0
            )
            logger.info(f"Ответ от Telegram: {response.status_code}")
            return Response(content=response.content, status_code=response.status_code)
        except Exception as e:
            logger.error(f"Ошибка связи с Telegram: {e}")
            return {"error": "TG_UNREACHABLE", "details": str(e)}