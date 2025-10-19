@echo off
echo Actualizando versiones en todas las páginas HTML...

REM Actualizar a v2.11.0 - Unified Version Management
powershell -Command "(Get-Content '1.html') -replace 'v[\d\.]+ - .*', 'v2.11.0 - Unified Version Management' | Set-Content '1.html'"
powershell -Command "(Get-Content '2.html') -replace 'v[\d\.]+ - .*', 'v2.11.0 - Unified Version Management' | Set-Content '2.html'"
powershell -Command "(Get-Content '3.html') -replace 'v[\d\.]+ - .*', 'v2.11.0 - Unified Version Management' | Set-Content '3.html'"
powershell -Command "(Get-Content '4.html') -replace 'v[\d\.]+ - .*', 'v2.11.0 - Unified Version Management' | Set-Content '4.html'"
powershell -Command "(Get-Content '5.html') -replace 'v[\d\.]+ - .*', 'v2.11.0 - Unified Version Management' | Set-Content '5.html'"
powershell -Command "(Get-Content 'login.html') -replace 'v[\d\.]+ - .*', 'v2.11.0 - Unified Version Management' | Set-Content 'login.html'"
powershell -Command "(Get-Content 'index.html') -replace 'v[\d\.]+ - .*', 'v2.11.0 - Unified Version Management' | Set-Content 'index.html'"
powershell -Command "(Get-Content 'telegram-settings.html') -replace 'v[\d\.]+ - .*', 'v2.11.0 - Unified Version Management' | Set-Content 'telegram-settings.html'"
powershell -Command "(Get-Content 'wallets.html') -replace 'v[\d\.]+ - .*', 'v2.11.0 - Unified Version Management' | Set-Content 'wallets.html'"

echo.
echo ✅ Todas las páginas actualizadas a v2.11.0 - Unified Version Management
echo.
echo Ahora ejecuta:
echo git add .
echo git commit -m "version: actualizar a v2.11.0 en todas las páginas"
echo git push origin main
echo.
pause
