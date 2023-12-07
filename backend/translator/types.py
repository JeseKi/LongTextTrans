from pydantic import BaseModel

class TencentTranslationRequest(BaseModel):
    text: str
    source_lang: str
    target_lang: str
    ID: str
    Key: str
    
class OpenAITranslationRequest(BaseModel):
    model: str
    text: str
    source_lang: str
    target_lang: str
    api_key: list