from fastapi.responses import StreamingResponse
import base64
import asyncio

from translators.openaiTranslator import OpenAITranslator
from translators.types import OpenAITranslationRequest
from utils.formators import convert_to_list
from utils.mystream import MyStreamingResponse
from utils.file_processer import FileProcessor
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
        decoded_text = base64.b64decode(translation_request.content.encode()).decode()
        # 调用翻译器进行翻译并获取结果生成器
        result_generator = self.openai_translator.elementsTranslate(
            decoded_text,
            translation_request.source_lang,
            translation_request.target_lang,
            self.openai_translator.splitText,
            self.openai_translator._openai_translate,
            isStream=True,
            model=translation_request.model
        )

        return MyStreamingResponse(result_generator)
        
    async def file_translate(self, translation_request: OpenAITranslationRequest) -> StreamingResponse:
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
        
        decoded_text = translation_request.content
        # 调用翻译器进行翻译并获取结果生成器
        result_generator = self.openai_translator.elementsTranslate(
            decoded_text,
            translation_request.source_lang,
            translation_request.target_lang,
            self.openai_translator.splitText,
            self.openai_translator._openai_translate,
            isStream=True,
            model=translation_request.model,
        )

        async for data in result_generator:
            yield data