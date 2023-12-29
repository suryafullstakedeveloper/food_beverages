import frappe
from datetime import datetime,time
# import schedule
import time

def get_current_date():
    today = datetime.now()
    dd = today.strftime('%d')
    mm = today.strftime('%m')
    yyyy = today.strftime('%Y')

    return f"{yyyy}-{mm}-{dd}"

@frappe.whitelist()
def Get_Beverages(location):
    existing_record = frappe.get_all(
        'Beverage Menu',
        filters={'location': location},
        fields=['item','mon','tue','wed','thu','fri','sat']
    )
    if existing_record:
        return existing_record


def update_current_date():
    # Get the record with the oldest date
    doc = frappe.get_doc({
        "doctype": "Quotes",
        "order_by": "date desc",
        "limit_page_length": 1
    })

    if doc:
        # Update the record with the current date
        doc.date = frappe.utils.nowdate()
        doc.save()

# Schedule the job to run daily at a specific time (adjust as needed)
# schedule.every().day.at("08:00").do(update_current_date)

# # Infinite loop to keep the script running
# while True:
#     schedule.run_pending()
#     time.sleep(1)


@frappe.whitelist()
def get_daily_quote():
    # Get the current date
    current_date = frappe.utils.nowdate()

    # # Get the quote for the current date
    # quote = frappe.get_value('Quotes', {'date': current_date}, 'quotes',limit=1)

    # return quote

    # Get the quote for the current date with limit 1
    quote = frappe.get_all(
        'Quotes',
        filters={'date': current_date},
        fields=['quotes'],
        limit_page_length=1
    )

    return quote[0]['quotes'] if quote else None
