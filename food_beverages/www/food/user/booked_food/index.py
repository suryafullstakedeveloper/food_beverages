import frappe
from datetime import datetime,time
from frappe import db
import time


@frappe.whitelist()
def datafetch(selectedDate,employeeId):
    existing_record = frappe.get_all(
        'Food Request',
        filters={'emp_id': employeeId, 'date': selectedDate ,'request_type': ['!=', 'Refreshments']},
        fields=['name','request_type','location','need']
    )
    if existing_record:
        # A record with the same employee_id and start_date already exists
        return existing_record
    else:
        return 'empty'

@frappe.whitelist()
def Booked_Meal_Update(id,value):
   
    doctype = "Food Request"
    docname = id
    # field_name = "location"
    # new_value = value
    fields_to_update = {
    "location": value,
    "need": "Yes",
    # Add more fields as needed
    }
    try:
        db.set_value(doctype, docname, fields_to_update)
        # time.sleep(5)
        return True 
    except Exception as e:
        return e

@frappe.whitelist()
def CancelFood(id):
   
    doctype = "Food Request"
    docname = id
    # field_name = "location"
    # new_value = value
    fields_to_update = {
    "location": '',
    "need": "No",
    # Add more fields as needed
    }
    try:
        db.set_value(doctype, docname, fields_to_update)
        # time.sleep(5)
        return True 
    except Exception as e:
        return e
