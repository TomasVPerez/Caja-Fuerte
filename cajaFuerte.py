#TomasPerez
#https://github.com/TomasVPerez

from claseAES import EncripcionAES, CAJAFUERTE
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import getpass, time, smtplib, os, geocoder, cv2 , argparse  

def args_parser():
    parser = argparse.ArgumentParser(description='archivo -o e(encriptar)/d(desencriptar) clave')
    parser.add_argument('-o', '--opcion', type=str, required=True, help='encriptar/desencriptar/mostrar archivo // -o e, d, de')
    parser.add_argument('-a', '--archivo', type=str, required=False, default=CAJAFUERTE, help='archivo')
    parser.add_argument('-p', '--clave', type=str, required=True, help='clave')
    args = parser.parse_args()
    return args      

def encriptar(key): 
    try:
        E = EncripcionAES(key)
        E.encripcion()
        print("> Encriptado")
    except Exception as e:
        print("> Error al encriptar")

def desencriptar(key):
    try:
        E = EncripcionAES(key)
        E.desencripcion()
        print("> Desencriptado")
    except Exception as e:
        print("> Error al desencriptar")
        mandarMail()

def sacarFoto():
    
    try:
        cam =  cv2.VideoCapture(0, cv2.CAP_DSHOW)
        ret, imagen = cam.read()
        cv2.imshow("cam", imagen)

        k = cv2.waitKey(1)
        home = os.path.expanduser("~")
        archivo = f"{home}/Desktop/Tomas/Python/safe/capturas/img.jpg"

        cv2.imwrite(archivo, imagen)
        cam.release
        cv2.destroyAllWindows

    except Exception as e:
        print("> Error al capturar imagen")

    return archivo

def mandarMail():
    REMITENTE = os.getenv('OUTMAIL')
    DESTINATARIO = os.getenv('PTNMAIL')
    CLAVE = os.getenv('OUTMAILKEY')

    g = geocoder.ip('me')
    locacion = g.latlng

    try:
        archivo = sacarFoto()
        with open(archivo, "rb") as imagen:
            datos = imagen.read()

        mensaje = MIMEMultipart()
        mensaje['Subject'] = "Caja Fuerte"
        mensaje['From'] = REMITENTE
        mensaje['TO'] = DESTINATARIO
        texto = MIMEText(f"\nAlguien intento entrar a tu caja fuerte.\n Fecha y hora: {time.ctime()}\n Lugar: {locacion}")
        mensaje.attach(texto)

        img = MIMEImage(datos, name=os.path.basename(archivo))
        mensaje.attach(img)

        servidor = smtplib.SMTP("smtp-mail.outlook.com", 587)
        servidor.ehlo()
        servidor.starttls()
        servidor.login(REMITENTE, CLAVE)
        servidor.sendmail(REMITENTE, DESTINATARIO, mensaje.as_string())
        servidor.quit()

        usuario = os.path.expanduser("~").split("\\")[2]
        print(f"> Se avisó a {usuario} por mail.")
        
    except Exception as e:
        print("> Error al enviar mail")


def main():
    argumento = args_parser().opcion
    key = args_parser().clave
    if argumento == "e":
        encriptar(key)
    if argumento == "d":
        desencriptar(key)
    if argumento == "m":
        desencriptar(key)
        encriptar(key)

if __name__=='__main__':
    main()
