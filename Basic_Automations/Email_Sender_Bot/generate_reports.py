import pandas as pd
import matplotlib.pyplot as plt
from jinja2 import Template
import os

INLINE_CHARTS_DIR = "inline_charts"
os.makedirs(INLINE_CHARTS_DIR, exist_ok=True)


def load_data():
    """Load sales data from Excel"""
    return pd.read_excel("data/sales_data.xlsx")  # columns: Name, Email, Product, Sales


def generate_chart(df, recipient_name):
    """Generate chart for a single recipient"""
    plt.figure(figsize=(6, 4))
    plt.bar(df["Product"], df["Sales"], color="skyblue")
    plt.title(f"Weekly Sales - {recipient_name}")
    plt.ylabel("Units Sold")
    plt.tight_layout()
    chart_path = os.path.join(INLINE_CHARTS_DIR, f"{recipient_name}_chart.png")
    plt.savefig(chart_path)
    plt.close()
    return chart_path


def generate_email_body(df, recipient_name, chart_path):
    """Generate personalized HTML email body with inline chart and clean styling"""
    template_str = """
    <div style="font-family: Arial, sans-serif; color: #333;">
        <h2 style="color: #2E86C1;">Hello {{ name }},</h2>
        <p>Here is your personalized <b>weekly sales report</b>:</p>

        <table style="border-collapse: collapse; width: 60%; margin-top: 10px; margin-bottom: 20px;">
            <thead>
                <tr style="background-color: #2E86C1; color: white; text-align: left;">
                    <th style="padding: 8px; border: 1px solid #ddd;">Product</th>
                    <th style="padding: 8px; border: 1px solid #ddd;">Sales</th>
                </tr>
            </thead>
            <tbody>
                {% for product, sales in data.items() %}
                <tr style="background-color: {% if loop.index0 % 2 == 0 %}#f9f9f9{% else %}#ffffff{% endif %};">
                    <td style="padding: 8px; border: 1px solid #ddd;">{{ product }}</td>
                    <td style="padding: 8px; border: 1px solid #ddd;">{{ sales }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>

        <h3 style="color: #2E86C1;">Chart Summary</h3>

        <p style="margin-top: 20px;">Best Regards,<br><b>Automation Bot 🤖</b></p>
    </div>
    """
    from jinja2 import Template

    template = Template(template_str)

    body = template.render(
        name=recipient_name,
        data=df.set_index("Product")["Sales"].to_dict(),
        chart_cid=f"cid:{os.path.basename(chart_path)}",
    )
    return body, chart_path
