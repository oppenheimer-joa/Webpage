import csv, psutil, time, sys, os, threading
from datetime import datetime

class LogMaker:
    def __init__(self, log_dir=None, csv_dir=None):
        self.log_dir = log_dir
        self.csv_dir = csv_dir

class LogMakerTxt(LogMaker):
    def __init__(self, log_dir):
        super().__init__(log_dir)

    def LogFunction(self, function):
        script = sys.argv[0]
        function_name = None
        if callable(function):
            function_name = function.__name__ # param
        else:
            raise ValueError("Input is not a valid function")

        start_time = time.time()
        start_datetime = datetime.fromtimestamp(start_time) # param

        try:
            returned = function() # param
            result = "succeed" # param
            success = True # param
            error_msg = None # param
        except Exception as e:
            result = "failed" # param
            success = False # param
            error_msg = str(e) # param

        end_time = time.time()
        end_datetime = datetime.fromtimestamp(end_time)
        runtime = end_time - start_time # param

        cpu_percent = psutil.cpu_percent(interval=1) # param
        memory_percent = psutil.virtual_memory().percent # param
        network_io = psutil.net_io_counters() # param

        log_content = f"""
=======================================================
       __                             _             
      / /  ___   __ _ _ __ ___   __ _| | _____ _ __ 
     / /  / _ \ / _` | '_ ` _ \ / _` | |/ / _ | '__|
    / /__| (_) | (_| | | | | | | (_| |   |  __| |   
    \____/\___/ \__, |_| |_| |_|\__,_|_|\_\___|_|   
                |___/                               
======================= v1.0.0 =======================

script: {script}
function: {function_name}

runtime: {runtime:.2f} sec
Start time : {start_datetime}
End time : {end_datetime}

result: {result}
error: {error_msg}

Total CPU usage: {cpu_percent}%
Total Memory usage: {memory_percent}%

Network sent: {network_io.bytes_sent / (1024 * 1024):.2f} mb
Network received: {network_io.bytes_recv / (1024 * 1024):.2f} mb

Return : {returned}

===============================================
"""
        print_datetime = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        log_file_name = os.path.join(self.log_dir, f"{function_name}_{print_datetime}.txt")
        with open(log_file_name, "w") as log_file:
            log_file.write(log_content)

class LogMakerCsv(LogMaker):
    def __init__(self, csv_dir):
        super().__init__(csv_dir=csv_dir)

    def LogFunction(self, duration:float, function):

        # get function name
        if callable(function):
            function_name = function.__name__
        else:
            raise ValueError("Input is not a valid function")
        
        # get date
        date = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

        # make file name & file write
        file_dir = f"{self.csv_dir}/{function_name}_{date}.csv"
        with open(file_dir, 'w', newline='') as csvfile:
            fieldnames = ['Timestamp', 'CPU (%)', 'Memory (%)', 'Network (bytes_sent)', 'Network (bytes_recv)']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            try:
                # set start time
                start_time = time.time()

                # start thread
                target_thread = threading.Thread(target=function)
                target_thread.start()

                # file write
                while target_thread.is_alive():
                    timestamp = time.time()
                    timestamp_datetime = datetime.fromtimestamp(timestamp)
                    cpu_percent = psutil.cpu_percent()
                    memory_percent = psutil.virtual_memory().percent
                    net_io_counters = psutil.net_io_counters()
                    bytes_sent = net_io_counters.bytes_sent
                    bytes_recv = net_io_counters.bytes_recv
                    writer.writerow({'Timestamp': timestamp_datetime, 'CPU (%)': cpu_percent, 'Memory (%)': memory_percent,
                                    'Network (bytes_sent)': bytes_sent, 'Network (bytes_recv)': bytes_recv})
                    time.sleep(duration)

                end_time = time.time()
                print(f"모니터링 종료. 실행 시간: {end_time - start_time} 초")
            except Exception as e:
                pass


if __name__ == "__main__":
    def demo_function():
        for i in range(5000000):
            print("Hello, World!")

    log_dir = "resourcebox/logmaker/src/logs"
    logger_1 = LogMakerTxt(log_dir=log_dir)

    csv_dir = "resourcebox/logmaker/src/logs"
    logger_2 = LogMakerCsv(csv_dir=csv_dir)

    logger_2.LogFunction(0.2, demo_function)
    # logger_1.LogFunction(demo_function)