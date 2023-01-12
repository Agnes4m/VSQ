
# VALVE-Server Queries
_✨基于与求生之路2服务器协议，一款可以查询求生服务器状态的库✨_</b>
_✨Based on the agreement with the Left 4 Dead 2 server, a library that can query the status of the survival server.✨_

<a href="https://github.com/Umamusume-Agnes-Digital/VSQ/stargazers">
    <img alt="GitHub stars" src="https://img.shields.io/github/stars/Umamusume-Agnes-Digital/VSQ?color=%09%2300BFFF&style=flat-square">
</a>
<a href="https://github.com/Umamusume-Agnes-Digital/VSQ/issues">
    <img alt="GitHub issues" src="https://img.shields.io/github/issues/Umamusume-Agnes-Digital/VSQ?color=Emerald%20green&style=flat-square">
</a>

## Description说明
        


## 🎉 available已实现
 - ipv4连接到求生之路2服务器并返回基本信息

## 📖 to do list可能会做
 - 求生之路2服务器查询玩家信息

## 👌 pip安装
        pip install VSQ


## 📖 use使用

函数包括

        get_server_info # 总信息 -> dict
        (ip : str , port : int , time : int = 60)
        ip:ipv4

        header, protocol, name, map_, folder, game, appid, players, max_players, bots, server_type, environment, visibility, vac, version, edf
        # 分别代表服务器返回的参数


## 🍻 exemple示例代码

    如果我想要获取服务器名字
        from VSQ import l4d2
        ip:str = '127.0.0.1' 
        port:int = 20715 
        name = l4d2.name(ip,port)
        print(name)

## 🌐 Communicate with me联系我

    email:Z735803792@163.com