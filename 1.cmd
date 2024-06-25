@echo off
setlocal enabledelayedexpansion

rem Specify the path to the parent folder
set "parentFolder=C:\Users\VICTUS\OneDrive\Desktop\Fahasa"

rem Loop through child folders 1 to 10
for /L %%i in (1, 1, 10) do (
    rem Specify the path to the child folder
    set "childFolder=!parentFolder!\!%%i!"
    
    rem Copy the secret.txt from the parent folder to the child folder and overwrite
    copy /Y "!parentFolder!\secret.txt" "!childFolder!\secret.txt"
    
    echo Copied secret.txt to !childFolder!
)

echo Done
