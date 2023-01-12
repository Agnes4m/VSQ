
# VALVE-Server Queries
_✨基于与求生之路2服务器协议，一款可以查询求生服务器状态的库✨_
_✨Based on the agreement with the Left 4 Dead 2 server, a library that can query the status of the survival server.✨_

## pip安装
        pip install VSQ


## 使用

函数包括

        get_server_info # 总信息 -> dict
        header, protocol, name, map_, folder, game, appid, players, max_players, bots, server_type, environment, visibility, vac, version, edf
        # 分别代表服务器返回的参数


## 示例代码

    如果我想要获取服务器名字
        from VSQ import l4d2
        ip:str = '127.0.0.1' 
        port:int = 20715 
        name = l4d2.name(ip,port)
        print(name)

## 联系我

    email:Z735803792@163.com