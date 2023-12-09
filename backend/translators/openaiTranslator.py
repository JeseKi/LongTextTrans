from openai import OpenAI , OpenAIError
import time

from .translator import Translator

class OpenAITranslator(Translator):
    def __init__(self,
                 api_keys: list
                 ) -> None:
        super().__init__()
        self.api_keys = api_keys
        self.isReponsed = False
        
    async def _openai_translate(self, 
                                text: str, 
                                source_lang:str,
                                target_lang: str, 
                                model: str) -> dict:
        
        for api_key in self.api_keys:
            try:
                client = OpenAI(api_key=api_key)
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {'role': 'system', 'content': 'You are a professional, authentic translation engine, only returns translations.'},
                        {'role': 'user', 'content': f'Translate the text from {source_lang} to {target_lang} Language, please do not explain my original text.:{text}'}
                    ],
                    temperature=0
                )
                self.isReponsed = True
                return {
                    "message": self.isReponsed,
                    'content': f"{response.choices[0].message.content}"
                }

            except OpenAIError as e:
                print(f"An error occurred with key {api_key}: {str(e)}\n")

        # 如果所有的 API 都尝试过后还是没有响应，则返回错误信息
        if not self.isReponsed:
            return {
                "message": self.isReponsed,
                "err": "您提供的全部API均失效，请检查您所设置的API\n"
            }
