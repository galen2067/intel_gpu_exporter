"""
本程序是监控intel_gpu_top的指标，并做成指标查询导出
"""
#!/usr/bin/env python3
import socket

#获取主机名
hostn = socket.gethostname()
server_name = "ip_transcode2_server_" + hostn
key1 = "intel_gpu_top"

#GPU刷新频率,ms
gpu_interval_time = "500"
#采集间隔时间，秒
collect_interval_time = 30

#定义需要采集的卡参数
card_list = ['card1','card2','card3','card4','card5','card6','card7','card8']
#定义采集指标bash命令
intel_gpu_top_cmd_list = {
    'card1' : ['/usr/sbin/intel_gpu_top', '-d' 'pci:card=1', '-s',str(gpu_interval_time),'-l'],
    'card2' : ['/usr/sbin/intel_gpu_top', '-d' 'pci:card=2', '-s',str(gpu_interval_time),'-l'],
    'card3' : ['/usr/sbin/intel_gpu_top', '-d' 'pci:card=3', '-s',str(gpu_interval_time),'-l'],
    'card4' : ['/usr/sbin/intel_gpu_top', '-d' 'pci:card=4', '-s',str(gpu_interval_time),'-l'],
    'card5' : ['/usr/sbin/intel_gpu_top', '-d' 'pci:card=5', '-s',str(gpu_interval_time),'-l'],
    'card6' : ['/usr/sbin/intel_gpu_top', '-d' 'pci:card=6', '-s',str(gpu_interval_time),'-l'],
    'card7' : ['/usr/sbin/intel_gpu_top', '-d' 'pci:card=7', '-s',str(gpu_interval_time),'-l'],
    'card8' : ['/usr/sbin/intel_gpu_top', '-d' 'pci:card=8', '-s',str(gpu_interval_time),'-l']
}

#定义标签
labels = ['card','instance','server_type']
#当前已经实现的采集指标列表
metrics_list = {
    'gpu_freq_req':1,
    'gpu_freq_act':1,
    'gpu_irq':1,
    'gpu_rc6':1,
    'gpu_rcs_0_rate':1,
    'gpu_rcs_0_se':1,
    'gpu_rcs_0_wa':1,
    'gpu_bcs_0_rate':1,
    'gpu_bcs_0_se':1,
    'gpu_bcs_0_wa':1,
    'gpu_vcs_0_rate':1,
    'gpu_vcs_0_se':1,
    'gpu_vcs_0_wa':1,
    'gpu_vcs_1_rate':1,
    'gpu_vcs_1_se':1,
    'gpu_vcs_1_wa':1,
    'gpu_vecs_0_rate':1,
    'gpu_vecs_0_se':1,
    'gpu_vecs_0_wa':1
}

#工作目录
work_dir = "/opt/monitor/intel_gpu_export"
#日志文件
log_file = f"{work_dir}/logs/intel_gpu_top.log"
#日志文件保留天数
log_back_cnt = 7
#日志级别
log_level = "INFO"

#服务端口定义,默认
server_port = 9109
