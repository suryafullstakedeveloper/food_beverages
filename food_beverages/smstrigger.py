import frappe
from datetime import datetime,timedelta
import requests


def get_current_date():
    today = datetime.now()
    dd = today.strftime('%d')
    mm = today.strftime('%m')
    yyyy = today.strftime('%Y')

    return f"{yyyy}-{mm}-{dd}"


def get_tomorrow_date():
    today = datetime.now()
    tomorrow = today + timedelta(days=1)
    return tomorrow.strftime('%Y-%m-%d')


@frappe.whitelist()
def get_current_day():

    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    current_day_index = datetime.today().weekday()
    return days_of_week[current_day_index]


def get_day_of_week(date_string):
    date_object = datetime.strptime(date_string, "%Y-%m-%d")
    day_of_week = date_object.weekday()
    if day_of_week == 6:
        return 0
    return day_of_week + 1




@frappe.whitelist()
def get_prefrence_data(day , location , meal_type):

    day_values = {
        1: 'mon_f_type',
        2: 'tue_f_type',
        3: 'wed_f_type',
        4: 'thu_f_type',
        5: 'fri_f_type',
        6: 'sat_f_type',
        0: 'sun_f_type'
    }

    if int(day) in day_values:
        field_key = day_values[int(day)]
        sql_query = f"""
            SELECT {field_key} AS type
                FROM `tabFood Menu`
            WHERE location = '{location}' and meal_type = '{meal_type}'
        """
        existing_record = frappe.db.sql(sql_query, {'location': location , 'meal_type': meal_type}, as_dict=True)
        if existing_record:
            return existing_record[0].type
        else:
            return "Record Doesn't Exist!"
    else:
        return "Invalid day number"



# @frappe.whitelist()
# def send_sms():
    
#     text = 'Test'
#     mobile = '6382191018'

#     # Construct the URL for sending the SMS

#     try:
#         # Make a GET request to the external API using requests library
#         response = requests.get(url)
#         response.raise_for_status()  # Raise an error for unsuccessful responses

#         # frappe.msgprint(f"SMS sent successfully: {response.text}")

#     except requests.RequestException as e:
#         frappe.msgprint(f"Error sending SMS: {str(e)}", indicator='red')



@frappe.whitelist()
def iitm_breakfast_sms():
    
    date_variable = get_current_date()

    daynumber = get_day_of_week(date_variable)

    vegture = get_prefrence_data(daynumber,'IITM RP','Breakfast')

    if vegture == 'Veg':

        sql_query = """
            SELECT
                SUM(CASE WHEN request_type = 'Breakfast' AND location = 'IITM RP' AND date = %(date_variable)s  AND need = 'Yes' THEN 1 ELSE 0 END) AS RP_BF_count
            FROM
                `tabFood Request`
        """

        # Execute the query
        result_request = frappe.db.sql(sql_query, {'date_variable': date_variable}, as_dict=True)

        sql_query_manual_count  = """
            SELECT
                SUM(CASE WHEN location = 'IITM RP' THEN breakfast ELSE 0 END) AS RP_BF_count
                
            FROM
                `tabFood Manual Count`
            WHERE
                date = %(date_variable)s

        """

        # Execute the query
        result_manual_count = frappe.db.sql(sql_query_manual_count , {'date_variable': date_variable}, as_dict=True)

        if result_request and result_manual_count:
            merged_result = {
                "RP_BF_count": (result_request[0].RP_BF_count or 0) + (result_manual_count[0].RP_BF_count or 0),
            }
        
            text = str(int(merged_result['RP_BF_count']))
            text = text + '/Breakfast'
            mobile = '6382191018'
        

            # Construct the URL for sending the SMS
        

            try:
                # Make a GET request to the external API using requests library
                response = requests.get(url)
                response.raise_for_status()  # Raise an error for unsuccessful responses

                # frappe.msgprint(f"SMS sent successfully: {response.text}")

            except requests.RequestException as e:
                frappe.msgprint(f"Error sending SMS: {str(e)}", indicator='red')

    else:

        sql_query = """
            SELECT
                SUM(CASE WHEN request_type = 'Breakfast' AND location = 'IITM RP' AND date = %(date_variable)s  AND need = 'Yes' AND food_preference != 'Veg' THEN 1 ELSE 0 END) AS count
            FROM
                `tabFood Request`
        """

        result_request = frappe.db.sql(sql_query, {'date_variable': date_variable}, as_dict=True)

        sql_query_manual_count  = """
            SELECT
                SUM(CASE WHEN location = 'IITM RP' THEN breakfast_nveg ELSE 0 END) AS count
                
            FROM
                `tabFood Manual Count`
            WHERE
                date = %(date_variable)s

        """

        result_manual_count = frappe.db.sql(sql_query_manual_count , {'date_variable': date_variable}, as_dict=True)
        n_veg = '0'
        if result_request and result_manual_count:
            merged_result = {
                "count": (result_request[0].count or 0) + (result_manual_count[0].count or 0),
            }
        
            n_veg = str(int(merged_result['count']))

        sql_query2 = """
            SELECT
                SUM(CASE WHEN request_type = 'Breakfast' AND location = 'IITM RP' AND date = %(date_variable)s  AND need = 'Yes' AND food_preference = 'Veg' THEN 1 ELSE 0 END) AS count
            FROM
                `tabFood Request`
        """

        result_request2 = frappe.db.sql(sql_query2, {'date_variable': date_variable}, as_dict=True)

        sql_query_manual_count2  = """
            SELECT
                SUM(CASE WHEN location = 'IITM RP' THEN breakfast ELSE 0 END) AS count
                
            FROM
                `tabFood Manual Count`
            WHERE
                date = %(date_variable)s

        """

        result_manual_count2 = frappe.db.sql(sql_query_manual_count2 , {'date_variable': date_variable}, as_dict=True)
        veg = '0'
        if result_request2 and result_manual_count2:
            merged_result = {
                "count": (result_request2[0].count or 0) + (result_manual_count2[0].count or 0),
            }
        
            veg = str(int(merged_result['count']))


        mobile = '6382191018'

        food_count = veg + '/' + n_veg

        Mealtype = 'Breakfast'
        
    

        try:
            response = requests.get(url)
            response.raise_for_status()

        except requests.RequestException as e:
            frappe.msgprint(f"Error sending SMS: {str(e)}", indicator='red')



