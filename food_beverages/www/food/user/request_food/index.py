import frappe
from datetime import datetime,time

def get_current_date():
    today = datetime.now()
    dd = today.strftime('%d')
    mm = today.strftime('%m')
    yyyy = today.strftime('%Y')

    return f"{yyyy}-{mm}-{dd}"

@frappe.whitelist()
def fill_form(Breakfast,Breakfast_location,Lunch,Lunch_location,Dinner,Dinner_location,Refreshments,Refreshments_location,food_type_breakfast_data,food_type_lunch_data,food_type_dinner_data,date,employeeId,employeeName):
    if Breakfast not in ['Yes', 'No', '']:
        Breakfast = ''

    if Breakfast not in ['Yes', 'No', '']:
        Breakfast = ''

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
        current_minute = datetime.now().minute
        current_time_in_minutes = current_hour * 60 + current_minute
        if current_date == selected_date and current_hour >= 5:
            doc = frappe.new_doc('Food Request') 
            doc.request_type = 'Breakfast'
            doc.need = 'No'
            doc.location = ''
            doc.attend = 'No'
            doc.food_preference = food_type_breakfast_data
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
            doc.food_preference = food_type_breakfast_data
            doc.emp_id = employeeId
            doc.user_name = employeeName
            doc.date = date
            doc.insert()
        if current_date == selected_date and current_time_in_minutes >= 9 * 60 + 30:
            doc = frappe.new_doc('Food Request') 
            doc.request_type = 'Lunch'
            doc.need = 'No'
            doc.location = ''
            doc.food_preference = ''
            doc.attend = 'No'
            doc.food_preference = food_type_lunch_data
            doc.emp_id = employeeId
            doc.user_name = employeeName
            doc.date = date
            doc.insert()
        else:
            doc = frappe.new_doc('Food Request') 
            doc.request_type = 'Lunch'
            doc.need = Lunch
            doc.location = Lunch_location
            doc.food_preference = food_type_lunch_data
            doc.attend = 'No'
            doc.emp_id = employeeId
            doc.user_name = employeeName
            doc.date = date
            doc.insert()
        if current_date == selected_date and current_hour >= 16:
            doc = frappe.new_doc('Food Request') 
            doc.request_type = 'Dinner'
            doc.need = 'No'
            doc.location = ''
            doc.attend = 'No'
            doc.food_preference = food_type_dinner_data
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
            doc.food_preference = food_type_dinner_data
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


@frappe.whitelist()
def get_prefrence_data(day):
    # Define a dictionary mapping day numbers to their corresponding values
    day_values = {
        1: 'mon_f_type',
        2: 'tue_f_type',
        3: 'wed_f_type',
        4: 'thu_f_type',
        5: 'fri_f_type',
        6: 'sat_f_type',
        0: 'sun_f_type'
    }

    # Check if the day value exists in the keys of the day_values dictionary
    if int(day) in day_values:
        field_key = day_values[int(day)]  # Get the corresponding key from the dictionary
        sql_query = f"""
            SELECT location, meal_type, {field_key} AS type
            FROM `tabFood Menu`
        """
        existing_record = frappe.db.sql(sql_query, as_dict=True)
        if existing_record:
            return existing_record
        else:
            return "Record Doesn't Exist!"
    else:
        return "Invalid day number"