import frappe
from datetime import datetime,time ,timedelta
from frappe import db
import calendar


def get_current_date():
    today = datetime.now()
    dd = today.strftime('%d')
    mm = today.strftime('%m')
    yyyy = today.strftime('%Y')

    return f"{yyyy}-{mm}-{dd}"

def date_convertion(date):
    dd = date.strftime('%d')
    mm = date.strftime('%m')
    yyyy = date.strftime('%Y')

    return f"{yyyy}-{mm}-{dd}"



@frappe.whitelist()
def getroledetail():
    return 'test'

    # Get_role_List = frappe.get_all(
    #     'Food Vendor',
    #     filters={"vendor_id":vendor_id},
    #     fields=['name']
    # )

    # if Get_role_List:
    #     return 'Record exists!'
    # else:
    #     'No User Found!'

