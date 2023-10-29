#!/bin/bash
# 定义退出信号处理函数
cleanup() {
    echo "Exiting..."
    # 在这里执行需要在退出时执行的代码
    ./stop_all.sh
}

# 捕捉退出信号
trap cleanup EXIT
# 主要程序逻辑
echo "Starting..."

cd robot
./stop_all.sh
./start_unitree_sdk.sh
./start_controller.sh

echo "End."