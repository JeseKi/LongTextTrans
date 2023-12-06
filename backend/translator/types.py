from pydantic import BaseModel

class TencentTranslationRequest(BaseModel):
    text: str
    source_lang: str
    target_lang: str
    
class OpenAITranslationRequest(BaseModel):
    text: str
    source_lang: str
    target_lang: str
    api_key: str