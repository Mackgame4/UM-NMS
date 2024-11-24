import subprocess
import psutil
import json
from notify import notify

def run_process(command, name):
        stdout = None
        try:
            process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            stdout = stdout.strip().decode()
            stderr = stderr.strip().decode()
            if stdout:
                notify("debug", f"Link metrics test {name} results: {stdout}")
            if stderr:
                notify("error", f"Error running command: {stderr}")
        except Exception as e:
            notify("error", f"Error running command: {e}")
        return stdout

def get_cpu_usage():
    try:
        cpu = psutil.cpu_percent(interval=1) # We could also use the psutil library to get the CPU usage for a determined process
        return cpu
    except Exception as e:
        notify("error", f"Error getting CPU Usage: {e}")
        return None

def get_ram_usage():
    try:
        ram = psutil.virtual_memory()
        ram_usage = ram.percent
        return ram_usage
    except Exception as e:
        notify("error", f"Error getting RAM Usage: {e}")
        return None

def get_interface_stats(): # Get network interface stats
    try:
        eth_stats = psutil.net_io_counters(pernic=True)
        notify("debug", f"Available network interfaces: {list(eth_stats.keys())}") # List of available network interfaces
        return eth_stats
    except Exception as e:
        notify("error", f"Error getting network interface stats: {e}")
        return None

def run_device_metrics(device, result_queue): # Run device metrics tests
    device_metrics_results = {}
    # Get cpu usage if device['device_metrics']['cpu'] is True
    if device['device_metrics']['cpu_usage']:
        cpu_usage = get_cpu_usage()
        if cpu_usage is not None:
            notify("info", f"CPU Usage: {cpu_usage}%")
            device_metrics_results['cpu_usage'] = cpu_usage
    # Get ram usage if device['device_metrics']['ram'] is True
    if device['device_metrics']['ram_usage']:
        ram_usage = get_ram_usage()
        if ram_usage is not None:
            notify("info", f"RAM Usage: {ram_usage}%")
            device_metrics_results['ram_usage'] = ram_usage
    # Get interface stats if device['device_metrics']['interface_stats'] is not empty
    for eth in device['device_metrics']['interface_stats']:
        eth_stats = get_interface_stats()
        if eth_stats is not None:
            if eth in eth_stats: # Check if the eth interface exists in available interfaces
                eth_name = eth
                eth_bytes_sent = eth_stats[eth].bytes_sent
                eth_bytes_recv = eth_stats[eth].bytes_recv
                notify("info", f"Interface {eth_name}: Bytes sent: {eth_bytes_sent}, Bytes received: {eth_bytes_recv}")
                device_metrics_results['interface_stats'] = {eth_name: {"bytes_sent": eth_bytes_sent, "bytes_recv": eth_bytes_recv}}
            else:
                notify("warning", f"Interface {eth} not found in network interfaces.")
    result_queue.put(device_metrics_results)
    return device_metrics_results

def run_link_metrics(device, result_queue): # Run network tests
    link_metric_results = {}
    for metric_name in device['link_metrics']:
        notify("info", f"Running {metric_name} metrics test")
        metric = device['link_metrics'][metric_name]
        metric_tool = metric['tool']
        if metric_tool == 'iperf':
            metric_role = metric.get('role', 'server') # Default role is server
            metric_server_address = metric.get('server_address', '0.0.0.0') # Default server address
            metric_duration = metric.get('duration', 10) # Default duration is 10 seconds
            metric_transport = '-u' if metric.get('transport', 'tcp') == 'udp' else '' # Default transport is TCP
            metric_frequency = metric.get('frequency', 1) # Default frequency is 1
            if metric_role == 'server':
                command = f"iperf3 -s".strip()
            elif metric_role == 'client':
                command = f"iperf3 -c {metric_server_address} -t {metric_duration} -J {metric_transport}".strip()
            for i in range(1, metric_frequency+1):
                # Run the command and get the output
                notify("debug", f"Running command: {command}; {i}/{metric_frequency} times")
                result = run_process(command, metric_name)
                if metric_name == 'jitter' and result:
                    try:
                        json_output = json.loads(result)
                        jitter = json_output['end']['sum']['jitter_ms']
                        notify("debug", f"Jitter: {jitter} ms")
                        link_metric_results[metric_name] = jitter
                    except Exception as e:
                        notify("error", f"Error parsing iperf3 output: {e}")
                if metric_name == 'bandwidth' and result:
                    try:
                        json_output = json.loads(result)
                        bandwidth = json_output['end']['sum_sent']['bits_per_second']
                        notify("debug", f"Bandwidth: {bandwidth} bps")
                        link_metric_results[metric_name] = bandwidth
                    except Exception as e:
                        notify("error", f"Error parsing iperf3 output: {e}")
                if metric_name == 'packet_loss' and result:
                    try:
                        json_output = json.loads(result)
                        packet_loss = json_output['end']['sum']['lost_percent']
                        notify("debug", f"Packet Loss: {packet_loss}%")
                        link_metric_results[metric_name] = packet_loss
                    except Exception as e:
                        notify("error", f"Error parsing iperf3 output: {e}")
        if metric_tool == 'ping':
            metric_destination_address = metric.get('destination', '127.0.0.1')
            metric_packet_count = metric.get('packet_count', 4)
            metric_frequency = metric.get('frequency', 1)
            command = f"ping {metric_destination_address} -c {metric_packet_count}".strip()
            for i in range(1, metric_frequency+1):
                # Run the command and get the output
                notify("debug", f"Running command: {command}; {i}/{metric_frequency} times")
                result = run_process(command, metric_name)
                if metric_name == 'latency' and result:
                    try:
                        latency = float(result.split('/')[-1].split()[0])
                        notify("debug", f"Latency: {latency} ms")
                        link_metric_results[metric_name] = latency
                    except Exception as e:
                        notify("error", f"Error parsing ping output for latency: {e}")
    result_queue.put(link_metric_results)
    return link_metric_results