@frappe.whitelist()
def iitm_lunch_sms():

    date_variable = get_current_date()

    daynumber = get_day_of_week(date_variable)

    vegture = get_prefrence_data(daynumber,'IITM RP','Lunch')

    if vegture == 'Veg':

        sql_query = """
            SELECT
                SUM(CASE WHEN request_type = 'Lunch' AND location = 'IITM RP' AND date = %(date_variable)s  AND need = 'Yes' THEN 1 ELSE 0 END) AS count
            FROM
                `tabFood Request`
        """

        result_request = frappe.db.sql(sql_query, {'date_variable': date_variable}, as_dict=True)

        sql_query_manual_count  = """
            SELECT
                SUM(CASE WHEN location = 'IITM RP' THEN lunch ELSE 0 END) AS count
                
            FROM
                `tabFood Manual Count`
            WHERE
                date = %(date_variable)s

        """

        result_manual_count = frappe.db.sql(sql_query_manual_count , {'date_variable': date_variable}, as_dict=True)

        if result_request and result_manual_count:
            merged_result = {
                "count": (result_request[0].count or 0) + (result_manual_count[0].count or 0),
            }
        
            text = str(int(merged_result['count']))
            text = text + '/Lunch'

            mobile = '6382191018'
            
        

            try:
                response = requests.get(url)
                response.raise_for_status()

            except requests.RequestException as e:
                frappe.msgprint(f"Error sending SMS: {str(e)}", indicator='red')

    else:

        sql_query = """
            SELECT
                SUM(CASE WHEN request_type = 'Lunch' AND location = 'IITM RP' AND date = %(date_variable)s  AND need = 'Yes' AND food_preference != 'Veg' THEN 1 ELSE 0 END) AS count
            FROM
                `tabFood Request`
        """

        result_request = frappe.db.sql(sql_query, {'date_variable': date_variable}, as_dict=True)

        sql_query_manual_count  = """
            SELECT
                SUM(CASE WHEN location = 'IITM RP' THEN lunch_nveg ELSE 0 END) AS count
                
            FROM
                `tabFood Manual Count`
            WHERE
                date = %(date_variable)s

        """

        result_manual_count = frappe.db.sql(sql_query_manual_count , {'date_variable': date_variable}, as_dict=True)
        n_veg = '0'
        if result_request and result_manual_count:
            merged_result = {
                "count": (result_request[0].count or 0) + (result_manual_count[0].count or 0),
            }
        
            n_veg = str(int(merged_result['count']))

        sql_query2 = """
            SELECT
                SUM(CASE WHEN request_type = 'Lunch' AND location = 'IITM RP' AND date = %(date_variable)s  AND need = 'Yes' AND food_preference = 'Veg' THEN 1 ELSE 0 END) AS count
            FROM
                `tabFood Request`
        """

        result_request2 = frappe.db.sql(sql_query2, {'date_variable': date_variable}, as_dict=True)

        sql_query_manual_count2  = """
            SELECT
                SUM(CASE WHEN location = 'IITM RP' THEN lunch ELSE 0 END) AS count
                
            FROM
                `tabFood Manual Count`
            WHERE
                date = %(date_variable)s

        """

        result_manual_count2 = frappe.db.sql(sql_query_manual_count2 , {'date_variable': date_variable}, as_dict=True)
        veg = '0'
        if result_request2 and result_manual_count2:
            merged_result = {
                "count": (result_request2[0].count or 0) + (result_manual_count2[0].count or 0),
            }
        
            veg = str(int(merged_result['count']))


        mobile = '6382191018'

        food_count = veg + '/' + n_veg

        lunch = 'Lunch'
        
    

        try:
            response = requests.get(url)
            response.raise_for_status()

        except requests.RequestException as e:
            frappe.msgprint(f"Error sending SMS: {str(e)}", indicator='red')








