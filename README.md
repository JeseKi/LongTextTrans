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
2. 双击`run.bat`
3. 打开控制台中的链接
4. 在设置中输入自己的信息即可使用
### Linux
1. 将relase中的`text_trans.zip`下载后在本地解压
2. 在应用根目录下打开终端
3. 输入`chmod +x run.sh`并回车
4. 输入`./run.sh`并回车
5. 打开终端中的链接
6. 在设置中输入自己的信息即可使用

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
- [ ] 框架化
- [ ] 支持插件