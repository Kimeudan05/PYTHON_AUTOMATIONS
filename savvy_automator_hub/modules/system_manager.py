import os
import platform
import subprocess


def run(log_func=None):
    """
    Launches a simple console selection for system operations.
    (In GUI, we call each function separately.)
    """
    if log_func:
        log_func("System Manager module loaded.")


def restart(log_func=None):
    if log_func:
        log_func("🔄 Restarting system...")
    system = platform.system()
    try:
        if system == "Windows":
            subprocess.run(["shutdown", "/r", "/t", "5"])
        elif system == "Linux" or system == "Darwin":
            subprocess.run(["sudo", "reboot"])
        if log_func:
            log_func("✅ Restart command executed.")
    except Exception as e:
        if log_func:
            log_func(f"⚠️ Error restarting: {e}")


def shutdown(log_func=None):
    if log_func:
        log_func("⛔ Shutting down system...")
    system = platform.system()
    try:
        if system == "Windows":
            subprocess.run(["shutdown", "/s", "/t", "5"])
        elif system == "Linux" or system == "Darwin":
            subprocess.run(["sudo", "shutdown", "now"])
        if log_func:
            log_func("✅ Shutdown command executed.")
    except Exception as e:
        if log_func:
            log_func(f"⚠️ Error shutting down: {e}")


def lock(log_func=None):
    if log_func:
        log_func("🔒 Locking system...")
    system = platform.system()
    try:
        if system == "Windows":
            subprocess.run("rundll32.exe user32.dll,LockWorkStation")
        elif system == "Linux":
            subprocess.run(["gnome-screensaver-command", "-l"])
        elif system == "Darwin":
            subprocess.run(
                [
                    "/System/Library/CoreServices/Menu Extras/User.menu/Contents/Resources/CGSession",
                    "-suspend",
                ]
            )
        if log_func:
            log_func("✅ Lock command executed.")
    except Exception as e:
        if log_func:
            log_func(f"⚠️ Error locking: {e}")


def sleep(log_func=None):
    if log_func:
        log_func("💤 Putting system to sleep...")
    system = platform.system()
    try:
        if system == "Windows":
            subprocess.run("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        elif system == "Linux":
            subprocess.run(["systemctl", "suspend"])
        elif system == "Darwin":
            subprocess.run(["pmset", "sleepnow"])
        if log_func:
            log_func("✅ Sleep command executed.")
    except Exception as e:
        if log_func:
            log_func(f"⚠️ Error putting system to sleep: {e}")
