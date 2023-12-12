import chardet
from datetime import datetime
from fastapi import UploadFile
from pydantic import BaseModel
from typing import Type, AsyncGenerator
import json

class FileProcessor:
    """
    文件处理器类,作为中间件，处理上传文件的编码转换和翻译保存。
    """

    def __init__(self, file: UploadFile, request_ip: str):
        self.file = file
        self.request_ip = request_ip
        self.timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        self.file_name = self.create_unique_filename()
        self.content = ""
        
    def create_unique_filename(self):
        """
        根据请求的IP地址和时间戳创建唯一的文件名。
        """
        return f"{self.file.filename}_{self.request_ip}_{self.timestamp}"

    async def process_file(self):
        """
        处理上传的文件，检测并转换编码为UTF-8。
        返回处理后的文件内容和新的文件名。
        """
        origin_content = await self.file.read()
        encoding = chardet.detect(origin_content)['encoding']

        # 如果检测到的编码不是utf-8，则转换编码
        if encoding and encoding.lower() != 'utf-8':
            self.content = origin_content.decode(encoding, 'replace').encode('utf-8')
        else:
            self.content = origin_content
    
    async def translate_and_append(
        self, 
        request_type: Type[BaseModel], 
        request: dict, 
        translate_callback
    ) -> AsyncGenerator:
        """
        处理翻译请求，将结果追加到文件中。
        :param service: 服务类型
        :param request_type: 请求类型，继承自BaseModel的类
        :param request: 请求数据
        :param translate_callback: 翻译回调函数
        :return: 异步生成器，生成翻译进度
        """
        # 构建翻译请求
        await self.process_file() # 加载文件内容
        
        request['content']= self.content
        request_translate = request_type(**request) 
        result_generator = translate_callback(request_translate)
        
        async for origin_data in result_generator:
            data = json.loads(origin_data)
            context = json.loads(data["context"])
            if context["message"] == True:
                with open(f"./temp_files/{self.file_name}", 'a', encoding='utf-8') as f:
                    result = context["content"]
                    f.write(result)
                    
            yield origin_data