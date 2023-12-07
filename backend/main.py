from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse , FileResponse
from fastapi.staticfiles import StaticFiles
import base64
import asyncio

from translator.tencentTranslator import TencentTranslator
from translator.openaiTranslator import OpenAITranslator
from translator.types import TencentTranslationRequest, OpenAITranslationRequest
from config import Config
from utils.logger import Logger
from utils.mystream import MyStreamingResponse

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)
app.mount("/static/", StaticFiles(directory="build/static/", html=True), name="static")

myConfig = Config()
logger = Logger()

# 允许通过web端进行配置
@app.post("/config")
def config(tencent_id: str = "", tencent_key: str = "", openai_key: str = "") -> list:
    result = myConfig.change_config(tencent_id, tencent_key, openai_key) # 更新配置文件
    return result
    
# 腾讯翻译的API
@app.post("/api/tencent_translate")
async def tencent_translate(translation_request: TencentTranslationRequest) -> str:
    # 判断ID与KEY是否存在
    if (translation_request.ID != "") and (translation_request.Key != "") :
        tencent_config = {
            'tencentCloudID' : translation_request.ID,
            'tencentCloudKey' : translation_request.Key
        }
        print("useUnlocal")
    else :
        tencent_config = myConfig.read_config()
        print("useLocal")
    # 解码文本
    decoded_text = base64.b64decode(translation_request.text.encode()).decode()
    # 实例化腾讯云翻译器
    tencent_translator = TencentTranslator(tencent_config['tencentCloudID'], tencent_config['tencentCloudKey'])
    # 翻译
    result_generator = tencent_translator.elementsTranslate(
                decoded_text, 
                translation_request.source_lang, 
                translation_request.target_lang, 
                tencent_translator.splitText, 
                tencent_translator._tencentTranslate,
            )
    # 流式返回结果
    return MyStreamingResponse(result_generator)

# OpenAI的API
@app.post("/api/openai_translate")
async def openai_translate(translation_request: OpenAITranslationRequest) -> str:
    # 判断API是否存在
    if translation_request.api_key and (translation_request.api_key != [""]) :
        openai_keys = translation_request.api_key
        print("useUnlocal")
    else :
        openai_keys = myConfig.read_config()['OpenAIKey']
        print("useLocal")
    # 实例化OpenAI翻译器
    openai_translator = OpenAITranslator(openai_keys)
    # 解码文本
    decoded_text = base64.b64decode(translation_request.text.encode()).decode()
    # 翻译
    result_generator = openai_translator.elementsTranslate(
        decoded_text,
        translation_request.source_lang,
        translation_request.target_lang,
        openai_translator.splitText,
        openai_translator._openai_translate,
        isStream=True,
        max_length=1000,
        model = translation_request.model
    )
    
    print(type(result_generator))
    # 流式返回结果
    return MyStreamingResponse(result_generator)

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