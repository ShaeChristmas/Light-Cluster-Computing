import platform, socket,re,uuid,json,psutil,logging

mac = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
def getName():
    return 'LightDevice' + mac[-6:]

def getIp():
    return socket.gethostbyname(socket.gethostname())

def getMac():
    return ':'.join(re.findall('..', '%012x' % uuid.getnode()))

def getComp():
    info={}
    try:
        info['processor']=platform.processor()
        info['ram']=str(round(psutil.virtual_memory().total / (1024.0 **3)))+" GB"
        return json.dumps(info)
    except Exception as e:
        logging.exception(e)
    print(json.loads(info))
    return info
        

def main():
    info = {}
    #name
    #print('name')
    info['name'] = getName()
    #print(info.name)
    #ip
    #print('ip')
    info['ip'] = getIp()
    #print(info.ip)
    #mac
    #print('mac')
    info['mac'] = getMac()
    #print(info.mac)
    #computation
    #print('Computation')
    info['comp'] = getComp()
    #print(info.comp)

    #format to JSON
    print(info)
    #save to Textfile
    with open('local.json', 'w') as f:
        json.dump(info, f)

if __name__ == '__main__':
    main()