#!/bin/bash

ppid=$(ps -ef |grep  intel_gpu_metrics_export  |grep -v grep |awk -F ' ' '{print $2}')
if [[ -z "$ppid" ]] ;  then
    echo "intel_gpu_metrics_export服务没有启动"
else
    echo "kill intel_gpu_metrics_export pid:$ppid"
    kill -9 $ppid
    sleep 5
    # netstat -tanlp |grep  ":11177"
    ps -ef  |grep intel_gpu_metrics_export  |grep -v grep
    if [[ $? -eq 0 ]] ;then
        echo "服务未停止成功"
    else
        echo "服务已停止成功"
    fi
fi
