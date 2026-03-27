#!/usr/bin/env python3
import sys
from scapy.all import rdpcap, ICMP, Raw
from colorama import Fore, Style

def descifrar_cesar(texto, corrimiento):
    """Descifra juntando letras, pero conserva espacios reales del mensaje."""
    resultado = ""
    for char in texto:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            resultado += chr((ord(char) - base - corrimiento) % 26 + base)
        elif char == " ":  
            # Mantener espacios si realmente vienen del mensaje
            resultado += " "
        # Si quieres conservar otros caracteres raros, puedes agregarlos aquí
    return resultado

def fuerza_bruta_cesar(texto_cifrado):
    print("=== Resultados de descifrado César ===\n")
    for i, corr in enumerate(range(1, 26), start=1):
        desc = descifrar_cesar(texto_cifrado, corr)
        if any(p in desc.lower() for p in ["hola", "mensaje", "secreto", "udp", "criptografia"]):
            print(Fore.GREEN + f"{i}. {desc}" + Style.RESET_ALL)
        else:
            print(f"{i}. {desc}")

def capturar_mensaje_desde_pcap(archivo_pcap="cesar.pcapng"):
    """
    Lee paquetes y arma el mensaje con letras y espacios tal cual vienen,
    sin meter espacios extra entre letras.
    """
    paquetes = rdpcap(archivo_pcap)
    partes = []

    for pkt in paquetes:
        if ICMP in pkt and Raw in pkt and getattr(pkt[ICMP], "type", None) in (8, 0):
            texto = pkt[Raw].load.decode("latin-1", errors="ignore")
            # conservar solo letras y espacios
            solo_validos = "".join(c for c in texto if c.isalpha() or c == " ")

            if solo_validos == "":
                continue

            if solo_validos == "b":  # fin del mensaje
                break

            partes.append(solo_validos)

    return "".join(partes)

if __name__ == "__main__":
    archivo = sys.argv[1] if len(sys.argv) > 1 else "cesar.pcapng"
    mensaje_interceptado = capturar_mensaje_desde_pcap(archivo)

    print(f"\nMensaje interceptado: {mensaje_interceptado}\n")
    fuerza_bruta_cesar(mensaje_interceptado)