@frappe.whitelist()
def iitm_dinner_sms():
    
    date_variable = get_current_date()

    daynumber = get_day_of_week(date_variable)

    vegture = get_prefrence_data(daynumber,'IITM RP','Dinner')

    if vegture == 'Veg':

        sql_query = """
            SELECT
                SUM(CASE WHEN request_type = 'Dinner' AND location = 'IITM RP' AND date = %(date_variable)s  AND need = 'Yes' THEN 1 ELSE 0 END) AS count
            FROM
                `tabFood Request`
        """

        result_request = frappe.db.sql(sql_query, {'date_variable': date_variable}, as_dict=True)

        sql_query_manual_count  = """
            SELECT
                SUM(CASE WHEN location = 'IITM RP' THEN dinner ELSE 0 END) AS count
                
            FROM
                `tabFood Manual Count`
            WHERE
                date = %(date_variable)s

        """

        result_manual_count = frappe.db.sql(sql_query_manual_count , {'date_variable': date_variable}, as_dict=True)

        if result_request and result_manual_count:
            merged_result = {
                "count": (result_request[0].count or 0) + (result_manual_count[0].count or 0),
            }
        
            text = str(int(merged_result['count']))
            text = text + '/Dinner'

            mobile = '6382191018'
            
        

            try:
                response = requests.get(url)
                response.raise_for_status()

            except requests.RequestException as e:
                frappe.msgprint(f"Error sending SMS: {str(e)}", indicator='red')

    else:

        sql_query = """
            SELECT
                SUM(CASE WHEN request_type = 'Dinner' AND location = 'IITM RP' AND date = %(date_variable)s  AND need = 'Yes' AND food_preference != 'Veg' THEN 1 ELSE 0 END) AS count
            FROM
                `tabFood Request`
        """

        result_request = frappe.db.sql(sql_query, {'date_variable': date_variable}, as_dict=True)

        sql_query_manual_count  = """
            SELECT
                SUM(CASE WHEN location = 'IITM RP' THEN dinner_nveg ELSE 0 END) AS count
                
            FROM
                `tabFood Manual Count`
            WHERE
                date = %(date_variable)s

        """

        result_manual_count = frappe.db.sql(sql_query_manual_count , {'date_variable': date_variable}, as_dict=True)
        n_veg = '0'
        if result_request and result_manual_count:
            merged_result = {
                "count": (result_request[0].count or 0) + (result_manual_count[0].count or 0),
            }
        
            n_veg = str(int(merged_result['count']))

        sql_query2 = """
            SELECT
                SUM(CASE WHEN request_type = 'Dinner' AND location = 'IITM RP' AND date = %(date_variable)s  AND need = 'Yes' AND food_preference = 'Veg' THEN 1 ELSE 0 END) AS count
            FROM
                `tabFood Request`
        """

        result_request2 = frappe.db.sql(sql_query2, {'date_variable': date_variable}, as_dict=True)

        sql_query_manual_count2  = """
            SELECT
                SUM(CASE WHEN location = 'IITM RP' THEN dinner ELSE 0 END) AS count
                
            FROM
                `tabFood Manual Count`
            WHERE
                date = %(date_variable)s

        """

        result_manual_count2 = frappe.db.sql(sql_query_manual_count2 , {'date_variable': date_variable}, as_dict=True)
        veg = '0'
        if result_request2 and result_manual_count2:
            merged_result = {
                "count": (result_request2[0].count or 0) + (result_manual_count2[0].count or 0),
            }
        
            veg = str(int(merged_result['count']))


        mobile = '6382191018'

        food_count = veg + '/' + n_veg

        lunch = 'Dinner'
        
    

        try:
            response = requests.get(url)
            response.raise_for_status()

        except requests.RequestException as e:
            frappe.msgprint(f"Error sending SMS: {str(e)}", indicator='red')








