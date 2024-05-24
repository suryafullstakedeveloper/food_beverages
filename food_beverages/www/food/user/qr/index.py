import frappe
from datetime import datetime,time
import time
import pytz    
tz_NY = pytz.timezone('Asia/Kolkata')

def get_current_date():
    today = datetime.now()
    dd = today.strftime('%d')
    mm = today.strftime('%m')
    yyyy = today.strftime('%Y')

    return f"{yyyy}-{mm}-{dd}"

@frappe.whitelist()
def checkQrAvailability(emp_id):
    # return '123/Dinner/1203'
    # return 'No Qr Present'
    currentdate = get_current_date()
    today = datetime.now(tz_NY)
    current_hour = today.hour
    current_minute = today.minute
    current_time_in_minutes = current_hour * 60 + current_minute

    if 8 * 60 + 20 <= current_time_in_minutes <= 10 * 60 + 30:
        meal = "Breakfast"
    elif 12 * 60 + 15 <= current_time_in_minutes <= 15 * 60 + 45:
        meal = "Lunch"
    elif 19 * 60 <= current_time_in_minutes <= 22 * 60 + 30:
        meal = "Dinner"
    else:
        meal = ""

    if current_time_in_minutes <= 10 * 60 + 30:
        food_type = "Breakfast"
    elif current_time_in_minutes <= 15 * 60 + 45:
        food_type = "Lunch"
    elif current_time_in_minutes <= 22 * 60 + 30:
        food_type = "Dinner"
    else :
        food_type = ""

    # return f"{meal}, {currentdate}, {emp_id}, ctm: {current_time_in_minutes}, cm: {current_minute}, ch: {current_hour}, t: {today}, date:{currentdate}"
    
    if meal != "":
        QR = frappe.get_all(
            'Food Request',
            filters={'emp_id': emp_id,'date': currentdate,'need': "Yes",'request_type': meal,'location': ('!=', '')},
            fields=['attend','request_type','location','emp_id','date']
        )
        if QR:
            record = QR[0]
            if record.get('attend') != 'Yes':
                return record.get('emp_id') +"/"+ record.get('request_type')+"/"+record.get('date')
            else:
                return "You have already scanned for "+record.get('request_type')

        else:
            return "You Haven't booked for "+food_type
    
    else:
        if(food_type == "Breakfast"):
            QR = frappe.get_all(
            'Food Request',
            filters={'emp_id': emp_id,'date': currentdate,'need': "Yes",'request_type': food_type,'location': ('!=', '')},
            fields=['attend','request_type','location','emp_id','date']
            )
            if QR:
                return 'For QR, please come back and check between 8.20am to 10:30am'
            else:
                return "You Haven't booked for "+food_type

        elif(food_type == "Lunch"):

            QR = frappe.get_all(
            'Food Request',
            filters={'emp_id': emp_id,'date': currentdate,'need': "Yes",'request_type': food_type,'location': ('!=', '')},
            fields=['attend','request_type','location','emp_id','date']
            )
            if QR:
                return 'For QR, please come back and check between 12.15pm to 3.45pm'
            else:
                return "You Haven't booked for "+food_type
           
        elif(food_type == "Dinner"):

            QR = frappe.get_all(
            'Food Request',
            filters={'emp_id': emp_id,'date': currentdate,'need': "Yes",'request_type': food_type,'location': ('!=', '')},
            fields=['attend','request_type','location','emp_id','date']
            )
            if QR:
                return 'For QR, please come back and check between 7.00pm to 10:30pm'
            else:
                return "You Haven't booked for "+food_type

        else:
            return "Sorry For the Inconvenience"
