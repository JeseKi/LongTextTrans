# 长文本翻译web程序
## 特点
- 多语言
- 长文本
- 支持使用多个OpenAI的API,利用英文逗号作为分割
前端使用React，后端则是使用了fastapi

## 使用
python版本 3.10

### Windows
1. 将relase中的`text_trans.zip`下载后在本地解压
2. 在该目录下打开Powershell
2. 输入`cp config-template.json config.json`
3. 在`config.json`中填入自己的信息(假如打算在web页面中设置信息就可以不在这里填写)
4. 双击`run.bat`
5. 打开控制台中的链接
6. 在设置中输入自己的信息即可使用
### Linux
1. 将relase中的`text_trans.zip`下载后在本地解压
2. 在应用根目录下打开终端
3. 输入`cp config-template.json config.json`
4. 在`config.json`中填入自己的信息(假如打算在web页面中设置信息就可以不在这里填写)
5. 输入`chmod +x run.sh`并回车
6. 输入`./run.sh`并回车
7. 打开终端中的链接
8. 在设置中输入自己的信息即可使用
9. 
### `config.json`
```python
{
    "tencentCloudID": "id", # 腾讯云ID
    "tencentCloudKey": "key", # 腾讯云KEY
    "OpenAIKey" : [ # OpenAIKey
        "key1","key2","key3"
    ]
}
```

## TO DO LIST
- [x] 流式返回结果
- [x] 允许上传txt文件并保存翻译
- [ ] 增加更多的可用API
  - [x] 腾讯云
  - [x] openai
  - [ ] 有道
  - [ ] 谷歌
  - [ ] DeepL
- [ ] 支持PDF
- [ ] 优化UI
- [ ] 框架化
