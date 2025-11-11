# core/system_actions.py
import os
import subprocess
import psutil
import time
import platform
from core.logger import log_action


def close_open_apps():
    """Close user applications except essential processes (keep explorer)."""
    for proc in psutil.process_iter(["pid", "name"]):
        try:
            name = (proc.info["name"] or "").lower()
            # keep explorer and python
            if name and name not in (
                "explorer.exe",
                "python.exe",
                "pythonw.exe",
                "system",
            ):
                # skip critical system processes by name heuristics
                if "svchost" in name or "system" in name:
                    continue
                proc.terminate()
        except Exception:
            pass
    time.sleep(2)


def restart_computer():
    """Restart computer (elevated on Windows)."""
    log_action("Attempting restart")
    if platform.system() == "Windows":
        # Use Start-Process with RunAs to ensure elevation (UAC)
        ps_cmd = "Start-Process -FilePath 'shutdown.exe' -ArgumentList '/r','/t','10' -Verb RunAs"
        subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], shell=True)
        return True
    else:
        os.system("sudo reboot")
        return True


def shutdown_computer():
    """Shutdown computer (elevated on Windows)."""
    log_action("Attempting shutdown")
    if platform.system() == "Windows":
        ps_cmd = "Start-Process -FilePath 'shutdown.exe' -ArgumentList '/s','/t','10' -Verb RunAs"
        subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], shell=True)
        return True
    else:
        os.system("sudo shutdown -h now")
        return True


def rename_computer(new_name):
    """
    Launch an elevated PowerShell process to rename the computer.
    This will prompt UAC. The rename takes effect on next restart.
    """
    if not new_name:
        log_action("Rename aborted: no name provided")
        return False

    if platform.system() != "Windows":
        # Linux rename
        try:
            os.system(f"sudo hostnamectl set-hostname {new_name}")
            log_action(f"Hostname changed to {new_name} (Linux)")
            return True
        except Exception as e:
            log_action(f"Rename failed (Linux): {e}")
            return False

    # Windows: use Start-Process -Verb RunAs to run Rename-Computer elevated
    # We build a PowerShell command that starts a new elevated PowerShell process which runs Rename-Computer -Force
    ps_inner = f"Rename-Computer -NewName '{new_name}' -Force"
    ps_cmd = f'Start-Process -FilePath powershell -ArgumentList "-NoProfile -Command {ps_inner}" -Verb RunAs'

    try:
        subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], shell=True)
        log_action(
            f"Rename command launched for {new_name} (elevated). Requires reboot."
        )
        return True
    except Exception as e:
        log_action(f"Rename failed to launch: {e}")
        return False
