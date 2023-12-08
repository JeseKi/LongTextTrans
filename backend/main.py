from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse , FileResponse
from fastapi.staticfiles import StaticFiles
import base64
import asyncio

from translators.tencentTranslator import TencentTranslator
from translators.openaiTranslator import OpenAITranslator
from translators.types import TencentTranslationRequest, OpenAITranslationRequest
from config import Config
from utils.logger import Logger
from views.openai_translate import OpenAITranslateView
from views.tencent_translate import TencentTranslateView

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)
app.mount("/static/", StaticFiles(directory="build/static/", html=True), name="static")

myConfig = Config() # 本地配置
logger = Logger() # 日志

# OpenAI类路由
openai_translator = OpenAITranslator(myConfig.read_config()['OpenAIKey'])
openai_translate_view = OpenAITranslateView(openai_translator, myConfig)

# 腾讯翻译类路由
tencent_translator = TencentTranslator(myConfig.read_config()['tencentCloudID'], myConfig.read_config()['tencentCloudKey'])
tencent_view = TencentTranslateView(tencent_translator, myConfig)

# 允许通过web端进行配置
# @app.post("/config")
# def config(tencent_id: str = "", tencent_key: str = "", openai_key: str = "") -> list:
#     result = myConfig.change_config(tencent_id, tencent_key, openai_key) # 更新配置文件
#     return result
    
# 调用腾讯翻译的API进行翻译
@app.post("/api/tencent_translate")
async def tencent_translate(translation_request: TencentTranslationRequest):
    return await tencent_view.translate(translation_request)

# 调用OpenAI的API进行翻译
@app.post("/api/openai_translate")
async def openai_translate(translation_request: OpenAITranslationRequest):
    return await openai_translate_view.translate(translation_request)

# 流式测试
# @app.get("/stream_test")
# async def stream_messages() -> str:
#     test_text = "test\n"
#     async def gen() :
#         for i in range(10):
#             yield test_text
#             await asyncio.sleep(1)
#             i += 1
#     print(type(gen()))
#     return StreamingResponse(gen())

# 主页
@app.get("/")
async def index() -> None:
    return FileResponse("build/index.html")