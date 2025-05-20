
import platform
import subprocess
import json
import time
import hashlib
import os
import threading
import requests
import sys

REPORT_URL = "https://example.com/report" 
INTERVAL_SECONDS = 1800  

previous_state_file = "last_state.json"

def get_os():
    return platform.system()

def hash_state(data):
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()

def get_disk_encryption_status():
    os_type = get_os()
    try:
        if os_type == "Windows":
            output = subprocess.check_output(["manage-bde", "-status"], stderr=subprocess.DEVNULL, text=True)
            return "Percentage Encrypted: 100%" in output
        elif os_type == "Darwin":
            output = subprocess.check_output(["fdesetup", "status"], stderr=subprocess.DEVNULL, text=True)
            return "FileVault is On" in output
        elif os_type == "Linux":
            output = subprocess.check_output(["lsblk", "-o", "NAME,TYPE"], text=True)
            return "crypt" in output
    except Exception:
        return False

def get_os_update_status():
    os_type = get_os()
    try:
        if os_type == "Windows":
            output = subprocess.check_output(
                ["powershell", "-Command", "(New-Object -ComObject Microsoft.Update.AutoUpdate).DetectNow()"],
                stderr=subprocess.DEVNULL,
                text=True
            )
            return True
        elif os_type == "Darwin":
            output = subprocess.check_output(["softwareupdate", "-l"], stderr=subprocess.DEVNULL, text=True)
            return "No new software available" in output
        elif os_type == "Linux":
            output = subprocess.check_output(["apt", "list", "--upgradable"], stderr=subprocess.DEVNULL, text=True)
            return "upgradable" not in output
    except Exception:
        return False

def get_antivirus_status():
    os_type = get_os()
    try:
        if os_type == "Windows":
            output = subprocess.check_output(
                ["powershell", "-Command", "Get-MpComputerStatus"],
                stderr=subprocess.DEVNULL,
                text=True
            )
            return "AMServiceEnabled" in output
        elif os_type == "Darwin":
            output = subprocess.check_output(["pgrep", "XProtect"], stderr=subprocess.DEVNULL)
            return bool(output.strip())
        elif os_type == "Linux":
            output = subprocess.check_output(["systemctl", "is-active", "clamav-daemon"], stderr=subprocess.DEVNULL, text=True)
            return "active" in output
    except Exception:
        return False

def get_sleep_setting():
    os_type = get_os()
    try:
        if os_type == "Windows":
            output = subprocess.check_output(
                ["powershell", "-Command", "(Get-ItemProperty -Path 'HKCU:\Control Panel\PowerCfg\PowerPolicies\0').Policies"],
                stderr=subprocess.DEVNULL,
                text=True
            )
            return True  
        elif os_type == "Darwin":
            output = subprocess.check_output(["pmset", "-g", "custom"], stderr=subprocess.DEVNULL, text=True)
            return "sleep" in output.lower()
        elif os_type == "Linux":
            output = subprocess.check_output(["gsettings", "get", "org.gnome.settings-daemon.plugins.power", "sleep-inactive-ac-timeout"], stderr=subprocess.DEVNULL, text=True)
            timeout = int(output.strip())
            return timeout <= 600
    except Exception:
        return False

def collect_system_data():
    return {
        "disk_encryption": get_disk_encryption_status(),
        "os_up_to_date": get_os_update_status(),
        "antivirus_active": get_antivirus_status(),
        "sleep_timeout_valid": get_sleep_setting(),
        "hostname": platform.node(),
        "platform": platform.platform()
    }

def read_previous_state():
    if os.path.exists(previous_state_file):
        with open(previous_state_file, "r") as f:
            return json.load(f)
    return None

def write_current_state(data):
    with open(previous_state_file, "w") as f:
        json.dump(data, f)

def send_data(data):
    try:
        response = requests.post(REPORT_URL, json=data)
        print(f"Data sent: {response.status_code}")
    except Exception as e:
        print(f"Failed to send data: {e}")

def check_and_report():
    while True:
        current_data = collect_system_data()
        prev_data = read_previous_state()

        if prev_data is None or hash_state(prev_data) != hash_state(current_data):
            send_data(current_data)
            write_current_state(current_data)

        time.sleep(INTERVAL_SECONDS)

if __name__ == "__main__":
    print("Starting system health monitor daemon...")
    thread = threading.Thread(target=check_and_report, daemon=True)
    thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting.")
