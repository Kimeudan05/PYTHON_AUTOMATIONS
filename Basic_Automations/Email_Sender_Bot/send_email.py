from yagmail_config import yag


def send_email(to, subject, body, attachments=None, cc=None):
    try:
        # Passing content inside HTML tags to content argument
        yag.send(to=to, subject=subject, contents=body, attachments=attachments, cc=cc)
        print(f"Email send to {to}")
        return True
    except Exception as e:
        print(f"Failed to send email :{e}")
        return False


# an example
if __name__ == "__main__":
    recipients = [
        "savvysolvetech@gmail.com",
        "kimeu.daniel@students.kyu.ac.ke",
    ]
    subject = "Test From Automation Bot"
    body = """
    <h1>hello,</h1>  
    <p>This is a test send from a python Email bot\n
    See you soon</p>
    """
    att = [
        "D:/PYTHON AUTOMATIONS/Basic_Automations/File_Organizer_Bot/file_organizer_gui_custom.py",
        "D:/PYTHON AUTOMATIONS/Basic_Automations/Email_Sender_Bot/config.py",
    ]
    send_email(recipients, subject, body, attachments=att)
