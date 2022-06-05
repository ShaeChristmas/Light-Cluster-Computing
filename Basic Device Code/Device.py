import socket
from time import sleep
from zeroconf import IPVersion, ServiceInfo, Zeroconf

if __name__ == '__main__':
    name = "test-device"
    ip = socket.gethostbyname(socket.gethostname())
    desc = {'deviceName': name, 'ip': ip}
    deviceType = "_iot-device"
    port = 3001
    info = ServiceInfo(
        deviceType + '._tcp.local.', 
        name+'.'+deviceType+"._tcp.local.",
        port=port,
        addresses=[ip],
        properties=desc,
        server=name+".local.",
    )

    zeroconf = Zeroconf()
    print("Registration of a service, press Ctrl-C to exit...")
    zeroconf.register_service(info, cooperating_responders=True)
    try:
        while True:
            sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        print("Unregistering...")
        zeroconf.unregister_service(info)
        zeroconf.close()