# dog_rl_deploy
四足机器人强化学习实物部署（Sim to Real）

参考仓库：https://github.com/Improbable-AI/walk-these-ways

# 使用方法

## 连接宇树机器狗

连接机器狗自带wifi`UnitreeRoboticsA1-xxx`，测试连通性

```bash
ping 192.168.123.12
```

若没问题进行下一步

## 部署docker环境

进入`scripts`文件夹，执行部署脚本。该脚本会下载docker镜像并发送至机器人。（密码为123）

```bash
cd dog_rl_deploy/scripts
bash deploy_env.sh
```

ssh进入机器人

```
ssh unitree@192.168.123.12
```

安装docker环境

```bash
cd ~/a1_gym/dog_rl_deploy/docker
bash unzip_image.sh
```

以上步骤仅需执行一次

## 运行控制器

ssh进入机器人

```bash
ssh unitree@192.168.123.12
```

进入`scripts`文件夹，运行`run_rl.sh`脚本。该脚本会停止unitree官方的进程，运行自定义的lcm程序与docker

```bash
cd ~/a1_gym/dog_rl_deploy/scripts
bash run_rl.sh
```

脚本会捕获退出信号，按下Ctrl+C自动停止程序并kill相关进程。
