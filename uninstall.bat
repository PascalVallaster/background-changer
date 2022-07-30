:: Bat file for uninstalling the application including autostart shortcut

@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

SET DEL_LINK=%HOMEDRIVE%%HOMEPATH%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\background-changer.lnk
SET DEL_FOLDER=background-changer

:: Delete the link
DEL "%DEL_LINK%" /f /q

:: Delete the application folder
start /b "" cmd /c rd /s /q "%~dp0"