from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse , FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

from translator.translator import Translator
from config import Config

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有头部
)
app.mount("/static/", StaticFiles(directory="build/static/", html=True), name="static")

myConfig = Config()
tencent_translator = Translator(myConfig.read_config()['tencentCloudID'], myConfig.read_config()['tencentCloudKey'])

@app.post("/config")
def config(tencent_id: str = "", tencent_key: str = "", openai_key: str = ""):
    
    pass

@app.get("/api/tencent_translate")
async def tencent_translate(text: str, source_lang: str, target_lang: str):
    result = tencent_translator.elementsTranslate(text, source_lang, target_lang, tencent_translator._splitText, tencent_translator._tencentTranslate)
    return StreamingResponse(result)

@app.get("/")
async def index():
    return FileResponse("build/index.html")