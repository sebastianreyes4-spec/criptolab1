from scapy.all import IP, ICMP, Raw, send
import sys
import time

def stealth_ping(dest_ip, message):
    """
    Payload de 48 bytes:
    [letra][`][22 x 0x00]["#$%&'()*+,-./01234567][espacios hasta 48]
    """
    base_pattern = b'!"#$%&\'()*+,-./01234567'  
    seq = 1
    for char in message:
        payload = (
            char.encode() +   
            b'`' +              
            b"\x00" * 22 +     
            base_pattern       
        )
        payload = payload.ljust(48, b' ')
        pkt = (
            IP(dst=dest_ip, ttl=64) /
            ICMP(type=8, id=0x1234, seq=seq) /
            Raw(load=payload)
        )
        send(pkt, verbose=False)        
        print(f"Enviando \"{char}\"")  # 👈 ahora muestra la letra enviada
        print("Sent 1 packets")
        seq += 1
        time.sleep(0.5)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: sudo python3 actividad2.py \"<mensaje>\"")
        sys.exit(1)
    destino = "8.8.8.8"  
    mensaje = sys.argv[1]
    stealth_ping(destino, mensaje)



