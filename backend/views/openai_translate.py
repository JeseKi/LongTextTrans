from fastapi import HTTPException, Depends
from fastapi.responses import StreamingResponse
import base64

from translators.openaiTranslator import OpenAITranslator
from translators.types import OpenAITranslationRequest
from utils.formators import convert_to_list
from config import Config

class OpenAITranslateView:
    def __init__(self, openai_translator: OpenAITranslator, config: Config):
        self.openai_translator = openai_translator
        self.config = config

    async def translate(self, translation_request: OpenAITranslationRequest) -> StreamingResponse:
        # 检查是否提供了自定义的 API 密钥
        if translation_request.api_key and (translation_request.api_key != [""]):
            # 将逗号分隔的 API 密钥字符串转换为列表
            openai_keys = convert_to_list(translation_request.api_key)
            print("useUnlocal") # 使用非本地配置
        else:
            openai_keys = self.config.read_config()['OpenAIKey']
            print("useLocal") # 使用本地配置

        # 更新翻译器实例中的 API 密钥
        self.openai_translator.api_keys = openai_keys
        # 解码 Base64 编码的文本
        decoded_text = base64.b64decode(translation_request.text.encode()).decode()
        # 调用翻译器进行翻译并获取结果生成器
        result_generator = self.openai_translator.elementsTranslate(
            decoded_text,
            translation_request.source_lang,
            translation_request.target_lang,
            self.openai_translator.splitText,
            self.openai_translator._openai_translate,
            isStream=True,
            max_length=1000,
            model=translation_request.model
        )

        # 返回流式响应
        return StreamingResponse(result_generator)