@frappe.whitelist()
def thaiyur_breakfast_sms():
    
    date_variable = get_current_date()

    daynumber = get_day_of_week(date_variable)

    vegture = get_prefrence_data(daynumber,'Thaiyur','Breakfast')

    if vegture == 'Veg':

        sql_query = """
            SELECT
                SUM(CASE WHEN request_type = 'Breakfast' AND location = 'Thaiyur' AND date = %(date_variable)s  AND need = 'Yes' THEN 1 ELSE 0 END) AS RP_BF_count
            FROM
                `tabFood Request`
        """

        # Execute the query
        result_request = frappe.db.sql(sql_query, {'date_variable': date_variable}, as_dict=True)

        sql_query_manual_count  = """
            SELECT
                SUM(CASE WHEN location = 'Thaiyur' THEN breakfast ELSE 0 END) AS RP_BF_count
                
            FROM
                `tabFood Manual Count`
            WHERE
                date = %(date_variable)s

        """

        # Execute the query
        result_manual_count = frappe.db.sql(sql_query_manual_count , {'date_variable': date_variable}, as_dict=True)

        if result_request and result_manual_count:
            merged_result = {
                "RP_BF_count": (result_request[0].RP_BF_count or 0) + (result_manual_count[0].RP_BF_count or 0),
            }
        
            text = str(int(merged_result['RP_BF_count']))
            # text = str(merged_result['count'])
            text = text + '/Breakfast'

            mobile = '6382191018'
        

            # Construct the URL for sending the SMS
        

            try:
                # Make a GET request to the external API using requests library
                response = requests.get(url)
                response.raise_for_status()  # Raise an error for unsuccessful responses

                # frappe.msgprint(f"SMS sent successfully: {response.text}")

            except requests.RequestException as e:
                frappe.msgprint(f"Error sending SMS: {str(e)}", indicator='red')


    else:

        sql_query = """
            SELECT
                SUM(CASE WHEN request_type = 'Breakfast' AND location = 'Thaiyur' AND date = %(date_variable)s  AND need = 'Yes' AND food_preference != 'Veg' THEN 1 ELSE 0 END) AS count
            FROM
                `tabFood Request`
        """

        result_request = frappe.db.sql(sql_query, {'date_variable': date_variable}, as_dict=True)

        sql_query_manual_count  = """
            SELECT
                SUM(CASE WHEN location = 'Thaiyur' THEN breakfast_nveg ELSE 0 END) AS count
                
            FROM
                `tabFood Manual Count`
            WHERE
                date = %(date_variable)s

        """

        result_manual_count = frappe.db.sql(sql_query_manual_count , {'date_variable': date_variable}, as_dict=True)
        n_veg = '0'
        if result_request and result_manual_count:
            merged_result = {
                "count": (result_request[0].count or 0) + (result_manual_count[0].count or 0),
            }
        
            n_veg = str(int(merged_result['count']))

        sql_query2 = """
            SELECT
                SUM(CASE WHEN request_type = 'Breakfast' AND location = 'Thaiyur' AND date = %(date_variable)s  AND need = 'Yes' AND food_preference = 'Veg' THEN 1 ELSE 0 END) AS count
            FROM
                `tabFood Request`
        """

        result_request2 = frappe.db.sql(sql_query2, {'date_variable': date_variable}, as_dict=True)

        sql_query_manual_count2  = """
            SELECT
                SUM(CASE WHEN location = 'Thaiyur' THEN breakfast ELSE 0 END) AS count
                
            FROM
                `tabFood Manual Count`
            WHERE
                date = %(date_variable)s

        """

        result_manual_count2 = frappe.db.sql(sql_query_manual_count2 , {'date_variable': date_variable}, as_dict=True)
        veg = '0'
        if result_request2 and result_manual_count2:
            merged_result = {
                "count": (result_request2[0].count or 0) + (result_manual_count2[0].count or 0),
            }
        
            veg = str(int(merged_result['count']))


        mobile = '6382191018'

        food_count = veg + '/' + n_veg

        Mealtype = 'Breakfast'
        
    

        try:
            response = requests.get(url)
            response.raise_for_status()

        except requests.RequestException as e:
            frappe.msgprint(f"Error sending SMS: {str(e)}", indicator='red')




