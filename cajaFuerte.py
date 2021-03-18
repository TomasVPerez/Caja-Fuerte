#TomasPerez
#https://github.com/TomasVPerez

from hashlib import sha256
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import new as Random
from email.message import EmailMessage
import base64, getpass, time, smtplib, os, geocoder     

ADMINPW = os.getenv('ADMINPW')
CAJAFUERTE = os.getenv('TXT')

class AESEncripcion:
    def __init__(self, llave):
        self.largo = 16
        self.archivo = CAJAFUERTE
        self.llave = sha256(llave.encode("utf-8")).digest()[:32] #Tomamos la pwd, la codificamos con sha256 y tomamos los primeros 32 bytes de la codificacion.
        #Pad para que los datos sean multiplos de 16.
        self.pad = lambda s: s + (self.largo - len(s) % self.largo) * chr((self.largo - len(s) % self.largo)) #El primer calculo nos da un numero, el segundo calculo nos da un numero y con chr obtenemos la letra correspondiente al mismo.
        #Usamos ese caracter para paddear los datos.
        self.unpad = lambda s: s[:-ord(s[len(s)-1:])] #Del pad obtenemos el ultimo caracter(el del calculo hecho) y con ord recuperamos el numero correspondiente al caracter.
    
    def leer(self):
        with open(self.archivo, "r") as a:
            datos = a.read()
            texto = self.pad(datos) #Usamos pad para convertir el dato leido en multiplo de 16.
            return texto

    def sobrescribir(self, dato):
        with open(self.archivo, "w") as a:
            a.write(dato)

    def encripcion(self):
        textoPleno = self.leer()
        iv = Random().read(16) #Devuelve bytes random del.largo escpecificado con read() usando AES.
        cifrar = AES.new(self.llave, AES.MODE_OFB, iv)
        textoCifrado = base64.b64encode(iv + cifrar.encrypt(bytes(textoPleno, "utf-8"))).decode() #Cifra el texto con base64 usando los bytes random y el texto en bytes.
        self.sobrescribir(textoCifrado)
    
    def desencripcion(self):
        textoEncriptado = self.leer() #Lee el archivo con el texto encriptado
        textoCifrado = base64.b64decode(textoEncriptado) #Obteniendo el texto cifrado con base64
        iv = textoCifrado[:self.largo] #Obtenemos el iv usado
        decifrar = AES.new(self.llave, AES.MODE_OFB, iv) #Lo deciframos usando la llave y el iv
        texto = self.unpad(decifrar.decrypt(textoCifrado[self.largo:])).decode() #Lo terminamos de desencriptar con unpad usando el texto decifrado desencriptado
        self.sobrescribir(texto)    

    
def encriptar():
    E = AESEncripcion(llave=ADMINPW)
    E.encripcion()

def desencriptar():
    E = AESEncripcion(llave=ADMINPW)
    E.desencripcion()

def mostrar():
    print("\nLinks: ")
    with open(CAJAFUERTE, "r") as a:
        desencriptar()
        print(a.read())
        encriptar()

def mandarMail():
    REMITENTE = os.getenv('OUTMAIL')
    DESTINATARIO = os.getenv('PTNMAIL')
    CLAVE = os.getenv('OUTMAILKEY')

    g = geocoder.ip('me')
    locacion = g.latlng

    mensaje = (f"\nAlguien intento entrar a tu caja fuerte.\n Fecha y hora: {time.ctime()}\n Lugar: {locacion}")

    servidor = smtplib.SMTP("smtp-mail.outlook.com", 587)
    servidor.ehlo()
    servidor.starttls()
    servidor.login(REMITENTE, CLAVE)
    servidor.sendmail(REMITENTE, DESTINATARIO, mensaje)

    usuario = os.path.expanduser("~").split("\\")[2]
    print(f"Se avisó a {usuario} por mail.")


def main():
    pwd = getpass.getpass("Contraseña: ")
    if pwd == ADMINPW:
        mostrar()
    else:
        print("Incorrecto!")
        print("...")
        mandarMail()

if __name__=='__main__':
    main()









 