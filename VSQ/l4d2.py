import socket
import struct


def get_server_info(ip, port):
    address = (ip, port)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(5)
    #send request for server info 
    header = b'\xFF\xFF\xFF\xFF'
    packet = b'\x54Source Engine Query\x00'
    try:
        s.sendto(header+packet, address)
        data, _ = s.recvfrom(1024)
        print('第一次返回')
        print(data)
    except socket.timeout:
        print("Timeout Occured")
        return
    if not data.startswith(header):
        print("Invalid Response")
        return
    # check if the response contains challenge number
    if data[4] == 65:
        challenge_number = data[5:]
        packet = header + packet + challenge_number
        struct.unpack('<L', challenge_number)
        s.sendto(packet, address)
        data, _ = s.recvfrom(1024)
        print('第二次返回')
    if data[4] == 73:
        data = data[4:]
        print(data)
        print(len(data))
        print('Server info received')
        '''
        byte	8 bit character or unsigned integer
        short	16 bit signed integer
        long	32 bit signed integer
        float	32 bit floating point
        long long	64 bit unsigned integer
        string	variable-length byte field, encoded in UTF-8, terminated by 0x00
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
        for i in data:
            n +=1
            if n in [1,2,8,9,10,11,12,13,14]: # byte
                new = struct.unpack('<b', bytes([data[sock]]))
                msg.append(new[0])
                sock += 1
                continue
            if n in [7]: # short
                new = struct.unpack('<h',bytes(data[sock:sock+2]))
                msg.append(new[0])
                sock += 2
                continue
            # if n in [17]: # long long
            #     new = struct.unpack('<c',bytes(data[s:s+8]))
            #     msg.append(new[0])
            #     s += 8
            if n in [3,4,5,6,15,16]: # string-check the len
                new,data_len =check_string(data,sock)
                msg.append(new)
                sock = sock + data_len + 1
        print(msg)
        header, protocol, name, map_, folder, game, appid, players, max_players, bots, server_type, environment, visibility, vac, version, edf = msg
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
        edf = int.from_bytes(edf, byteorder='little')
        offset = struct.calcsize('<b')
        if edf & 0x80 :
            port, = struct.unpack('<H', data[offset:offset+2])
            print('16、port:', port)
        offset += 2
        if edf & 0x10:
            steam_id, = struct.unpack('<Q', data[offset:offset+8])
            print('17、SteamID:', steam_id)
        offset += 8
        if edf & 0x40:
            spectator_port, = struct.unpack('<H', data[offset:offset+3])
            print('18、spectator_port',spectator_port)
            new,data_len =check_string(data,offset)
            spectator_name , = new
            print('19、spectator_name',spectator_name.decode())
        offset += 15
        if edf & 0x20:
            new,data_len =check_string(data,offset)
            Keywords = new
            print('20、Keywords',Keywords.decode())
        offset += 13
        if edf & 0x01:
            GameID, = struct.unpack('<Q', data[offset:offset+8])
            print('21、GameID',GameID)
    elif data == b'A':
        print("Server is using Challenge Number")
    else:
        print("Invalid Response")
    s.close()


def check_string(data:bytes,sock:int):
    data_this = data[sock:]
    data_right = data_this.split(b'\x00')
    data_len = len(data_right[0])
    tag = '<'+str(data_len)+'s'
    new = struct.unpack(tag,bytes(data[sock:sock+data_len]))
    return [new[0],data_len]

__all__ = ['get_server_info']