@frappe.whitelist()
def thaiyur_lunch_sms():

    date_variable = get_current_date()

    daynumber = get_day_of_week(date_variable)

    vegture = get_prefrence_data(daynumber,'Thaiyur','Lunch')

    if vegture == 'Veg':

        sql_query = """
            SELECT
                SUM(CASE WHEN request_type = 'Lunch' AND location = 'Thaiyur' AND date = %(date_variable)s  AND need = 'Yes' THEN 1 ELSE 0 END) AS count
            FROM
                `tabFood Request`
        """

        result_request = frappe.db.sql(sql_query, {'date_variable': date_variable}, as_dict=True)

        sql_query_manual_count  = """
            SELECT
                SUM(CASE WHEN location = 'Thaiyur' THEN lunch ELSE 0 END) AS count
                
            FROM
                `tabFood Manual Count`
            WHERE
                date = %(date_variable)s

        """

        result_manual_count = frappe.db.sql(sql_query_manual_count , {'date_variable': date_variable}, as_dict=True)

        if result_request and result_manual_count:
            merged_result = {
                "count": (result_request[0].count or 0) + (result_manual_count[0].count or 0),
            }
        
            text = str(int(merged_result['count']))
            text = text + '/Lunch'

            mobile = '6382191018'
            
        

            try:
                response = requests.get(url)
                response.raise_for_status()

            except requests.RequestException as e:
                frappe.msgprint(f"Error sending SMS: {str(e)}", indicator='red')

    else:
        date_variable = get_current_date()

        sql_query = """
            SELECT
                SUM(CASE WHEN request_type = 'Lunch' AND location = 'Thaiyur' AND date = %(date_variable)s  AND need = 'Yes' AND food_preference != 'Veg' THEN 1 ELSE 0 END) AS count
            FROM
                `tabFood Request`
        """

        result_request = frappe.db.sql(sql_query, {'date_variable': date_variable}, as_dict=True)

        sql_query_manual_count  = """
            SELECT
                SUM(CASE WHEN location = 'Thaiyur' THEN lunch_nveg ELSE 0 END) AS count
                
            FROM
                `tabFood Manual Count`
            WHERE
                date = %(date_variable)s

        """

        result_manual_count = frappe.db.sql(sql_query_manual_count , {'date_variable': date_variable}, as_dict=True)
        n_veg = '0'
        if result_request and result_manual_count:
            merged_result = {
                "count": (result_request[0].count or 0) + (result_manual_count[0].count or 0),
            }
        
            n_veg = str(int(merged_result['count']))

        sql_query2 = """
            SELECT
                SUM(CASE WHEN request_type = 'Lunch' AND location = 'Thaiyur' AND date = %(date_variable)s  AND need = 'Yes' AND food_preference = 'Veg' THEN 1 ELSE 0 END) AS count
            FROM
                `tabFood Request`
        """

        result_request2 = frappe.db.sql(sql_query2, {'date_variable': date_variable}, as_dict=True)

        sql_query_manual_count2  = """
            SELECT
                SUM(CASE WHEN location = 'Thaiyur' THEN lunch ELSE 0 END) AS count
                
            FROM
                `tabFood Manual Count`
            WHERE
                date = %(date_variable)s

        """

        result_manual_count2 = frappe.db.sql(sql_query_manual_count2 , {'date_variable': date_variable}, as_dict=True)
        veg = '0'
        if result_request2 and result_manual_count2:
            merged_result = {
                "count": (result_request2[0].count or 0) + (result_manual_count2[0].count or 0),
            }
        
            veg = str(int(merged_result['count']))


        mobile = '6382191018'

        food_count = veg + '/' + n_veg

        lunch = 'Lunch'
        
    

        try:
            response = requests.get(url)
            response.raise_for_status()

        except requests.RequestException as e:
            frappe.msgprint(f"Error sending SMS: {str(e)}", indicator='red')





@frappe.whitelist()
def thaiyur_dinner_sms():
    
    date_variable = get_current_date()

    daynumber = get_day_of_week(date_variable)

    vegture = get_prefrence_data(daynumber,'Thaiyur','Dinner')

    if vegture == 'Veg':

        sql_query = """
            SELECT
                SUM(CASE WHEN request_type = 'Dinner' AND location = 'Thaiyur' AND date = %(date_variable)s  AND need = 'Yes' THEN 1 ELSE 0 END) AS count
            FROM
                `tabFood Request`
        """

        result_request = frappe.db.sql(sql_query, {'date_variable': date_variable}, as_dict=True)

        sql_query_manual_count  = """
            SELECT
                SUM(CASE WHEN location = 'Thaiyur' THEN dinner ELSE 0 END) AS count
                
            FROM
                `tabFood Manual Count`
            WHERE
                date = %(date_variable)s

        """

        result_manual_count = frappe.db.sql(sql_query_manual_count , {'date_variable': date_variable}, as_dict=True)

        if result_request and result_manual_count:
            merged_result = {
                "count": (result_request[0].count or 0) + (result_manual_count[0].count or 0),
            }
        
            text = str(int(merged_result['count']))
            # text = str(merged_result['count'])
            text = text + '/Dinner'

            mobile = '6382191018'
            
        

            try:
                response = requests.get(url)
                response.raise_for_status()

            except requests.RequestException as e:
                frappe.msgprint(f"Error sending SMS: {str(e)}", indicator='red')

    else:

        sql_query = """
            SELECT
                SUM(CASE WHEN request_type = 'Dinner' AND location = 'Thaiyur' AND date = %(date_variable)s  AND need = 'Yes' AND food_preference != 'Veg' THEN 1 ELSE 0 END) AS count
            FROM
                `tabFood Request`
        """

        result_request = frappe.db.sql(sql_query, {'date_variable': date_variable}, as_dict=True)

        sql_query_manual_count  = """
            SELECT
                SUM(CASE WHEN location = 'Thaiyur' THEN dinner_nveg ELSE 0 END) AS count
                
            FROM
                `tabFood Manual Count`
            WHERE
                date = %(date_variable)s

        """

        result_manual_count = frappe.db.sql(sql_query_manual_count , {'date_variable': date_variable}, as_dict=True)
        n_veg = '0'
        if result_request and result_manual_count:
            merged_result = {
                "count": (result_request[0].count or 0) + (result_manual_count[0].count or 0),
            }
        
            n_veg = str(int(merged_result['count']))

        sql_query2 = """
            SELECT
                SUM(CASE WHEN request_type = 'Dinner' AND location = 'Thaiyur' AND date = %(date_variable)s  AND need = 'Yes' AND food_preference = 'Veg' THEN 1 ELSE 0 END) AS count
            FROM
                `tabFood Request`
        """

        result_request2 = frappe.db.sql(sql_query2, {'date_variable': date_variable}, as_dict=True)

        sql_query_manual_count2  = """
            SELECT
                SUM(CASE WHEN location = 'Thaiyur' THEN dinner ELSE 0 END) AS count
                
            FROM
                `tabFood Manual Count`
            WHERE
                date = %(date_variable)s

        """

        result_manual_count2 = frappe.db.sql(sql_query_manual_count2 , {'date_variable': date_variable}, as_dict=True)
        veg = '0'
        if result_request2 and result_manual_count2:
            merged_result = {
                "count": (result_request2[0].count or 0) + (result_manual_count2[0].count or 0),
            }
        
            veg = str(int(merged_result['count']))


        mobile = '6382191018'

        food_count = veg + '/' + n_veg

        lunch = 'Dinner'
        
    

        try:
            response = requests.get(url)
            response.raise_for_status()

        except requests.RequestException as e:
            frappe.msgprint(f"Error sending SMS: {str(e)}", indicator='red')






