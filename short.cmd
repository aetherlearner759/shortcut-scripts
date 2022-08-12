@ECHO off
:: Global variables
SET /A timeOutSeconds=5
SET CommandName=%1

:: Get absolute path to command scripts folder
PUSHD %~dp0
SET ScriptPATH=%CD%\scripts
POPD

:: Get all argument values except the first one (exclude our command-name)
SET RestArguments=
SHIFT
:ArgumentLoop
IF "%1"=="" GOTO END_ArgumentLoop
SET RestArguments=%RestArguments% %1
SHIFT
GOTO ArgumentLoop
:END_ArgumentLoop

:: Call appropriate script by jumping to the correct case
GOTO :CASE_%CommandName%

:: Final Clean Up
:EOF
TIMEOUT /T %timeOutSeconds%
EXIT /B


:: Cases 
:CASE_clipcopy
    python3 %ScriptPATH%\clipboard-copy.py %RestArguments%
    GOTO END_CASE
:CASE_listify
    python3 %ScriptPATH%\clipboard-listify.py %RestArguments%
    GOTO END_CASE
:CASE_randnum
    python3 %ScriptPATH%\random-number.py %RestArguments%
    GOTO END_CASE

:END_CASE
    GOTO EOF

