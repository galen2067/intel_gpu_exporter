# 简介
intel_gpu_exporter是intel的GPU显卡指标采集，结合python的prometheuse客户端进行导出，采集的指标可以在Grafana上展示。
# 安装
  备注：本程序已经在Debian11.9； ubuntu20.04上调试通过，只需要在python3的版本上，同时intel_gpu_top命令正常使用就行。
 ` apt update 
` apt install    intel-gpu-tools   -y`
` pip3 install   prometheus_client `

# 启动
本程序可以采用标准服务启动，也可以通过脚本方式启动和停止，可以根据自己习惯弄

## 标准服务操作：
### 创建服务配置
` cp intel_gpu_export.service /etc/systemd/system/ `
### 加载配置
` systemctl  daemon-reload`
` systemctl start  intel_gpu_export.service`
### 开机启动
`systemctl  enable   intel_gpu_export.service`
### 停止服务
`systemctl stop  intel_gpu_export.service`
### 重启
`systemctl restart  intel_gpu_export.service`


## 脚本启动：
### 启动
` sh start_server.sh`
### 停止
`sh stop_server.sh `
