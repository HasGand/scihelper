# scihelper

> 方便的文献获取工具(webofscience & arXiv & sci-hub)


## 使用方法

```
scihelper -h 帮助信息
scihelper --help 帮助信息
scihelper [doi/serial] 根据传入的doi/serial下载文献
scihelper --arxiv [topic] 从arxiv获取相关主题的文献信息
scihelper --arxiv -d [topic] 从arxiv获取相关主题的文献信息并下载所有文献
scihelper --wos -link [topic] [link] 自行输入从webofscience获得的搜索页面的网址
scihelper --wos -link -d [topic] [link] 自行输入从webofscience获得的搜索页面的网址并下载所有文献
scihelper --wos [topic] 从webofscience获取相关主题的文献信息并下载所有文献
scihelper --wos -d [topic] 从webofscience获取相关主题的文献信息并下载所有文献
scihelper -d <ditems file> 从规定格式的文件(参考ditems目录下文件)中批量下载文献pdf
scihelper <ditems file> 从规定格式的文件(参考ditems目录下文件)中批量下载文献pdf
```