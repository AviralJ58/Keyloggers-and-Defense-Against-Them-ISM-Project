# capture system information
import os
import sys
import time
import logging
import socket
import platform
import psutil
import threading

# Set up logging
logging.basicConfig(filename='keylogs.log', level=logging.INFO, format='%(asctime)s: %(message)s')

# Define function to get system information
def get_info():
    try:
        # Get hostname
        hostname = socket.gethostname()
        # Get IP address
        ip_address = socket.gethostbyname(hostname)
        # Get OS
        oprsys = platform.system()
        # Get number of running processes
        running_processes = psutil.pids()
        # Get name of running processes
        running_processes = [psutil.Process(pid).name() for pid in running_processes]
        # Convert list to string
        running_processes = ', '.join(running_processes)
        # Get number of running threads
        running_threads = threading.active_count()

        # Get network information
        # Get network statistics
        stats = psutil.net_io_counters()
        # Get packets sent
        packets_sent = stats.packets_sent
        # Get packets received
        packets_received = stats.packets_recv
        # Get bytes sent
        bytes_sent = stats.bytes_sent
        # Get bytes received
        bytes_received = stats.bytes_recv
        # Get errors in
        errors_in = stats.errin
        # Get errors out
        errors_out = stats.errout
        # Get dropped packets in
        dropped_packets_in = stats.dropin
        # Get dropped packets out
        dropped_packets_out = stats.dropout

        # log system information to a csv

        if os.path.exists('system_info.csv'):
            with open('system_info.csv', 'a') as f:
                f.write(f'{hostname},{ip_address},{oprsys},"{running_processes}",{running_threads},{time.time()},{packets_sent},{packets_received},{bytes_sent},{bytes_received},{errors_in},{errors_out},{dropped_packets_in},{dropped_packets_out}\n')
        else:
            with open('system_info.csv', 'w') as f:
                f.write(f'Hostname,IP Address,OS,Running Processes,Running Threads,Time,Packets Sent,Packets Received,Bytes Sent,Bytes Received,Errors In,Errors Out,Dropped Packets In,Dropped Packets Out\n')
                f.write(f'{hostname},{ip_address},{oprsys},"{running_processes}",{running_threads},{time.time()},{packets_sent},{packets_received},{bytes_sent},{bytes_received},{errors_in},{errors_out},{dropped_packets_in},{dropped_packets_out}\n')

        logging.info(f'Hostname: {hostname}')
        logging.info(f'IP Address: {ip_address}')
        logging.info(f'OS: {oprsys}')
        logging.info(f'Running Processes: {running_processes}')
        logging.info(f'Running Threads: {running_threads}')
        logging.info(f'Network Statistics: {stats}')
        logging.info(f'Time: {time.time()}')

    except Exception as e:
        print(e)
        logging.error('Error getting system information')

# Get system information every 30 seconds
while True:
    get_info()
    time.sleep(10)
    

