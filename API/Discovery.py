from zeroconf import ServiceBrowser, ServiceListener, Zeroconf
import json, socket, dns.resolver


addresses = []
class MyListener(ServiceListener):

    def update_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        print(f"Service {name} updated")

    def remove_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        print(f"Service {name} removed")

    def add_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        info = zc.get_service_info(type_, name)
        print(f"Service {name} added, service info: {info}")
        # Add device to list.
        addr = socket.inet_ntoa(info.addresses[0])
        if not (addr in addresses):
            addresses.append(addr)
            print(addr," Added!")
        with open('ips.json', 'w') as f:
            json.dump(addresses, f)



zeroconf = Zeroconf()
listener = MyListener()
# My devices are "_iot-device._tcp.local."
#clear_ips(120)
browser = ServiceBrowser(zeroconf, "_iot-device._tcp.local.", listener)
#info = zeroconf.get_service_info("_iot-device._tcp.local.", "test-device._iot-device._tcp.local.")
#addr = socket.gethostbyname(info.server[0:-1])
#print("Service Info: ",addr)
#print("Service Info: ",info.addresses[0])
try:
    input("Press enter to exit...\n\n")
finally:
    zeroconf.close()