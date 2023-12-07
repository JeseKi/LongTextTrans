from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse , FileResponse
from fastapi.staticfiles import StaticFiles

from translator.tencentTranslator import TencentTranslator
from translator.openaiTranslator import OpenAITranslator
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
    if (translation_request.ID != "") and (translation_request.Key != "") :
        tencent_config = {
            'tencentCloudID' : translation_request.ID,
            'tencentCloudKey' : translation_request.Key
        }
        print("useUnlocal")
    else :
        tencent_config = myConfig.read_config()
        print("useLocal")
        
    tencent_translator = TencentTranslator(tencent_config['tencentCloudID'], tencent_config['tencentCloudKey'])
    result_generator = tencent_translator.elementsTranslate(
                translation_request.text, 
                translation_request.source_lang, 
                translation_request.target_lang, 
                tencent_translator.splitText, 
                tencent_translator._tencentTranslate
            )
    
    return StreamingResponse(result_generator)

@app.post("/api/openai_translate")
async def openai_translate(translation_request: OpenAITranslationRequest):
    if translation_request.api_key and (translation_request.api_key != [""]) :
        openai_keys = translation_request.api_key
        print("useUnlocal")
    else :
        openai_keys = myConfig.read_config()['OpenAIKey']
        print("useLocal")
        
    openai_translator = OpenAITranslator(openai_keys)
    result_generator = openai_translator.elementsTranslate(
        translation_request.text,
        translation_request.source_lang,
        translation_request.target_lang,
        openai_translator.splitText,
        openai_translator._openai_translate,
        isStream=True,
        max_length=2000,
        model = translation_request.model
    )
    
    return StreamingResponse(result_generator, media_type='text/plain')

@app.get("/")
async def index():
    return FileResponse("build/index.html")