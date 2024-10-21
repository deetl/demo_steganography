@echo off
rem Überprüfen, ob ein Parameter übergeben wurde
if "%1"=="" (
    echo Fehler: Kein Parameter übergeben.
    echo Verwendung: batchdatei.bat [Parameter]
    exit /b 1
)

rem Schleife von 1 bis 8
for /l %%i in (0,1,7) do (
    echo py.exe .\stego_layer.py -r %1.png -w %1_%%i.png -B %%i -n
    py.exe .\stego_layer.py -r %1.png -w %1_%%i.png -B %%i -n
)
echo Fertig.
