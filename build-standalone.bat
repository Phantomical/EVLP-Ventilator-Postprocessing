@echo on

rmdir /s /q dist

pyinstaller "%~dp0/convert_to_utf8/convert_to_utf8.py"
pyinstaller "%~dp0/ventilator_data/preprocess.py"
pyinstaller "%~dp0/ventilator_data/sample.py"
pyinstaller "%~dp0/ventilator_data/time-sample.py"

rmdir /s /q build
md bin

xcopy /y /s dist\convert_to_utf8 bin\
copy /Y /B  dist\preprocess\preprocess.exe bin /B
copy /Y /B  dist\sample\sample.exe bin /B
copy /Y /B  dist\time-sample\time-sample.exe bin /B

del convert_to_utf8.spec
del preprocess.spec
del sample.spec
del time-sample.spec

copy /Y /A "%~dp0\README.txt" "%cd%" /A
copy /Y /A "%~dp0\generate-csvs.bat" "%cd%" /A

rmdir /s /q dist

call "%~dp0\mkhelp"

