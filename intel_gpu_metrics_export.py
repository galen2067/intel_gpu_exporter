"""
本程序是监控intel_gpu_top的指标，并做成指标查询导出
同时本程序不依赖读取其它文件输出的指标，而是直接执行intel_gpu_top命令获取指标,主动结束
"""
#!/usr/bin/env python3
from prometheus_client import Summary, Gauge,start_http_server
# import  datetime
import time 
import os
# import socket
import subprocess
import   logging
from logging.handlers import TimedRotatingFileHandler
from config import *

#定义指标类型
g_FREQ_req = Gauge('gpu_freq_req','',labels)
g_FREQ_act = Gauge('gpu_freq_act','',labels)
g_IRQ = Gauge('gpu_irq','',labels)
g_RC6 = Gauge('gpu_rc6','',labels)
g_RCS_0_rate = Gauge('gpu_rcs_0_rate','',labels)
g_RCS_0_se = Gauge('gpu_rcs_0_se','',labels)
g_RCS_0_wa = Gauge('gpu_rcs_0_wa','',labels)
g_BCS_0_rate = Gauge('gpu_bcs_0_rate','',labels)
g_BCS_0_se = Gauge('gpu_bcs_0_se','',labels)
g_BCS_0_wa = Gauge('gpu_bcs_0_wa','',labels)
g_VCS_0_rate = Gauge('gpu_vcs_0_rate','',labels)
g_VCS_0_se = Gauge('gpu_vcs_0_se','',labels)
g_VCS_0_wa = Gauge('gpu_vcs_0_wa','',labels)
g_VCS_1_rate = Gauge('gpu_vcs_1_rate','',labels)
g_VCS_1_se = Gauge('gpu_vcs_1_se','',labels)
g_VCS_1_wa = Gauge('gpu_vcs_1_wa','',labels)
g_VECS_0_rate = Gauge('gpu_vecs_0_rate','',labels)
g_VECS_0_se = Gauge('gpu_vecs_0_se','',labels)
g_VECS_0_wa = Gauge('gpu_vecs_0_wa','',labels)

#其它指标
monitor_card_cnt = Gauge('monitor_card_cnt','',['instance','server_type'])
monitor_card_failure_cnt = Gauge('monitor_card_failure_cnt','',['instance','server_type'])
request_time = Summary('request_processing_seconds', 'Time spent processing request')


def setup_logger(logger_name="rowin", log_file="./logs/run.log", level="INFO",interval=1, backupCount=7,when="midnight"):
    """
    定义一个日志初始化函数，包括文件、级别、格式等，以及切割和时间范围
    logger_name:日志名称
    log_file:日志文件路径和文件名
    level:日志级别
    interval:切割周期，即频率，根据when决定
    backupCount:保留的日志文件数量，超过该数量则删除最旧的日志文件
    when:切割单位，支持"S","M", "H", "D", "midnight"等
    """
    level_dict = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL
    }
    logger = logging.getLogger(logger_name)
    logger.setLevel(level_dict[level])
    log_path = os.path.dirname(log_file)
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    handler = TimedRotatingFileHandler(log_file, when=when, interval=interval, backupCount=backupCount, encoding='utf-8')
    formatter = logging.Formatter('%(asctime)s  %(levelname)s  %(funcName)s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

#初始化日志记录器
main_logger = setup_logger(logger_name="rowin", log_file=log_file, level=log_level,interval=1, backupCount=log_back_cnt,when="midnight")


def get_gpu_data_for_text(run_cmd:list):
    """
    获取GPU数据，是以text模式，当前json还未调试出来
    """
    #process = subprocess.Popen([run_cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    process = subprocess.Popen(run_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    last_data = ""
    try:
        lines_read = 0
        main_logger.info(f"start_collect_gpu_data:{' '.join(run_cmd)}")
        for line in process.stdout:
            main_logger.debug(line.strip())
            lines_read += 1
            #相当于输出结果的第二行数据读取内容
            if lines_read >= 4:
                last_data = line.strip()
                break
    except Exception as e:
        main_logger.exception(f"采集GPU数据异常: {e}")
    finally:
        process.send_signal(subprocess.signal.SIGINT)
        process.wait() 		
    if not last_data:
        main_logger.warning(f"当前采集数据为空:{last_data}")
        return  []
    if last_data:
        main_logger.info(f"本次采集数据:{last_data}")
        return last_data.split()


@request_time.time()
def refresh_gpu_data():
    """
    刷新GPU数据
    """
    #本次成功采集板卡数量
    success_cnt = 0
    failure_cnt = 0
    for card,run_cmd in intel_gpu_top_cmd_list.items():
        try:
            res_list = get_gpu_data_for_text(run_cmd)
            if not res_list or len(res_list) != len(metrics_list):
                main_logger.warning(f"当前节点{card}获取GPU数据失败,res:{res_list}")
                failure_cnt += 1
                continue
            
            success_cnt += 1
            g_FREQ_req.labels(card,hostn,'gpu').set(res_list[0])
            g_FREQ_act.labels(card,hostn,'gpu').set(res_list[1])
            g_IRQ.labels(card,hostn,'gpu').set(res_list[2])
            g_RC6.labels(card,hostn,'gpu').set(res_list[3])
            g_RCS_0_rate.labels(card,hostn,'gpu').set(res_list[4])
            g_RCS_0_se.labels(card,hostn,'gpu').set(res_list[5])
            g_RCS_0_wa.labels(card,hostn,'gpu').set(res_list[6])
            g_BCS_0_rate.labels(card,hostn,'gpu').set(res_list[7])
            g_BCS_0_se.labels(card,hostn,'gpu').set(res_list[8])
            g_BCS_0_wa.labels(card,hostn,'gpu').set(res_list[9])
            g_VCS_0_rate.labels(card,hostn,'gpu').set(res_list[10])
            g_VCS_0_se.labels(card,hostn,'gpu').set(res_list[11])
            g_VCS_0_wa.labels(card,hostn,'gpu').set(res_list[12])
            g_VCS_1_rate.labels(card,hostn,'gpu').set(res_list[13])
            g_VCS_1_se.labels(card,hostn,'gpu').set(res_list[14])
            g_VCS_1_wa.labels(card,hostn,'gpu').set(res_list[15])
            g_VECS_0_rate.labels(card,hostn,'gpu').set(res_list[16])
            g_VECS_0_se.labels(card,hostn,'gpu').set(res_list[17])
            g_VECS_0_wa.labels(card,hostn,'gpu').set(res_list[18])
        except Exception as err: 
            main_logger.exception(f"当前节点{card}获取GPU数据失败，ERR:{err}")
    
    monitor_card_cnt.labels(hostn,'gpu').set(success_cnt)
    monitor_card_failure_cnt.labels(hostn,'gpu').set(failure_cnt)

if __name__ == '__main__':
    server,t = start_http_server(server_port if server_port else 9109)
    while True:
        try:
            refresh_gpu_data()
            time.sleep(collect_interval_time)
        except Exception as err:
            main_logger.exception(f"刷新GPU数据失败，ERR:{err}")
            #优雅关闭
            # server.shutdown()
            # t.join()
