from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse , FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

from translator.tencentTranslator import Translator
from translator.types import TencentTranslationRequest, OpenAITranslationRequest
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

@app.post("/config")
def config(tencent_id: str = "", tencent_key: str = "", openai_key: str = "") -> list:
    result = myConfig.change_config(tencent_id, tencent_key, openai_key) # 更新配置文件
    return result
    
@app.post("/api/tencent_translate")
async def tencent_translate(translation_request: TencentTranslationRequest):
    tencent_config = myConfig.read_config()
    tencent_translator = Translator(tencent_config['tencentCloudID'], tencent_config['tencentCloudKey'])
    result = tencent_translator.elementsTranslate(
                translation_request.text, 
                translation_request.source_lang, 
                translation_request.target_lang, 
                tencent_translator._splitText, 
                tencent_translator._tencentTranslate
            )
    return StreamingResponse(result)

@app.post("api/openai_translate")
async def openai_translate(translation_request: OpenAITranslationRequest):
    pass

@app.get("/")
async def index():
    return FileResponse("build/index.html")