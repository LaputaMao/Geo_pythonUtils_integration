@echo off
rem 切换到当前批处理文件所在的目录，确保路径正确
cd /d "%~dp0"

rem 使用相对路径运行 main.py
.\PythonUtils\python.exe main.py