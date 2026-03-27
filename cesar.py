import sys

def cifrado_cesar(texto, corrimiento):
    resultado = ""
    for caracter in texto:
        if caracter.isalpha():  
            base = ord('A') if caracter.isupper() else ord('a')
            nuevo_caracter = chr((ord(caracter) - base + corrimiento) % 26 + base)
            resultado += nuevo_caracter
        else:
            resultado += caracter
    return resultado

if len(sys.argv) != 3:
    sys.exit(1)

texto = sys.argv[1]
corrimiento = int(sys.argv[2])

print(cifrado_cesar(texto, corrimiento))

