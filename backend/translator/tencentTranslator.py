import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.tmt.v20180321 import tmt_client, models

from utils.logger import Logger
from .translator import Translator

logger = Logger()

class TencentTranslator(Translator):
    def __init__(
                 self, 
                 ID: str = "", 
                 KEY: str = "", 
                 region: str = "ap-beijing"
                 ):
        super().__init__()
        self.ID = ID
        self.KEY = KEY
        self.region = region

    async def _tencentTranslate(
                          self,
                          text: str, 
                          source_lang: str, 
                          target_lang: str,
                        ) -> dict:
        """
        翻译字符串
        参数:
        text: 字符串
        source_lang: 源语言
        target_lang: 目标语言
        :return:翻译后的字符串
        """
        try:
            # 使用传入的ID和KEY创建腾讯云API的凭证
            cred = credential.Credential(self.ID, self.KEY)
            # 创建HTTP配置
            httpProfile = HttpProfile()
            httpProfile.endpoint = "tmt.tencentcloudapi.com"
            # 创建客户端配置
            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            # 创建翻译服务的客户端
            client = tmt_client.TmtClient(cred, self.region, clientProfile)

            # 创建翻译请求对象，并设置所需的参数。
            req = models.TextTranslateRequest()
            params = {
                "SourceText": text,  # 需要翻译的文本
                "Source": source_lang,  # 源语言代码
                "Target": target_lang,  # 目标语言代码
                "ProjectId": 0  # 项目ID，这里填写0即可，因为翻译API不需要项目ID
            }
            # 将参数转换为JSON字符串，并设置给请求对象
            req.from_json_string(json.dumps(params))
            # 调用翻译方法，并获取响应
            resp = client.TextTranslate(req)
            # 解析响应数据，获取翻译后的文本
            result = json.loads(resp.to_json_string())["TargetText"]
            return (
                {
                    "message" : True,
                    "content" : result
                }
            )
            
        except TencentCloudSDKException as err:
            # 捕获并打印异常
            print(err)
            # 如果调用API过程中发生异常，则返回原始文本段
            return (
                {
                    "message" : False,
                    "content" : str(err)
                }
            )