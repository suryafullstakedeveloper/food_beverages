import frappe
from datetime import datetime,time
from frappe import db
import time
import pytz    
tz_NY = pytz.timezone('Asia/Kolkata')

def get_current_date():
    today = datetime.now()
    dd = today.strftime('%d')
    mm = today.strftime('%m')
    yyyy = today.strftime('%Y')

    return f"{yyyy}-{mm}-{dd}"


def get_part_by_index(input_string, index):
    parts = input_string.split('/')
    if 0 <= index < len(parts):
        return parts[index]
    else:
        return None

def find_meal_type():
    currentdate = get_current_date()
    today = datetime.now(tz_NY)
    current_hour = today.hour
    current_minute = today.minute
    current_time_in_minutes = current_hour * 60 + current_minute

    if current_time_in_minutes <= 10 * 60 + 40:
        return "Breakfast"
    elif current_time_in_minutes <= 15 * 60 + 45:
        return "Lunch"
    elif current_time_in_minutes <= 22 * 60 + 30:
        return "Dinner"
    else :
        return ""



@frappe.whitelist()
def QrValidation(Qrcontent,location_value):
    request_type = find_meal_type()
    today = get_current_date()
    employee_id = get_part_by_index(Qrcontent,0)
    GivenFoodtype = get_part_by_index(Qrcontent,1)
    GIvendate = get_part_by_index(Qrcontent,2)

    if(request_type != GivenFoodtype or  GIvendate != today):
        return "Invalid QR"

    records = frappe.get_all(
        'Food Request',
        filters={'request_type': request_type,'emp_id': employee_id,'date': today,'need':'Yes'},
        fields=['location','name','attend','user_name']
    )
    if records:
        record = records[0]
        Empname = record.get('user_name')
        location = record.get('location')
        if record.get('location') == location_value:
            if record.get('attend') != 'Yes':

                id = record.get('name')
                doctype = "Food Request"
                docname = id
                fields_to_update = {
                "attend": "Yes",
                }
                try:
                    db.set_value(doctype, docname, fields_to_update)
                    return 'Success'
                except Exception as e:
                    return e
            else :
                return 'You have already scanned Today for the ' + request_type +','+Empname+'.'
        else:
            return  'At this location, you do not have a reservation for your meal. You have a reservation at the '+ location +' site.'
    else:
        return 'You do not have a reservation for '+ request_type+'.'





@frappe.whitelist()
def QrValidation_shar(Qrcontent,location_value):
    request_type = find_meal_type()
    today = get_current_date()
    employee_id = get_part_by_index(Qrcontent,1)
    

    records = frappe.get_all(
        'Food Request',
        filters={'request_type': request_type,'emp_id': employee_id,'date': today,'need':'Yes'},
        fields=['location','name','attend','user_name']
    )
    if records:
        record = records[0]
        Empname = record.get('user_name')
        location = record.get('location')
        if record.get('location') == location_value:
            if record.get('attend') != 'Yes':

                id = record.get('name')
                doctype = "Food Request"
                docname = id
                fields_to_update = {
                "attend": "Yes",
                }
                try:
                    db.set_value(doctype, docname, fields_to_update)
                    return 'Success'
                except Exception as e:
                    return e
            else :
                return 'You have already scanned Today for the ' + request_type +','+Empname+'.'
        else:
            return  'At this location, you do not have a reservation for your meal. You have a reservation at the '+ location +' site.'
    else:
        return 'You do not have a reservation for '+ request_type+'.'





