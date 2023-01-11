import socket
import struct

ip = '43.142.178.212'
port = 40001
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
        # '''
        # ms = ''
        # a = [data[0],data[1],data[2:51],data[138]]
        # print(a)
        # for i in a:
        #     try:
        #         ms += i.decode()+':'
        #     except AttributeError:
        #         ms += str(i)+':'
        # print(a)
        # print(ms)
        # header, protocol, name, map_, folder, game, appid, players, max_players, bots, server_type, environment, visibility, vac, version, edf = struct.unpack('<b b 20s 16s 20s 20s h b b b c c b 20s b', data[4:111])
        # ('<b b 20s 16s 20s 20s h b b b c c b 20s b', data[5:])
        header, protocol, name, map_, folder, game, appid, players, max_players, bots, server_type, environment, visibility, vac, version, edf  = struct.unpack('<b b 35s 13s 12s 14s h b b b c c b b 8s 46s', data)
        print("Server Name: ", name.decode('utf-8').strip('\x00'))
        print("Map: ", map_.decode('utf-8').strip('\x00'))
        print("Folder: ", folder.decode('utf-8').strip('\x00'))
        print("Game: ", game.decode('utf-8',errors='ignore').strip('\x00'))
        print('appid: ',appid)
        print("Players: ", players)
        print("Maximum Players: ", max_players)
        print("Bots: ",bots)
        print("Server type: ", server_type.decode())
        print("Environment: ",environment.decode())
        print("Visibility: ",visibility)
        print("Vac: ",vac)
        print("Server version: ",version.decode(errors='ignore'))
        print(len(edf),edf)
        edf = int.from_bytes(edf, byteorder='little')
        offset = struct.calcsize('<b')
        if edf & 0x80 :
            port, = struct.unpack('<H', data[offset:offset+2])
            print('port:', port)
        offset += 2
        if edf & 0x10:
            steam_id, = struct.unpack('<Q', data[offset:offset+8])
            print('SteamID:', steam_id)
        offset += 8
        if edf & 0x40:
            spectator_port, = struct.unpack('<H', data[offset:offset+2])
            print('spectator_port',spectator_port)
            spectator_name , = struct.unpack('<13s', data[offset:offset+13])
            print('spectator_name',spectator_name.decode())
        offset += 15
        if edf & 0x20:
            Keywords, = struct.unpack('<13s', data[offset:offset+13])
            print('Keywords',Keywords)
        offset += 13
        if edf & 0x01:
            GameID, = struct.unpack('<Q', data[offset:offset+8])
            print(offset)
            print('GameID',GameID)
    elif data == b'A':
        print("Server is using Challenge Number")
    else:
        print("Invalid Response")
    s.close()

get_server_info(ip, port)