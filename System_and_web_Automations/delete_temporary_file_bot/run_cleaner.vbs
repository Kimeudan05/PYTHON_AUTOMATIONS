' this prevents the terminal from opening '

Set WshShell = CreateObject("WScript.Shell")
WshShell.Run """D:\PYTHON AUTOMATIONS\system_and_web_automations\delete_temporary_file_bot\run_cleaner.bat""", 0, False
