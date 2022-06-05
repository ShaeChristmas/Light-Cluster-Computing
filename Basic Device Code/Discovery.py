from zeroconf import ServiceBrowser, ServiceListener, Zeroconf
import json


class MyListener(ServiceListener):

    def update_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        print(f"Service {name} updated")

    def remove_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        print(f"Service {name} removed")

    def add_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        info = zc.get_service_info(type_, name)
        print(f"Service {name} added, service info: {info}")


zeroconf = Zeroconf()
listener = MyListener()
# My devices are "_iot-device._tcp.local."
browser = ServiceBrowser(zeroconf, "_iot-device._tcp.local.", listener)
info = zeroconf.get_service_info("_iot-device._tcp.local.", "test-device._iot-device._tcp.local.")
print("Service Info: "+str((info.addresses)))

try:
    input("Press enter to exit...\n\n")
finally:
    zeroconf.close()