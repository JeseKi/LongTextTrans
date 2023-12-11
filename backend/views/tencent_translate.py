from fastapi import HTTPException, Depends
from fastapi.responses import StreamingResponse
import base64
import json

from translators.tencentTranslator import TencentTranslator
from translators.types import TencentTranslationRequest
from config import Config
from utils.mystream import MyStreamingResponse

class TencentTranslateView:
    def __init__(self, tencent_translator: TencentTranslator, config: Config):
        self.tencent_translator = tencent_translator
        self.config = config

    async def translate(self, translation_request: TencentTranslationRequest) -> StreamingResponse:
        # 判断ID与KEY是否存在
        if (translation_request.ID) and (translation_request.Key):
            tencent_config = {
                'tencentCloudID': translation_request.ID,
                'tencentCloudKey': translation_request.Key
            }
            self.tencent_translator.ID = tencent_config["tencentCloudID"]
            self.tencent_translator.KEY = tencent_config["tencentCloudKey"]
            print("useUnlocal")
        else:
            tencent_config = self.config.read_config()
            self.tencent_translator.ID = tencent_config["tencentCloudID"]
            self.tencent_translator.KEY = tencent_config["tencentCloudKey"]
            print("useLocal")

        # 解码文本
        decoded_text = base64.b64decode(translation_request.text.encode()).decode()
        # 翻译
        result_generator = self.tencent_translator.elementsTranslate(
            decoded_text,
            translation_request.source_lang,
            translation_request.target_lang,
            self.tencent_translator.splitText,
            self.tencent_translator._tencentTranslate,
            isStream=False,
        )
        
        # 流式返回结果
        return MyStreamingResponse(result_generator, media_type="text/event-stream")
