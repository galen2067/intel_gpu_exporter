# cd /xor/python/pyvenv && source bin/activate
cd /opt/monitor
nohup  python3   intel_gpu_metrics_export.py   >  ./logs/stdout.log  2>&1 & 
echo "正在启动服务。。。"
sleep 5
ps -ef |grep intel_gpu_metrics_export
netstat -tanlp |grep ":9109"
