@echo off
REM 检查Python虚拟环境模块venv是否安装
python -c "import venv" 2>NUL
IF %ERRORLEVEL% NEQ 0 (
    echo The virtual environment package 'venv' is not installed.
    echo Please install 'venv' or update Python to a version that includes 'venv'.
    exit /b
)

REM 检查虚拟环境是否已存在
IF NOT EXIST ".\venv\" (
    echo Creating virtual environment...
    python -m venv venv
) ELSE (
    echo Virtual environment already exists.
)

REM 激活虚拟环境
CALL .\venv\Scripts\activate

REM 检查requirements.txt是否存在并安装依赖
IF EXIST "requirements.txt" (
    echo Installing dependencies...
    pip install -r requirements.txt
) ELSE (
    echo requirements.txt not found, skipping dependencies installation.
)

REM 启动Uvicorn服务器
echo Starting Uvicorn server...
uvicorn main:app

pause
