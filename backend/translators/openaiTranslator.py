from openai import OpenAI , OpenAIError 
import asyncio
from collections import deque
from datetime import datetime
import re
import json
import time

from .translator import Translator
from utils.logger import Logger

class OpenAITranslator(Translator):
    def __init__(self,
                 api_keys: list
                 ) -> None:
        super().__init__()
        self.api_keys = api_keys
        self.pattern = r"Error code: (\d+)"
        self.logger = Logger()
        
    async def _openai_translate(self, 
                                content: str, 
                                source_lang: str, 
                                target_lang: str = 'zh', 
                                model: str = 'gpt-3.5-turbo',
                                rpm: int = 3
                                ) -> dict:
        
        api_key_index = 0  # 从第一个 API 密钥开始
        request_times = deque(maxlen=rpm)
        error_code_list = []
        re_count = 0 # 重试次数
        self.info = ""
        
        while True:  # 持续尝试，直到翻译成功或所有密钥失败
            api_key = self.api_keys[api_key_index]
            current_time = datetime.now()

            # 速率限制：如果达到最大请求数，请等待再重试
            if len(request_times) == 3 and (current_time - request_times[0]).total_seconds() < 60:
                await asyncio.sleep(60 - (current_time - request_times[0]).total_seconds())

            try:
                client = OpenAI(api_key=api_key)
                # 创建一个用于翻译的流
                stream = client.chat.completions.create(
                    model=model,
                    messages=[
                        {'role': 'system', 'content': 'You are a professional, authentic translation engine, only returns translations.'},
                        {'role': 'user', 'content': f'Translate the text from {source_lang} to {target_lang} Language, please do not explain my original text.:{content}'}
                    ],
                    temperature=0,
                    stream=True
                )
                
                for chunk in stream:
                    await asyncio.sleep(0)  # 让出控制权以允许其他任务运行
                    if hasattr(chunk.choices[0].delta, 'content'):
                        content = chunk.choices[0].delta.content
                        if content is not None:
                            yield {
                                'message': True,
                                'content': content,
                                'info': self.info
                            }
                            
                self.info = ""
                request_times.append(current_time)
                break  # 成功执行后退出循环

            except OpenAIError as e:
                error_message = str(e)
                print(f"密钥{api_key}发生错误：{error_message}\n")

                # 使用正则表达式提取错误代码
                match = re.search(r"Error code: (\d+)", error_message)
                if match:
                    error_code = int(match.group(1))
                    error_code_list.append(error_code) # 添加出现的错误代码
                    print(f"已添加错误码{error_code}")
                    
                    # 处理特定的错误代码
                    if error_code == 402:
                        self.logger.event_time_log(f"API: \"{api_key}\"余额不足，请检查")
                        
                    elif error_code == 401:
                        # 如果警告消息不存在，则添加警告消息
                        if f'[WARNNING]API\n\"{api_key}\"\n不正确，请检查您的API' not in self.info:
                            self.info += f'[WARNNING]API\n\"{api_key}\"\n不正确，请检查您的API\n\n'
                            
                    elif error_code == 429:
                        if f"[WARNNING]API\n\"{api_key}\n{e}\"" not in self.info:
                            self.info += f"[WARNNING]API\n\"{api_key}\n{e}\""
                    api_key_index = (api_key_index + 1) % len(self.api_keys)  # 切换到下一个密钥
                if api_key_index == 0:
                    re_count += 1
                    # 最多重试2倍密钥数量次
                    if re_count >= 2 * len(self.api_keys):
                        yield {
                            'message': False,
                            'err': '遍历两次密钥重试均失败，请检查您的API',
                            'info': self.info
                        }
                        break
                    
                # 如果再次到达第一个密钥, 并且错误代码中有419且没有429，则在重试之前等待一段时间
                if api_key_index == 0 and 419 in error_code_list and 429 not in error_code_list:
                    await asyncio.sleep(60)