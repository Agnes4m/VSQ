<div align="center">

# VALVE-Server Queries
_✨基于与求生之路2服务器协议，一款可以查询求生服务器状态的库✨_

_✨Based on the agreement with the Left 4 Dead 2 server, a library that can query the status of the survival server.✨_

<a href="https://github.com/Umamusume-Agnes-Digital/VSQ/stargazers">
    <img alt="GitHub stars" src="https://img.shields.io/github/stars/Umamusume-Agnes-Digital/VSQ">
</a>
<a href="https://github.com/Umamusume-Agnes-Digital/VSQ/issues">
    <img alt="GitHub issues" src="https://img.shields.io/github/issues/Umamusume-Agnes-Digital/VSQ">
</a>

</div>
## Description说明
        目标是实现服务器全链接(1/N)


## 🎉 available已实现
 - ipv4连接到求生之路2服务器并返回基本信息
 - ipv4连接到求生之路2服务器并返回在线玩家信息

## 📖 to do list可能会做
 - 暂无

## 👌 pip安装
        pip install VSQ


## 📖 use使用

函数包括

        # 总信息
        server  (ip : str , port : int , times = 60) -> dict
        ip:ipv4 ,port:端口号 , times 默认为60,也就是说一分钟内同时调用任意函数，服务器将使用第一次的缓存，这可以使得防止被当做DDOS
        # 格式 {'header':xx,'protocol':xxx,...}
        header, protocol, name, map_, folder, game, appid, players, max_players, bots, server_type, environment, visibility, vac, version, edf
        # 分别代表服务器返回的参数

---
        # 玩家信息
        players (ip : str , port : int , times = 60) -> dict:
        # 格式
        {
        'header':1,
        'Players':
            [{
                'Index':0,
                'Name':xxx,
                'Score':114514,
                'Duration':int but who care
            },
            {
                ...
            }
            ]
        }

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
        server_dict = l4d2.server(ip,port)
        print(server_dict)

        from VSQ import l4d2
        ip:str = '127.0.0.1' 
        port:int = 20715 
        players_data = l4d2.players(ip,port)
        players_number = players_data['header']
        for i in players_data['Players'][0]
            print('player_name',i['Name'])


## 🌐 Communicate with me联系我

    email:Z735803792@163.com