from typing import List ,Callable
import time

import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.tmt.v20180321 import tmt_client, models

from utils.logger import Logger

logger = Logger()

class Translator():
    def __init__(
                 self, 
                 ID: str, 
                 KEY: str, 
                 region: str = "ap-beijing"
                 ):
        self.ID = ID
        self.KEY = KEY
        self.region = region

    def elementsTranslate(
                          self,
                          text: str, 
                          source_lang: str,
                          target_lang: str,
                          split_callback: Callable[[str], List[str]], # 多数翻译API都限制单次请求的文本长度
                          translate_callback: Callable[[str, str, str], str],# 翻译API,需传入源文本,源语言,目标语言参数
                        ):
        """
        将字符串进行翻译,并以流式返回结果
        参数:
        - text: 需要进行翻译的字符串
        - source_lang: 源语言
        - target_lang: 目标语言
        - split_callback: 用于分割字符串的回调函数
        - translate_callback: 用于翻译字符串的回调函数
        :return: 流式结果
        """
        i = 0
        for element in split_callback(text):
            yield translate_callback(element, source_lang, target_lang)
            # 日志
            i += 1
            logger.event_time_log(f"向服务端发送请求第{i}次",False)
            # time.sleep(1)

    def _splitText(self,text: str) -> List[str]:
        """
        分割字符串
        参数:
        - text: 字符串
        :return: 分割后的每个元素均符合长度的字符串数组
        """
        # 计算文本长度
        text_length = len(text)
        text_segments = []
        MAX_LENGTH = 5500
        # 根据文本长度计算需要分成几部分，使用天花板除法确保分割完全
        num_partitions = -(-text_length // MAX_LENGTH)
        
        # 如果文本已经足够短，不需要分割，直接返回包含原文本的列表
        if num_partitions == 1:
            return [text]
        
        last_split_point = 0  # 上一次分割点的索引
        for i in range(1, num_partitions):
            # 计算每一部分的理论分割长度
            partition_length = i * text_length // num_partitions
            # 在分割点前找最近的句号，保证句子完整性
            period_index = text.rfind('.', last_split_point, partition_length)
            
            # 如果找不到句号，就在计算出的分割点长度处直接分割
            if period_index == -1:
                split_point = partition_length
            else:
                # 如果找到了句号，分割点后移一位，包含句号
                split_point = period_index + 1
            
            # 打印分割点信息，用于调试
            start = max(0, split_point - 10)  # 确保开始不会低于文本开头
            end = min(len(text), split_point + 10)  # 确保结束不会超过文本结尾
            print(f"Splitting at position {split_point}: {text[start:split_point]}|{text[split_point:end]}...")
            
            # 将当前分割的文本段添加到段列表中
            text_segments.append(text[last_split_point:split_point])
            last_split_point = split_point  # 更新上一次分割点的索引
        
        # 将最后剩余的文本作为最后一个段落添加到列表中
        text_segments.append(text[last_split_point:])
        
        return text_segments  # 返回分割后的文本段列表

    def _tencentTranslate(
                          self,
                          text: str, 
                          source_lang: str, 
                          target_lang: str,
                        ) -> str:
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
            return result
            
        except TencentCloudSDKException as err:
            # 捕获并打印异常
            print(err)
            # 如果调用API过程中发生异常，则返回原始文本段
            return text