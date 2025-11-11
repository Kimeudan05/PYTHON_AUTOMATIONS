import subprocess
import platform


def ensure_pswindowsupdate():
    """Ensure the PSWindowsUpdate module is installed and imported"""
    subprocess.run(
        [
            "powershell",
            "-Command",
            "if (!(Get-Module -ListAvailable -Name PSWindowsUpdate)) "
            "{ Install-Module -Name PSWindowsUpdate -Force -Confirm:$false }",
        ],
        capture_output=True,
        text=True,
    )


def install_updates():
    """Install system updates (requires admin privileges)"""
    if platform.system() == "Windows":
        ensure_pswindowsupdate()
        # Launch elevated PowerShell to run Install-WindowsUpdate
        subprocess.run(
            [
                "powershell",
                "-Command",
                "Start-Process powershell "
                "'-NoProfile -Command \"Import-Module PSWindowsUpdate; Install-WindowsUpdate -AcceptAll -AutoReboot\"' "
                "-Verb RunAs",
            ]
        )


def check_updates():
    """Check for system updates"""
    if platform.system() == "Windows":
        result = subprocess.run(
            ["powershell", "Get-WindowsUpdate"], capture_output=True, text=True
        )
        return result.stdout
    return "Updates check only supported on Windows."
