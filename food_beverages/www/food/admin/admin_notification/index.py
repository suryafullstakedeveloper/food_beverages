import frappe
from datetime import datetime,time ,timedelta
from collections import defaultdict
from frappe import db

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
def GetNotificationList():

    Notification_List = frappe.get_all(
        'Food Notification',
        fields=['title','name','description','end_date','location']
    )
    if Notification_List:
        return Notification_List




@frappe.whitelist()
def Add_Notification(Title,Description,End_Date,Location,employeeId):

    doc = frappe.new_doc('Food Notification') 
    doc.title = Title,
    doc.description = Description,
    doc.end_date = End_Date,
    doc.location = Location,
    doc.created_by = employeeId,
    doc.insert()

    return "Request Successfull.."




@frappe.whitelist()
def Edit_Notification(Title,Description,End_Date,Location,employeeId,id):
   
    doctype = "Food Notification"
    docname = id
    fields_to_update = {
    "title": Title,
    "description": Description,
    "end_date": End_Date,
    "location": Location,
    "modyfied_by": employeeId,
    # Add more fields as needed
    }
    try:
        db.set_value(doctype, docname, fields_to_update)
        # time.sleep(5)
        return True 
    except Exception as e:
        return e



@frappe.whitelist()
def delete_function(id):
    try:
        # Specify the doctype
        doctype = "Food Notification"
        
        # Get the document
        doc = frappe.get_doc(doctype, id)
        
        # Delete the document
        doc.delete()
        
        return True
    except Exception as e:
        return str(e)