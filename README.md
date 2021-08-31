# Caja-Fuerte
Encripción de archivo de texto protegido por contraseña.

## ¿Cómo funciona?

-Toma como argumento una opcion (-o) y una clave (-c).

-Opciones:

e para encriptar el archivo.

d para desencriptar el archivo.ç

m para mostrar el contenido y volver a encriptarlo con la misma clave.

### Ejemplos:
```
python cajaFuerte.py -o e -c 1234
python cajaFuerte.py -o d -c 1234
python cajaFuerte.py -o m -c 1234
```

-Si ponemos mal la clave al querer desencriptar, se nos envia un mail detallando la hora, las coordenadas y una captura de la webcam en el momento. También se vuelve a encriptar el archivo para mas seguridad.

## Para correrlo: 

-Setear nuestros valores para las variables "CAJAFUERTE", "REMITENTE", "DESTINATARIO" Y "CLAVE".
-Poner el archivo.bat en el directorio :C/Users/TuNombreDeUsuario para correr el programa solo escriendo cajaFuerte.


### To do:

-Crear archivo con intentos fallidos para poder deshacer la doble encriptación.


