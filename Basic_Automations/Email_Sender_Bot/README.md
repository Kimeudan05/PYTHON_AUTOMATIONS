# 📧 Email Automation Bot – Weekly Sales Reports (v1.0.0)

This Python automation project sends personalized **weekly sales reports** via email using **Yagmail**, **Matplotlib**, and **ReportLab**.  
It also automatically cleans up temporary files such as charts and PDFs after sending.

---

## 🧩 Features

- Generates a personalized report for each recipient.
- Embeds inline sales charts directly in the email.
- Attaches a professional PDF report.
- Cleans up `/inline_charts` and `/pdf_reports` after sending.
- Logs all send events in `logs/email_log.txt`.
- Configurable scheduling (runs every Monday at 8 AM).

## 🏗 Folder Structure

```
Email_Sender_Bot/
├── main.py
├── generate_reports.py
├── pdf_generator.py
├── send_email.py
├── yagmail_config.py
├── data/
│ └── sales_data.xlsx
├── logs/
│ └── email_log.txt
├── inline_charts/ # temp (auto-deleted)
├── pdf_reports/ # temp (auto-deleted)
├── .env
└── README.md
```

## ⚙️ Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/kimeudan05/python-automations.git
   cd python-automations/Basic_Automations/Email_Reports_Automation
   ```
2. Install dependencies

   ```bash
   pip install -r requirements.txt
   ```

3. create a .env file

```ini
SENDER_EMAIL=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
```

- use this link to create an app password for your gmail configuration

https://myaccount.google.com/apppasswords

4. Run the automation

```
python main.py
```

🧹 Auto-Cleanup

After sending all emails:

- inline_charts/ and pdf_reports/ are automatically deleted.

- Logs are preserved in logs/email_log.txt.

#### 🧠 Example Output

An email includes:

- Personalized greeting

- Clean data table

- Embedded chart (inline)

- Attached PDF report

#### Dependencies

```
yagmail
pandas
matplotlib
jinja2
reportlab
schedule
python-dotenv
```

### 🏷 Version Info

Tag: `email_reports_v1.0.0`

Release Notes:

- Added inline chart support

- Added PDF generation

- Added automatic cleanup of temp folders

- Added detailed email logging
