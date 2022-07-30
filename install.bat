:: Bat file for installing autostart

:: Idea for Yes-No-Choice:  gist.github.com/jcefoli/fb9400aafee2ac585db3
:: Idea for shortcut:       superuser.com/questions/392061/how-to-make-a-shortcut-from-cmd


@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

:: BEGIN-Hotkey
:start
SET HOTKEY=
echo Enter hotkey for fast-background-changing, format (uppercase): KEY+KEY+...
echo Enter "default" for default combination "CTRL+ALT+N"
echo Enter nothing to skip
SET /p HOTKEY=Hotkey:
if NOT "%HOTKEY%"=="" (
    if "%HOTKEY%"=="default" (
        SET HOTKEY="CTRL+ALT+N"
    )
    SET choice=
    SET /p choice=Is your input for the hotkey: !HOTKEY! correct? [Y/n]:
    IF '!choice!'=='Y' GOTO continue
    IF '!choice!'=='n' GOTO no
    ECHO "!choice!" is not valid
    ECHO.
    GOTO start

    :no
    echo.
    GOTO start
)
if "%HOTKEY%"=="" SET HOTKEY=""

:continue
:: END-Hotkey

SET LinkName=background-changer
SET CWD=%cd%
SET Esc_LinkDest=%%HOMEDRIVE%%%%HOMEPATH%%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\!LinkName!.lnk
SET Esc_LinkTarget=%CWD%\background-changer.py
SET cSctVBS=CreateShortcut.vbs
SET LOG=".\%~N0_log.log"
COPY /y NUL !LOG! >NUL

((
  echo Set oWS = WScript.CreateObject^("WScript.Shell"^) 
  echo sLinkFile = oWS.ExpandEnvironmentStrings^("!Esc_LinkDest!"^)
  echo Set oLink = oWS.CreateShortcut^(sLinkFile^) 
  echo oLink.TargetPath = oWS.ExpandEnvironmentStrings^("!Esc_LinkTarget!"^)
  echo oLink.WorkingDirectory = "%CWD%"
  echo oLink.WindowStyle = 7
  echo oLink.Description = "A autostart-shortcut for background-changer script"
  echo oLink.Hotkey = %HOTKEY%
  echo oLink.Save
)1>!cSctVBS!
IF EXIST %Esc_LinkDest% DEL /F %Esc_LinkDest%
cscript //nologo .\!cSctVBS!
DEL !cSctVBS! /f /q
)1>>!LOG! 2>>&1

TYPE !LOG!
