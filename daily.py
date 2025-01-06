import subprocess
import time

# Global variable to store the subprocess instance
current_process = None

def run_main_script():
    global current_process
    
    # If a previous process is running, terminate it
    if current_process is not None:
        print("Stopping previous execution...")
        current_process.terminate()
        current_process.wait()  # Wait for the process to terminate completely
        print("Previous execution stopped.")  
    
    # Start a new process
    print("Starting new execution...")
    current_process = subprocess.Popen(["python", "main.py"])  
    print("New execution started.")

def start_scheduler(interval_minutes):
    while True:
        run_main_script()  # Start or restart the process
        time.sleep(interval_minutes * 60)  # Wait for the specified interval

# Set the interval in minutes
interval_minutes = 1440 
print(f"Scheduler started. Running main.py every {interval_minutes} minutes.")
start_scheduler(interval_minutes)
