import frappe
from datetime import datetime,time
from frappe.utils import now_datetime
import time
from frappe import db

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


@frappe.whitelist()
def update_current_date():
    
    records = frappe.get_all(
        'Quotes',
        fields=['name'],
        order_by='date asc',
        limit_page_length=1
    )
    if records:
        record = records[0]
        id = record.get('name')

        doctype = "Quotes"
        docname = id
        fields_to_update = {
        "date": frappe.utils.nowdate()
        }
        try:
            db.set_value(doctype, docname, fields_to_update)
            return 'Success'
        except Exception as e:
            return e








# @frappe.whitelist()
# def get_daily_quote():
#     # Get the current date
#     current_date = frappe.utils.nowdate()

#     # # Get the quote for the current date
#     # quote = frappe.get_value('Quotes', {'date': current_date}, 'quotes',limit=1)

#     # return quote

#     # Get the quote for the current date with limit 1
#     quote = frappe.get_all(
#         'Quotes',
#         filters={'date': current_date},
#         fields=['quotes'],
#         limit_page_length=1
#     )

#     return quote[0]['quotes'] if quote else None



@frappe.whitelist()
def get_daily_quote():
    # Get the latest quote based on creation date in ascending order
    quote = frappe.get_all(
        'Quotes',
        fields=['name', 'quotes'],
        order_by='date ASC',
        limit_page_length=1
    )

    if quote:
        # Update the quote record with the current date
        current_datetime = now_datetime()
        frappe.db.set_value('Quotes', quote[0]['name'], 'date',  current_datetime)
        return quote[0]['quotes']
    else:
        return None