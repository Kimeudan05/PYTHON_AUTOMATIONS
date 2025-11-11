import os
import shutil
import tempfile


def run(log_func=None):
    """
    Cleans temporary files, system temp folders, and cache files.
    """
    total_deleted = 0
    errors = 0

    def delete_path(path):
        nonlocal total_deleted, errors
        try:
            if os.path.isfile(path):
                os.remove(path)
                total_deleted += 1
                if log_func:
                    log_func(f"🗑️ Deleted file: {path}")
            elif os.path.isdir(path):
                shutil.rmtree(path, ignore_errors=True)
                total_deleted += 1
                if log_func:
                    log_func(f"🧩 Removed folder: {path}")
        except Exception as e:
            errors += 1
            if log_func:
                log_func(f"⚠️ Error deleting {path}: {e}")

    # 1️⃣ Clean system temp directory
    temp_dir = tempfile.gettempdir()
    if log_func:
        log_func(f"Cleaning system temp: {temp_dir}")

    for root, dirs, files in os.walk(temp_dir):
        for f in files:
            delete_path(os.path.join(root, f))
        for d in dirs:
            delete_path(os.path.join(root, d))

    # 2️⃣ Clean user cache/temp folders (like Downloads/.cache)
    home = os.path.expanduser("~")
    possible_dirs = [
        os.path.join(home, "Downloads"),
        os.path.join(home, "AppData", "Local", "Temp"),
        os.path.join(home, ".cache"),
    ]

    for directory in possible_dirs:
        if not os.path.exists(directory):
            continue

        if log_func:
            log_func(f"Scanning: {directory}")

        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith((".tmp", ".log", ".bak")):
                    delete_path(os.path.join(root, file))

    if log_func:
        log_func(
            f"✅ Cleaning complete. Deleted {total_deleted} items. Errors: {errors}."
        )
