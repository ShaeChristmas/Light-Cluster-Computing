from zeroconf import ServiceBrowser, Zeroconf, ServiceInfo

class MyListener:

    def remove_service(self, zeroconf, type, name):
        print("Service %s removed" % (name))

    def add_service(self, zeroconf, type, name):
        print(name+"\n"+type)
        info = zeroconf.get_service_info(type, name) # Couldn't get this working, kept returning None. I think i need to use websockets for hosting the device.
        print("Service %s added, service info: %s" % (name, info))


zeroconf = Zeroconf()
listener = MyListener()
browser = ServiceBrowser(zeroconf, "_iot-device._tcp.local.", listener)
try:
    input("Press enter to exit...\n\n")
finally:
    zeroconf.close()