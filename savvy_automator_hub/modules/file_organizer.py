import os
import shutil
from datetime import datetime


def run(log_func=None):
    """
    Organizes files in the user's Downloads folder by file type.
    """
    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
    if not os.path.exists(downloads_path):
        if log_func:
            log_func("❌ Downloads folder not found.")
        return

    if log_func:
        log_func(f"📁 Scanning: {downloads_path}")

    try:
        count = 0
        for filename in os.listdir(downloads_path):
            file_path = os.path.join(downloads_path, filename)

            if os.path.isdir(file_path):
                continue

            ext = os.path.splitext(filename)[1].lower().strip(".")
            if not ext:
                ext = "no_extension"

            target_dir = os.path.join(downloads_path, ext.upper())
            os.makedirs(target_dir, exist_ok=True)

            dest_path = os.path.join(target_dir, filename)

            # Avoid overwriting
            if os.path.exists(dest_path):
                base, extn = os.path.splitext(filename)
                new_name = f"{base}_{datetime.now().strftime('%H%M%S')}{extn}"
                dest_path = os.path.join(target_dir, new_name)

            shutil.move(file_path, dest_path)
            count += 1
            if log_func:
                log_func(f"Moved: {filename} → {ext.upper()}/")

        if log_func:
            log_func(f"✅ Organized {count} files successfully.")
    except Exception as e:
        if log_func:
            log_func(f"⚠️ Error: {e}")
