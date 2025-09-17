@echo off
:: Run as Administrator

echo Enabling WSL feature...
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart

echo Enabling Virtual Machine Platform...
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

echo Installing Ubuntu as default WSL distro...
wsl --install -d Ubuntu

echo Setting WSL2 as default...
wsl --set-default-version 2

echo Done! Please restart your machine.
pause
