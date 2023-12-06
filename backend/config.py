import json
import os
with open('config.json', 'r', encoding='utf-8') as config_file:
    config = json.load(config_file)
ID = config["tencentCloudID"]
KEY = config["tencentCloudKey"]

class Config():
    def __init__(self) -> None:
        config_path = 'config.json'
        self.isChange = False
        self.changeLog = ""
        # 检查文件是否存在
        if not os.path.exists(config_path):
            # 如果文件不存在，创建一个新的配置文件
            self.config = {
                "tencentCloudID": "",
                "tencentCloudKey": "",
                "OpenAIKey": ""
            }
        else:
            with open('config.json', 'r', encoding='utf-8') as config_file:
                self.config = json.load(config_file)
    def change_config(self, tencent_id: str = "", tencent_key: str = "", openai_key = "") -> list:
        if tencent_id:
            self.config['tencentCloudID'] = tencent_id
            self.isChange = True
            self.changeLog += "腾讯云ID,"
        if tencent_key:
            self.config['tencentCloudKey'] = tencent_key
            self.isChange = True
            self.changeLog += "腾讯云KEY,"
        if openai_key:
            self.config['OpenAIKey'] = openai_key
            self.isChange = True
            self.changeLog += "OpenAIKEy,"
        with open('config.json', 'w', encoding='utf-8') as config_file:
            json.dump(self.config, config_file, indent=4)
        return [self.changeLog, self.isChange]
    
    def read_config(self) -> dict:
        return self.config