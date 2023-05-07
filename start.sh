#!/bin/bash

# 启动model_api.py
echo "正在启动model_api.py ..."
python model_api.py &

# 等待5秒钟，确保model_api.py已经启动完成
sleep 30

# 启动web_ui.py
echo "正在启动web_ui.py ..."
python web_ui.py &

# 等待5秒钟，确保web_ui.py已经启动完成
sleep 30

# 输出提示
echo "启动成功！"
