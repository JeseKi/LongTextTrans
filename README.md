# 基于腾讯云机器翻译翻译API的web翻译程序 
## 特点
- 多语言
- 长文本
- 可托入文件进行翻译(仅支持纯文本文件)

前端使用React，后端则是使用了fastapi

## 使用
python版本 3.10
### Windows
1. 将relase中的`text_trans.zip`下载后在本地解压
2. 双击`run.bat`
3. 打开控制台中的链接
4. 输入自己的腾讯云ID和KEY即可使用(注意保存，避免下次重复输入)
### Linux
1. 将relase中的`text_trans.zip`下载后在本地解压
2. 在应用根目录下打开终端
3. 输入`chmod +x run.sh`并回车
4. 输入`./run.sh`并回车
5. 打开终端中的链接
6. 输入自己的腾讯云ID和KEY即可使用(注意保存，避免下次重复输入)
## TO DO LIST
- [x] 流式返回结果
- [ ] 增加翻译结果的保存
- [ ] 增加更多的可用API
  - [x] openai
  - [ ] 有道
  - [ ] 谷歌
  - [ ] DeepL
- [ ] 可选择文件进行导入
- [ ] 支持PDF
- [ ] 优化UI