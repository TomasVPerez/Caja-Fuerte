@echo Acceso a caja fuerte

@echo off
cd "DIRECTORIO DONDE SE ENCUENTRE GUARDADO cajaFuerte.py"
set /p modo= "Modo: " 
set /p clave= "Clave: "
python cajaFuerte.py -o %modo% -p %clave%
