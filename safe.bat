@echo Acceso a caja fuerte

@echo off
cd "C:\Users\Tomas\Desktop\Tomas\Python\safe"
set /p modo= "Modo: " 
set /p clave= "Clave: "
python safe.py -o %modo% -p %clave%
cd "C:\Users\Tomas"