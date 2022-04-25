import zeroconf as z
import socket

def initZero(type, name):
    deviceType = '_'+type
    ip = socket.gethostbyname(socket.gethostname())
    properties = {'deviceName': name, 'ip': ip}
    port = 3001

    info = z.ServiceInfo(
        deviceType + '._tcp.local.', 
        name+'.'+deviceType+"._tcp.local.",
        port=port, 
        properties=properties, 
        server=name+ ".local."
    )

    print(info)
    zeroconf = z.Zeroconf()
    zeroconf.register_service(info,cooperating_responders=True)
    print(info.name+"\n"+info.type)
    print("service started")
    try:
        input("Press enter to exit...\n\n") # Device is only discoverable while code is actively running. Not sure if ServiceInfo cannot be retrieved because its not running as a express API or not lmao.
    finally:
        print("quitting")
        zeroconf.close()

def main():
    initZero("iot-device", "test-device")

if __name__ == '__main__':
    main()