import socket
import struct
import time

cache = {}
tu_title = ('header', 'protocol', 'name', 'map_', 'folder', 'game', 'appid', 'players', 'max_players', 'bots', 'server_type', 'environment', 'visibility', 'vac', 'version', 'edf')


def server_info(
    ip:str, 
    port:int
    ) -> bytes:
    """send message/back bytes"""
    address = (ip, port)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(5)
    #send request for server info 
    header = b'\xFF\xFF\xFF\xFF'
    packet = b'\x54Source Engine Query\x00'
    try:
        s.sendto(header+packet, address)
        data, _ = s.recvfrom(1024)
    except socket.timeout:
        print("Timeout Occured")
        return
    if not data.startswith(header):
        print("Invalid Response")
        return
    # check if the response contains challenge number
    if data[4] == 65:
        """challenge_number"""
        challenge_number = data[5:]
        packet = header + packet + challenge_number
        struct.unpack('<L', challenge_number)
        s.sendto(packet, address)
        data, _ = s.recvfrom(1024)
    if data[4] == 73:
        print('Server info received')
        data = data[4:]
    elif data == b'A':
        print("Server is using Challenge Number")
    else:
        print("Invalid Response")
    s.close()
    # print(len(data))
    return data

def unpack_info(data) -> list:
        '''
        byte	8 bit character or unsigned integer \n
        short	16 bit signed integer \n
        long	32 bit signed integer \n
        float	32 bit floating point \n
        long long	64 bit unsigned integer \n
        string	variable-length byte field, encoded in UTF-8, terminated by 0x00 \n
        '''
        """PLAN A"""
        # message = struct.unpack('<b b 35x 13x 12x 14x h b b b c c b b 8x 46x', data)
        # ('<b b 20s 16s 20s 20s h b b b c c b 20s b', data[5:])
        # header, protocol, name, map_, folder, /game, appid, players, max_players, bots, /server_type, environment, visibility, vac, version, /edf  = struct.unpack('<b b 35s 13s 12s 14s h b b b c c b b 8s 46s', data)
        # val = struct.unpack('!i', data)
        # print(val)
        """PLAN B"""
        n:int = 0 # time
        sock:int = 0 # order
        msg = []
        for n in range(1,17):
            if n in [1,2,8,9,10,11,12,13,14]: # byte
                new = struct.unpack('<b', bytes([data[sock]]))
                msg.append(new[0])
                sock += 1
            if n in [7]: # short
                new = struct.unpack('<h',bytes(data[sock:sock+2]))
                msg.append(new[0])
                sock += 2
            # if n in [17]: # long long
            #     new = struct.unpack('<c',bytes(data[s:s+8]))
            #     msg.append(new[0])
            #     s += 8
            if n in [3,4,5,6,15,16]: # string-check the len
                new,data_len =check_string(data,sock)
                msg.append(new)
                main_log = sock
                sock = sock + data_len + 1
            # print('第',n,'次值为：',sock)
        return [msg,main_log]



def dict_info(msg:list) ->dict:
    tu_info = (header, protocol, name, map_, folder, game, appid, players, max_players, bots, server_type, environment, visibility, vac, version, edf) = msg
    msg_dict = {} 
    for i in range(15):
        try:
            tu_info[i] = tu_info[i].decode()
        except (AttributeError,UnicodeDecodeError):
            pass
        finally:
            tu_info[i] = str(tu_info[i])
        msg_dict.update({tu_title[i]:tu_info[i]})
    msg_dict.update({tu_title[15]:tu_info[15]})
    # print(msg_dict)
    return msg_dict

