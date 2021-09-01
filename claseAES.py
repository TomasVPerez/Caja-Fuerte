#TomasPerez
#https://github.com/TomasVPerez

from hashlib import sha256
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import new as Random
import base64, os

CAJAFUERTE = os.getenv('TXT') #env variable que contiene el path al archivo que quiero encriptar

class EncripcionAES:

    def __init__(self, key):
        self.tamanio_del_bloque = 16 #los datos tienen que estar en bloques de 16 bits
        self.archivo = CAJAFUERTE
        self.key = sha256(key.encode("utf-8")).digest()[:32] #crea una llave con un hash de 256 bits y toma los primeros 32 (debe ser multiplo de 16)
        self.pad = lambda s: s + (self.tamanio_del_bloque - len(s) % self.tamanio_del_bloque) * chr((self.tamanio_del_bloque - len(s) % self.tamanio_del_bloque)) # creamos un padding para rellenar el bloque de bits faltantes
        self.unpad = lambda s: s[:-ord(s[len(s)-1:])] # obtenemos el ultimo caracter del padding y con ord lo pasamos a numero, obteniendo el calculo previo para saber cuantos bits quitarle al output

    def leer_archivo(self):
        with open(self.archivo, "r") as documento:
            datos = documento.read()
            texto = self.pad(datos) #padea el contenido para rellenar el bloque de bits
            return texto

    def sobreescribir_archivo(self, dato):
        with open(self.archivo, "w") as documento:
            documento.write(dato)

    def encripcion(self):
        texto_pleno = self.leer_archivo()
        iv = Random().read(AES.block_size) #capa extra de seguridad para la encripcion
        cifrar = AES.new(self.key, AES.MODE_OFB, iv) #Crea una instancia AES con la llave y el iv
        texto_encriptado = base64.b64encode(iv + cifrar.encrypt(bytes(texto_pleno, "utf-8"))).decode() #lo encripto y lo codifico con base64
        self.sobreescribir_archivo(texto_encriptado)

    def desencripcion(self):
        texto_encriptado = self.leer_archivo()
        texto_cifrado = base64.b64decode(texto_encriptado)
        iv = texto_cifrado[:self.tamanio_del_bloque] #obtenemos el iv usado tomando los bits correspondientes al tamaño del bloque del texto usado
        decifrar = AES.new(self.key, AES.MODE_OFB, iv)
        texto_pleno = self.unpad(decifrar.decrypt(texto_cifrado[self.tamanio_del_bloque:])).decode()
        print(texto_pleno)
        self.sobreescribir_archivo(texto_pleno)
       
