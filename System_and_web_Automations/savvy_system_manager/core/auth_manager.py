# core/auth_manager.py
import win32security
import win32api
from tkinter import simpledialog, Tk


def verify_user(gui_mode=False):
    """
    Verify the current user's password.
    - gui_mode=True -> show masked Tkinter dialog
    Returns True if credentials validated, False otherwise.
    """
    user = win32api.GetUserName()

    if gui_mode:
        root = Tk()
        root.withdraw()
        password = simpledialog.askstring(
            "Authorization Required", f"Enter password for {user}:", show="*"
        )
        root.destroy()
        if not password:
            return False
    else:
        import getpass

        password = getpass.getpass(f"Enter password for {user}: ")

    try:
        # Attempt an interactive logon with provided password (does not create session here)
        token = win32security.LogonUser(
            user,
            None,
            password,
            win32security.LOGON32_LOGON_INTERACTIVE,
            win32security.LOGON32_PROVIDER_DEFAULT,
        )
        token.Close()
        return True
    except Exception:
        return False
