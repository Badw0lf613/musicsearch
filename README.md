# 华语乐坛问答系统
## 上海大学语义网络与知识图谱课程项目（已施工完毕）
### 相关依赖（pip安装即可）
&emsp;&emsp;Django==2.1<br>
&emsp;&emsp;py2neo==4.3.0
### 使用说明
&emsp;&emsp;首先需要配置neo4j并建库，查阅相关教程即可，通过形如本项目文件match.py中的<br>
graph = Graph('http://localhost:7474', username='你的用户名', password='你的密码')<br>
来进行连接。<br>
&emsp;&emsp;其次，数据库会保存在本地，形如以下路径<br>
&emsp;&emsp;D:\Program Files (x86)\neo4j-community-3.5.22-windows\neo4j-community-3.5.22\data<br>
若套用本项目的数据，将根目录下的data.zip解压并替换即可。<br>
&emsp;&emsp;最后，终端输入python manage.py runserver或右上角绿色三角运行项目即可在 http://127.0.0.1:8000/ 看到内容。
