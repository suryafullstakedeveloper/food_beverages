import frappe
import json
from datetime import datetime,time ,timedelta
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
def Food_menu_update(id,field,value):
   
    doctype = "Food Menu"
    docname = id
    # field_name = "location"
    # new_value = value
    fields_to_update = {
    field: value,
    # Add more fields as needed
    }
    try:
        db.set_value(doctype, docname, fields_to_update)
        # time.sleep(5)
        return True 
    except Exception as e:
        return e


@frappe.whitelist()
def Get_Beverages(location):
    existing_record = frappe.get_all(
        'Beverage Menu',
        filters={'location': location},
        fields=['name','item','mon','tue','wed','thu','fri','sat'],
        order_by='name'
    )
    if existing_record:
        return existing_record




@frappe.whitelist()
def beverage_menu_update(id,obj):

    obj_dict = json.loads(obj)
    mon = obj_dict.get("mon")
    tue = obj_dict.get("tue")
    wed = obj_dict.get("wed")
    thu = obj_dict.get("thu")
    fri = obj_dict.get("fri")
    sat = obj_dict.get("sat")

    doctype = "Beverage Menu"
    docname = id
    fields_to_update = {
    'mon': mon,
    'tue': tue,
    'wed': wed,
    'thu': thu,
    'fri': fri,
    'sat': sat,
    }
    try:
        db.set_value(doctype, docname, fields_to_update)
        # time.sleep(5)
        return True 
    except Exception as e:
        return e