@frappe.whitelist()
def shar_breakfast_sms():
    
    date_variable = get_tomorrow_date()

    daynumber = get_day_of_week(date_variable)

    vegture = get_prefrence_data(daynumber,'Shar','Breakfast')

    if vegture == 'Veg':

        sql_query = """
            SELECT
                SUM(CASE WHEN request_type = 'Breakfast' AND location = 'Shar' AND date = %(date_variable)s  AND need = 'Yes' THEN 1 ELSE 0 END) AS RP_BF_count
            FROM
                `tabFood Request`
        """

        # Execute the query
        result_request = frappe.db.sql(sql_query, {'date_variable': date_variable}, as_dict=True)

        sql_query_manual_count  = """
            SELECT
                SUM(CASE WHEN location = 'Shar' THEN breakfast ELSE 0 END) AS RP_BF_count
                
            FROM
                `tabFood Manual Count`
            WHERE
                date = %(date_variable)s

        """

        # Execute the query
        result_manual_count = frappe.db.sql(sql_query_manual_count , {'date_variable': date_variable}, as_dict=True)

        if result_request and result_manual_count:
            merged_result = {
                "RP_BF_count": (result_request[0].RP_BF_count or 0) + (result_manual_count[0].RP_BF_count or 0),
            }
        
            text = str(int(merged_result['RP_BF_count']))
            # text = str(merged_result['count'])
            text = text + '/Breakfast'

            mobile = '6382191018'
        

            # Construct the URL for sending the SMS
        

            try:
                # Make a GET request to the external API using requests library
                response = requests.get(url)
                response.raise_for_status()  # Raise an error for unsuccessful responses

                # frappe.msgprint(f"SMS sent successfully: {response.text}")

            except requests.RequestException as e:
                frappe.msgprint(f"Error sending SMS: {str(e)}", indicator='red')


    else:

        sql_query = """
            SELECT
                SUM(CASE WHEN request_type = 'Breakfast' AND location = 'Shar' AND date = %(date_variable)s  AND need = 'Yes' AND food_preference != 'Veg' THEN 1 ELSE 0 END) AS count
            FROM
                `tabFood Request`
        """

        result_request = frappe.db.sql(sql_query, {'date_variable': date_variable}, as_dict=True)

        sql_query_manual_count  = """
            SELECT
                SUM(CASE WHEN location = 'Shar' THEN breakfast_nveg ELSE 0 END) AS count
                
            FROM
                `tabFood Manual Count`
            WHERE
                date = %(date_variable)s

        """

        result_manual_count = frappe.db.sql(sql_query_manual_count , {'date_variable': date_variable}, as_dict=True)
        n_veg = '0'
        if result_request and result_manual_count:
            merged_result = {
                "count": (result_request[0].count or 0) + (result_manual_count[0].count or 0),
            }
        
            n_veg = str(int(merged_result['count']))

        sql_query2 = """
            SELECT
                SUM(CASE WHEN request_type = 'Breakfast' AND location = 'Shar' AND date = %(date_variable)s  AND need = 'Yes' AND food_preference = 'Veg' THEN 1 ELSE 0 END) AS count
            FROM
                `tabFood Request`
        """

        result_request2 = frappe.db.sql(sql_query2, {'date_variable': date_variable}, as_dict=True)

        sql_query_manual_count2  = """
            SELECT
                SUM(CASE WHEN location = 'Shar' THEN breakfast ELSE 0 END) AS count
                
            FROM
                `tabFood Manual Count`
            WHERE
                date = %(date_variable)s

        """

        result_manual_count2 = frappe.db.sql(sql_query_manual_count2 , {'date_variable': date_variable}, as_dict=True)
        veg = '0'
        if result_request2 and result_manual_count2:
            merged_result = {
                "count": (result_request2[0].count or 0) + (result_manual_count2[0].count or 0),
            }
        
            veg = str(int(merged_result['count']))


        mobile = '6382191018'

        food_count = veg + '/' + n_veg

        Mealtype = 'Breakfast'
        
    

        try:
            response = requests.get(url)
            response.raise_for_status()

        except requests.RequestException as e:
            frappe.msgprint(f"Error sending SMS: {str(e)}", indicator='red')





