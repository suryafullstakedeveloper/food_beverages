import frappe
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
def GetTableValues(location):

    breakfast_records = frappe.get_all(
        'Food Menu',
        filters={'location': location,'meal_type':'Breakfast'},
        fields=['name','mon','tue','wed','thu','fri','sat','sun','meal_type','meal_type','mon_f_type','tue_f_type','wed_f_type','thu_f_type','fri_f_type','sat_f_type','sun_f_type']
    )

    lunch_records = frappe.get_all(
        'Food Menu',
        filters={'location': location,'meal_type':'Lunch'},
        fields=['name','mon','tue','wed','thu','fri','sat','sun','meal_type','mon_f_type','tue_f_type','wed_f_type','thu_f_type','fri_f_type','sat_f_type','sun_f_type']
    )

    dinner_records = frappe.get_all(
        'Food Menu',
        filters={'location': location,'meal_type':'Dinner'},
        fields=['name','mon','tue','wed','thu','fri','sat','sun','meal_type','meal_type','mon_f_type','tue_f_type','wed_f_type','thu_f_type','fri_f_type','sat_f_type','sun_f_type']
    )
    
    breakfast_values = []
    lunch_values = []
    dinner_values = []
    for breakfast in breakfast_records:
        breakfast_values.append({'name': breakfast.name, 'Day':'mon', 'value': breakfast.mon, 'meal_type': breakfast.meal_type , 'meal_prefrence' : breakfast.mon_f_type})
        breakfast_values.append({'name': breakfast.name, 'Day':'tue', 'value': breakfast.tue, 'meal_type': breakfast.meal_type , 'meal_prefrence' : breakfast.tue_f_type})
        breakfast_values.append({'name': breakfast.name, 'Day':'wed', 'value': breakfast.wed, 'meal_type': breakfast.meal_type , 'meal_prefrence' : breakfast.wed_f_type})
        breakfast_values.append({'name': breakfast.name, 'Day':'thu', 'value': breakfast.thu, 'meal_type': breakfast.meal_type , 'meal_prefrence' : breakfast.thu_f_type})
        breakfast_values.append({'name': breakfast.name, 'Day':'fri', 'value': breakfast.fri, 'meal_type': breakfast.meal_type , 'meal_prefrence' : breakfast.fri_f_type})
        breakfast_values.append({'name': breakfast.name, 'Day':'sat', 'value': breakfast.sat, 'meal_type': breakfast.meal_type , 'meal_prefrence' : breakfast.sat_f_type})
        breakfast_values.append({'name': breakfast.name, 'Day':'sun', 'value': breakfast.sun, 'meal_type': breakfast.meal_type , 'meal_prefrence' : breakfast.sun_f_type})
    
    for lunch in lunch_records:
        lunch_values.append({'name': lunch.name, 'Day':'mon', 'value': lunch.mon, 'meal_type': lunch.meal_type , 'meal_prefrence' : lunch.mon_f_type})
        lunch_values.append({'name': lunch.name, 'Day':'tue', 'value': lunch.tue, 'meal_type': lunch.meal_type , 'meal_prefrence' : lunch.tue_f_type})
        lunch_values.append({'name': lunch.name, 'Day':'wed', 'value': lunch.wed, 'meal_type': lunch.meal_type , 'meal_prefrence' : lunch.wed_f_type})
        lunch_values.append({'name': lunch.name, 'Day':'thu', 'value': lunch.thu, 'meal_type': lunch.meal_type , 'meal_prefrence' : lunch.thu_f_type})
        lunch_values.append({'name': lunch.name, 'Day':'fri', 'value': lunch.fri, 'meal_type': lunch.meal_type , 'meal_prefrence' : lunch.fri_f_type})
        lunch_values.append({'name': lunch.name, 'Day':'sat', 'value': lunch.sat, 'meal_type': lunch.meal_type , 'meal_prefrence' : lunch.sat_f_type})
        lunch_values.append({'name': lunch.name, 'Day':'sun', 'value': lunch.sun, 'meal_type': lunch.meal_type , 'meal_prefrence' : lunch.sun_f_type})

    for dinner in dinner_records:
        dinner_values.append({'name': dinner.name, 'Day':'mon', 'value': dinner.mon, 'meal_type': dinner.meal_type , 'meal_prefrence' : dinner.mon_f_type})
        dinner_values.append({'name': dinner.name, 'Day':'tue', 'value': dinner.tue, 'meal_type': dinner.meal_type , 'meal_prefrence' : dinner.tue_f_type})
        dinner_values.append({'name': dinner.name, 'Day':'wed', 'value': dinner.wed, 'meal_type': dinner.meal_type , 'meal_prefrence' : dinner.wed_f_type})
        dinner_values.append({'name': dinner.name, 'Day':'thu', 'value': dinner.thu, 'meal_type': dinner.meal_type , 'meal_prefrence' : dinner.thu_f_type})
        dinner_values.append({'name': dinner.name, 'Day':'fri', 'value': dinner.fri, 'meal_type': dinner.meal_type , 'meal_prefrence' : dinner.fri_f_type})
        dinner_values.append({'name': dinner.name, 'Day':'sat', 'value': dinner.sat, 'meal_type': dinner.meal_type , 'meal_prefrence' : dinner.sat_f_type})
        dinner_values.append({'name': dinner.name, 'Day':'sun', 'value': dinner.sun, 'meal_type': dinner.meal_type , 'meal_prefrence' : dinner.sun_f_type})
    
    Food_Menu = [
        {
            'Breakfast': breakfast_values,
            'Lunch': lunch_values,
            'Dinner': dinner_values,
        }
    ]
    return Food_Menu



@frappe.whitelist()
def Food_menu_update(id,field,value,food_type):
   
    doctype = "Food Menu"
    docname = id
    # field_name = "location"
    # new_value = value
    fields_to_update = {
    field: value,
    field+'_f_type': food_type,
    # Add more fields as needed
    }
    try:
        db.set_value(doctype, docname, fields_to_update)
        # time.sleep(5)
        return True 
    except Exception as e:
        return e



            