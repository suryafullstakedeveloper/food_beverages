import frappe
from datetime import datetime,time

def get_current_date():
    today = datetime.now()
    dd = today.strftime('%d')
    mm = today.strftime('%m')
    yyyy = today.strftime('%Y')

    return f"{yyyy}-{mm}-{dd}"

@frappe.whitelist()
def Get_Food_Menu(location):
    Breakfast = frappe.get_all(
        'Food Menu',
        filters={'location': location,'meal_type':'Breakfast'},
        fields=['mon','tue','wed','thu','fri','sat']
    )

    Lunch = frappe.get_all(
        'Food Menu',
        filters={'location': location,'meal_type':'Lunch'},
        fields=['mon','tue','wed','thu','fri','sat']
    )

    Dinner = frappe.get_all(
        'Food Menu',
        filters={'location': location,'meal_type':'Dinner'},
        fields=['mon','tue','wed','thu','fri','sat']
    )

    foodmenu = {
        'Breakfast': Breakfast,
        'Lunch': Lunch,
        'Dinner': Dinner
    }
    return foodmenu

   


            