@frappe.whitelist()
def shar_lunch_sms():


    date_variable = get_tomorrow_date()

    daynumber = get_day_of_week(date_variable)

    vegture = get_prefrence_data(daynumber,'Shar','Lunch')

    if vegture == 'Veg':

        sql_query = """
            SELECT
                SUM(CASE WHEN request_type = 'Lunch' AND location = 'Shar' AND date = %(date_variable)s  AND need = 'Yes' THEN 1 ELSE 0 END) AS count
            FROM
                `tabFood Request`
        """

        result_request = frappe.db.sql(sql_query, {'date_variable': date_variable}, as_dict=True)

        sql_query_manual_count  = """
            SELECT
                SUM(CASE WHEN location = 'Shar' THEN lunch ELSE 0 END) AS count
                
            FROM
                `tabFood Manual Count`
            WHERE
                date = %(date_variable)s

        """

        result_manual_count = frappe.db.sql(sql_query_manual_count , {'date_variable': date_variable}, as_dict=True)

        if result_request and result_manual_count:
            merged_result = {
                "count": (result_request[0].count or 0) + (result_manual_count[0].count or 0),
            }
        
            text = str(int(merged_result['count']))
            text = text + '/Lunch'

            mobile = '6382191018'
            
        

            try:
                response = requests.get(url)
                response.raise_for_status()

            except requests.RequestException as e:
                frappe.msgprint(f"Error sending SMS: {str(e)}", indicator='red')

    else:

        sql_query = """
            SELECT
                SUM(CASE WHEN request_type = 'Lunch' AND location = 'Shar' AND date = %(date_variable)s  AND need = 'Yes' AND food_preference != 'Veg' THEN 1 ELSE 0 END) AS count
            FROM
                `tabFood Request`
        """

        result_request = frappe.db.sql(sql_query, {'date_variable': date_variable}, as_dict=True)

        sql_query_manual_count  = """
            SELECT
                SUM(CASE WHEN location = 'Shar' THEN lunch_nveg ELSE 0 END) AS count
                
            FROM
                `tabFood Manual Count`
            WHERE
                date = %(date_variable)s

        """

        result_manual_count = frappe.db.sql(sql_query_manual_count , {'date_variable': date_variable}, as_dict=True)
        n_veg = '0'
        if result_request and result_manual_count:
            merged_result = {
                "count": (result_request[0].count or 0) + (result_manual_count[0].count or 0),
            }
        
            n_veg = str(int(merged_result['count']))

        sql_query2 = """
            SELECT
                SUM(CASE WHEN request_type = 'Lunch' AND location = 'Shar' AND date = %(date_variable)s  AND need = 'Yes' AND food_preference = 'Veg' THEN 1 ELSE 0 END) AS count
            FROM
                `tabFood Request`
        """

        result_request2 = frappe.db.sql(sql_query2, {'date_variable': date_variable}, as_dict=True)

        sql_query_manual_count2  = """
            SELECT
                SUM(CASE WHEN location = 'Shar' THEN lunch ELSE 0 END) AS count
                
            FROM
                `tabFood Manual Count`
            WHERE
                date = %(date_variable)s

        """

        result_manual_count2 = frappe.db.sql(sql_query_manual_count2 , {'date_variable': date_variable}, as_dict=True)
        veg = '0'
        if result_request2 and result_manual_count2:
            merged_result = {
                "count": (result_request2[0].count or 0) + (result_manual_count2[0].count or 0),
            }
        
            veg = str(int(merged_result['count']))


        mobile = '6382191018'

        food_count = veg + '/' + n_veg

        lunch = 'Lunch'
        
    

        try:
            response = requests.get(url)
            response.raise_for_status()

        except requests.RequestException as e:
            frappe.msgprint(f"Error sending SMS: {str(e)}", indicator='red')





