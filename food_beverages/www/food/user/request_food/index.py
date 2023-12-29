import frappe
from datetime import datetime,time

def get_current_date():
    today = datetime.now()
    dd = today.strftime('%d')
    mm = today.strftime('%m')
    yyyy = today.strftime('%Y')

    return f"{yyyy}-{mm}-{dd}"

@frappe.whitelist()
def fill_form(Breakfast,Breakfast_location,Lunch,Lunch_location,Dinner,Dinner_location,Refreshments,Refreshments_location,date,employeeId,employeeName):
    existing_record = frappe.get_all(
        'Food Request',
        filters={'emp_id': employeeId, 'date': date},
        fields=['id']
    )
    if existing_record:
        return "Record Exists!"

    else:
        selected_date = date
        current_date = get_current_date()
        current_hour = datetime.now().hour
        if current_date == selected_date and current_hour >= 6:
            doc = frappe.new_doc('Food Request') 
            doc.request_type = 'Breakfast'
            doc.need = 'No'
            doc.location = ''
            doc.attend = 'No'
            doc.emp_id = employeeId
            doc.user_name = employeeName
            doc.date = date
            doc.insert()
        else:
            doc = frappe.new_doc('Food Request') 
            doc.request_type = 'Breakfast'
            doc.need = Breakfast
            doc.location = Breakfast_location
            doc.attend = 'No'
            doc.emp_id = employeeId
            doc.user_name = employeeName
            doc.date = date
            doc.insert()
        if current_date == selected_date and current_hour >= 10:
            doc = frappe.new_doc('Food Request') 
            doc.request_type = 'Lunch'
            doc.need = 'No'
            doc.location = ''
            doc.attend = 'No'
            doc.emp_id = employeeId
            doc.user_name = employeeName
            doc.date = date
            doc.insert()
        else:
            doc = frappe.new_doc('Food Request') 
            doc.request_type = 'Lunch'
            doc.need = Lunch
            doc.location = Lunch_location
            doc.attend = 'No'
            doc.emp_id = employeeId
            doc.user_name = employeeName
            doc.date = date
            doc.insert()
        if current_date == selected_date and current_hour >= 17:
            doc = frappe.new_doc('Food Request') 
            doc.request_type = 'Dinner'
            doc.need = 'No'
            doc.location = ''
            doc.attend = 'No'
            doc.emp_id = employeeId
            doc.user_name = employeeName
            doc.date = date
            doc.insert()
        else:
            doc = frappe.new_doc('Food Request') 
            doc.request_type = 'Dinner'
            doc.need = Dinner
            doc.location = Dinner_location
            doc.attend = 'No'
            doc.emp_id = employeeId
            doc.user_name = employeeName
            doc.date = date
            doc.insert()
        doc = frappe.new_doc('Food Request') 
        doc.request_type = 'Refreshments'
        doc.need = Refreshments
        doc.location = Refreshments_location
        doc.attend = 'No'
        doc.emp_id = employeeId
        doc.user_name = employeeName
        doc.date = date
        doc.insert()

        return "Request Successfull.."


            