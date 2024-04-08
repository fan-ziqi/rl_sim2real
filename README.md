# 此项目已停止维护，请不要再fork本仓库。如需sim2real功能请关注https://github.com/fan-ziqi/rl_sar

# dog_rl_deploy
四足机器人强化学习实物部署（Sim to Real）

参考仓库：https://github.com/Improbable-AI/walk-these-ways

# 拉取代码

在walk-these-ways根目录下拉取代码

```bash
git clone -b a1_wtw https://github.com/fan-ziqi/dog_rl_deploy
```

# 使用方法

## 连接宇树机器狗

连接机器狗自带wifi`UnitreeRoboticsA1-xxx`，测试连通性

```bash
ping 192.168.123.12
```

若没问题进行下一步

## 部署docker环境

进入本项目根目录下的`scripts`文件夹，执行部署脚本。该脚本会下载docker镜像并发送至机器人。（密码为123）

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

进入本项目根目录下的`scripts`文件夹，运行`run_rl.sh`脚本。该脚本会停止unitree官方的进程，运行自定义的lcm程序与docker

```bash
cd ~/a1_gym/dog_rl_deploy/scripts
bash run_rl.sh
```

随后多次（大概三四次）按下LR键，狗会开始运动。具体键位详见https://github.com/Improbable-AI/walk-these-ways中的README

再次按下LR键，狗会停止运动

此脚本会捕获退出信号，按下Ctrl+C自动停止程序并kill相关进程。