@frappe.whitelist()
def shar_dinner_sms():
    
    date_variable = get_tomorrow_date()

    daynumber = get_day_of_week(date_variable)

    vegture = get_prefrence_data(daynumber,'Shar','Dinner')

    if vegture == 'Veg':

        sql_query = """
            SELECT
                SUM(CASE WHEN request_type = 'Dinner' AND location = 'Shar' AND date = %(date_variable)s  AND need = 'Yes' THEN 1 ELSE 0 END) AS count
            FROM
                `tabFood Request`
        """

        result_request = frappe.db.sql(sql_query, {'date_variable': date_variable}, as_dict=True)

        sql_query_manual_count  = """
            SELECT
                SUM(CASE WHEN location = 'Shar' THEN dinner ELSE 0 END) AS count
                
            FROM
                `tabFood Manual Count`
            WHERE
                date = %(date_variable)s

        """

        result_manual_count = frappe.db.sql(sql_query_manual_count , {'date_variable': date_variable}, as_dict=True)

        if result_request and result_manual_count:
            merged_result = {
                "count": (result_request[0].count or 0) + (result_manual_count[0].count or 0),
            }
        
            text = str(int(merged_result['count']))
            text = text + '/Dinner'

            mobile = '6382191018'
            
        

            try:
                response = requests.get(url)
                response.raise_for_status()

            except requests.RequestException as e:
                frappe.msgprint(f"Error sending SMS: {str(e)}", indicator='red')


    else:

        sql_query = """
            SELECT
                SUM(CASE WHEN request_type = 'Dinner' AND location = 'Shar' AND date = %(date_variable)s  AND need = 'Yes' AND food_preference != 'Veg' THEN 1 ELSE 0 END) AS count
            FROM
                `tabFood Request`
        """

        result_request = frappe.db.sql(sql_query, {'date_variable': date_variable}, as_dict=True)

        sql_query_manual_count  = """
            SELECT
                SUM(CASE WHEN location = 'Shar' THEN dinner_nveg ELSE 0 END) AS count
                
            FROM
                `tabFood Manual Count`
            WHERE
                date = %(date_variable)s

        """

        result_manual_count = frappe.db.sql(sql_query_manual_count , {'date_variable': date_variable}, as_dict=True)
        n_veg = '0'
        if result_request and result_manual_count:
            merged_result = {
                "count": (result_request[0].count or 0) + (result_manual_count[0].count or 0),
            }
        
            n_veg = str(int(merged_result['count']))

        sql_query2 = """
            SELECT
                SUM(CASE WHEN request_type = 'Dinner' AND location = 'Shar' AND date = %(date_variable)s  AND need = 'Yes' AND food_preference = 'Veg' THEN 1 ELSE 0 END) AS count
            FROM
                `tabFood Request`
        """

        result_request2 = frappe.db.sql(sql_query2, {'date_variable': date_variable}, as_dict=True)

        sql_query_manual_count2  = """
            SELECT
                SUM(CASE WHEN location = 'Shar' THEN dinner ELSE 0 END) AS count
                
            FROM
                `tabFood Manual Count`
            WHERE
                date = %(date_variable)s

        """

        result_manual_count2 = frappe.db.sql(sql_query_manual_count2 , {'date_variable': date_variable}, as_dict=True)
        veg = '0'
        if result_request2 and result_manual_count2:
            merged_result = {
                "count": (result_request2[0].count or 0) + (result_manual_count2[0].count or 0),
            }
        
            veg = str(int(merged_result['count']))


        mobile = '6382191018'

        food_count = veg + '/' + n_veg

        lunch = 'Dinner'
        
    

        try:
            response = requests.get(url)
            response.raise_for_status()

        except requests.RequestException as e:
            frappe.msgprint(f"Error sending SMS: {str(e)}", indicator='red')



# @frappe.whitelist()
# def template_check():
    
#     text = '56'

#     text = text + ' for dinner'
#     mobile = '8667872175,6382191018,8903581771'

#     # Construct the URL for sending the SMS
    

#     try:
#         # Make a GET request to the external API using requests library
#         response = requests.get(url)
#         response.raise_for_status()  # Raise an error for unsuccessful responses

#         # frappe.msgprint(f"SMS sent successfully: {response.text}")

#     except requests.RequestException as e:
#         frappe.msgprint(f"Error sending SMS: {str(e)}", indicator='red')





# @frappe.whitelist()
# def template_check():
    
#     text = '56/67'

#     text1 = 'Dinner'
#     mobile = '8667872175'
    

#     try:
#         response = requests.get(url)
#         response.raise_for_status() 

#     except requests.RequestException as e:
#         frappe.msgprint(f"Error sending SMS: {str(e)}", indicator='red')

        
