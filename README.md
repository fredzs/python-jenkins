update-config.py:利用jenkins的python插件，批量获取、更改所有job的配置文件，以实现修改“构建完成”后执行的js脚本
default-script:JavaScript脚本，发送原生get请求，利用jenkins的RESTful API，获取工程信息，在页面中获取DOM节点，动态增加显示内容。
configFiles:python脚本自动下载备份旧的配置文件

关于jenkins的api，请参阅官方文档，在任意项目url后加“/api”即可