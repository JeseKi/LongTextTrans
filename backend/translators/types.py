from pydantic import BaseModel

class TencentTranslationRequest(BaseModel):
    text: str
    source_lang: str
    target_lang: str
    ID: str | None
    Key: str | None
    
class OpenAITranslationRequest(BaseModel):
    model: str
    text: str
    source_lang: str
    target_lang: str
    api_key: str | None
    rpm : int | None