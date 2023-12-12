import asyncio
from fastapi import FastAPI , File , UploadFile , APIRouter , Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse , JSONResponse
from fastapi.staticfiles import StaticFiles
from datetime import datetime
import chardet
import json

from translators.tencentTranslator import TencentTranslator
from translators.openaiTranslator import OpenAITranslator
from translators.types import TencentTranslationRequest, OpenAITranslationRequest
from config import Config
from utils.logger import Logger
from utils.mystream import MyStreamingResponse
from utils.file_processer import FileProcessor
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

@app.post("/upload/")
async def upload_file(request: Request, file: UploadFile = File(...), data: str = Form(...)):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    ip = request.client.host
    data_dict = json.loads(data)
    file_processor = FileProcessor(file, ip)
    
    file_name = file_processor.file_name
    
    if data_dict['service'] == "OpenAI":
        generater = file_processor.translate_and_append(OpenAITranslationRequest, data_dict, openai_translate_view.translate)
        async for result in generater:  # 直接迭代异步生成器
            data = json.loads(result)
            if data["have_done"] == 100:
                return {
                    "message": "OK",
                    "file_path": f'{file_name}{ip}{timestamp}'
                }
            
            return MyStreamingResponse(generater)

                
    # 处理完成后，发送一条消息回复
    return JSONResponse(content={"message": True})

# 流式测试
@app.get("/stream_test")
async def stream_messages() -> str:
    test_text = "test\n"
    async def gen() :
        for i in range(10):
            yield test_text
            await asyncio.sleep(1)
            i += 1
    print(type(gen()))
    return MyStreamingResponse(gen())

# 主页
@app.get("/")
async def index() -> None:
    return FileResponse("build/index.html")