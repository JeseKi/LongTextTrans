#!/bin/bash

# 退出脚本，如果任何命令失败
set -e

# 检查 venv 是否存在，如果不存在则创建
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
echo "Installing dependencies..."
pip install -r requirements.txt

# 启动 Uvicorn 服务器
echo "Starting Uvicorn server..."
uvicorn main:app --host 0.0.0.0 --port 8000
