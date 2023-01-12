
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
        目标是实现服务器全链接(1/N)


## 🎉 available已实现
 - ipv4连接到求生之路2服务器并返回基本信息

## 📖 to do list可能会做
 - 求生之路2服务器查询玩家信息

## 👌 pip安装
        pip install VSQ


## 📖 use使用

函数包括

        get_server_info # 总信息 -> dict
        (ip : str , port : int , times : int = 60)
        ip:ipv4 ,port:端口号 , times 默认为60,也就是说一分钟内同时调用任意函数，服务器将使用第一次的缓存，这可以使得防止被当做DDOS

        header, protocol, name, map_, folder, game, appid, players, max_players, bots, server_type, environment, visibility, vac, version, edf
        # 分别代表服务器返回的参数


## 🍻 exemple示例代码

    如果我想要获取服务器名字/地图/玩家数量
        from VSQ import l4d2
        ip:str = '127.0.0.1' 
        port:int = 20715 
        name = l4d2.name(ip,port)
        map_ = l4d2.map_(ip,port)
        players = l4d2.players(ip,port)
        print(name)
        print(map_)
        print(players)
    
    如果我想要获取服务器所有信息的字典（所有的键在上面，其中edf是bytes类，后面还有额外的附带信息所以有21个键对，如果有需求可以看源代码
        from VSQ import l4d2
        ip:str = '127.0.0.1' 
        port:int = 20715 
        server_dict = l4d2.get_server_info(ip,port)
        print(server_dict)

## 🌐 Communicate with me联系我

    email:Z735803792@163.com