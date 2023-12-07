import json
import os

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
        """
        更新配置文件并记录更改日志。

        该方法接受三个可选参数（tencent_id, tencent_key, openai_key），用于更新配置文件。
        如果传入参数，则相应的配置项会被更新。同时，更改的配置项会被记录在日志中。
        
        参数:
            tencent_id (str): 腾讯云ID，如果提供，将更新配置文件中的对应项。
            tencent_key (str): 腾讯云密钥，如果提供，将更新配置文件中的对应项。
            openai_key (str): OpenAI 密钥，如果提供，将更新配置文件中的对应项。

        返回:
            list: 包含两个元素的列表。第一个元素是更改日志的字符串，第二个元素是布尔值，表示是否有更改发生。
        """
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
        with open('config.json', 'r', encoding='utf-8') as config_file:
            self.config = json.load(config_file)
            
        return self.config