def edf_split(msg_dict:dict,data,main_len:int) -> dict:
    a = ['port','steam_id','spectator_port','spectator_name','Keywords','GameID']
    edf = msg_dict['edf']
    edf = int.from_bytes(edf, byteorder='little')
    offset = main_len
    # print(offset)
    if edf & 0x80 :
        port:str = struct.unpack('<H', data[offset:offset+2])
        msg_dict.update({a[0]:port})
    offset += 2
    if edf & 0x10:
        steam_id:str = struct.unpack('<Q', data[offset:offset+8])
        msg_dict.update({a[1]:steam_id})
    offset += 8
    if edf & 0x40:
        spectator_port, = struct.unpack('<H', data[offset:offset+3])
        msg_dict.update({a[2]:spectator_port})
        offset += 2
        new,data_len =check_string(data,offset)
        spectator_name:str  = new
        msg_dict.update({a[3]:spectator_name.decode()})
        offset += data_len
    if edf & 0x20:
        new,data_len =check_string(data,offset)
        Keywords:str = new
        msg_dict.update({a[4]:Keywords.decode()})
        offset += data_len
    if edf & 0x01:
        GameID:str = struct.unpack('<Q', data[offset:offset+8])
        msg_dict.update({a[1]:GameID})
        offset += data_len
    # print(msg_dict)
    return msg_dict
    
    
    

"""
print("3、Server Name: ", name.decode('utf-8'))
print("4、Map: ", map_.decode('utf-8'))
print("5、Folder: ", folder.decode('utf-8',errors='ignore'))
print("6、Game: ", game.decode('utf-8',errors='ignore'))
print('7、appid: ',appid)
print("8、Players: ", players)
print("9、Maximum Players: ", max_players)
print("10、Bots: ",bots)
print("11、Server type: ", server_type)
print("12、Environment: ",environment)
print("13、Visibility: ",visibility)
print("14、Vac: ",vac)
print("15、Server version: ",version.decode())
"""


def check_string(data:bytes,sock:int) -> list:
    """check len(string)"""
    data_this = data[sock:]
    data_right = data_this.split(b'\x00')
    data_len = len(data_right[0])
    tag = '<'+str(data_len)+'s'
    new = struct.unpack(tag,bytes(data[sock:sock+data_len]))
    return [new[0],data_len]


def get_server_info(ip:str, port:int,times) -> dict:
    """ip to dict"""
    if (ip, port) in cache:
        # check if the cache is still fresh
        if time.time() - cache[(ip, port)]['timestamp'] < times:
            return cache[(ip, port)]['message']
    data = server_info(ip, port)
    data_list,data_len = unpack_info(data)
    message = edf_split(dict_info(data_list),data,data_len)
    # print(message)
    cache[(ip, port)] = {'message': message, 'timestamp': time.time()}
    return message

        # header, protocol, name, map_, folder, /game, appid, players, max_players, bots, /server_type, environment, visibility, vac, version, /edf  = struct.unpack('<b b 35s 13s 12s 14s h b b b c c b b 8s 46s', data)

def header(ip,port,times:int = 60):
    return get_server_info(ip, port,times)['header']

def protocol(ip,port,times:int = 60):
    return get_server_info(ip, port,times)['protocol']

def name(ip,port,times:int = 60):
    return get_server_info(ip, port,times)['name']

def map_(ip,port,times:int = 60):
    return get_server_info(ip, port,times)['map_']

def folder(ip,port,times:int = 60):
    return get_server_info(ip, port,times)['folder']

def appid(ip,port,times:int = 60):
    return get_server_info(ip, port,times)['appid']

def players(ip,port,times:int = 60):
    return get_server_info(ip, port,times)['players']

def max_players(ip,port,times:int = 60):
    return get_server_info(ip, port,times)['max_players']

def server_type(ip,port,times:int = 60):
    return get_server_info(ip, port,times)['server_type']

def environment(ip,port,times:int = 60):
    return get_server_info(ip, port,times)['environment']

def visibility(ip,port,times:int = 60):
    return get_server_info(ip, port,times)['visibility']

def vac(ip,port,times:int = 60):
    return get_server_info(ip, port,times)['vac']

def version(ip,port,times:int = 60):
    return get_server_info(ip, port,times)['version']

def version(ip,port,times:int = 60):
    return get_server_info(ip, port,times)['version']

def edf(ip,port,times:int = 60):
    return get_server_info(ip, port,times)['edf']
    
# for variable in tu_title:
#     locals()[variable] = lambda ip,port: get_server_info(ip,port)[variable]