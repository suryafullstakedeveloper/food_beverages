import frappe
from datetime import datetime,time ,timedelta
from frappe import db
import calendar


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


def get_month_range(input_date):
    # Convert input date string to a datetime object
    input_date = datetime.strptime(input_date, '%Y-%m-%d')

    # Get the first day of the month
    start_date = input_date.replace(day=1)

    # Calculate the last day of the month
    _, last_day = calendar.monthrange(start_date.year, start_date.month)
    end_date = start_date.replace(day=last_day)

    # Format the dates as strings
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')

    # Return the result as a dictionary
    return {'start_date': start_date_str, 'end_date': end_date_str}


@frappe.whitelist()
def Food_details_Month(startDate):

    dateperiod = get_month_range(startDate)

    start = dateperiod['start_date']
    end = dateperiod['end_date']

    sql_query = """
        SELECT
            SUM(CASE WHEN request_type = 'Breakfast' AND location = 'IITM RP' AND date >= %(start)s AND date <= %(end)s AND need = 'Yes' THEN 1 ELSE 0 END) AS RP_BF_count,
            SUM(CASE WHEN request_type = 'Lunch' AND location = 'IITM RP' AND date >= %(start)s AND date <= %(end)s AND need = 'Yes' THEN 1 ELSE 0 END) AS RP_Lunch_count,
            SUM(CASE WHEN request_type = 'Dinner' AND location = 'IITM RP' AND date >= %(start)s AND date <= %(end)s AND need = 'Yes' THEN 1 ELSE 0 END) AS RP_Dinner_count,
            
            SUM(CASE WHEN request_type = 'Breakfast' AND location = 'Thaiyur' AND date >= %(start)s AND date <= %(end)s AND need = 'Yes' THEN 1 ELSE 0 END) AS Thaiyur_BF_count,
            SUM(CASE WHEN request_type = 'Lunch' AND location = 'Thaiyur' AND date >= %(start)s AND date <= %(end)s AND need = 'Yes' THEN 1 ELSE 0 END) AS Thaiyur_Lunch_count,
            SUM(CASE WHEN request_type = 'Dinner' AND location = 'Thaiyur' AND date >= %(start)s AND date <= %(end)s AND need = 'Yes' THEN 1 ELSE 0 END) AS Thaiyur_Dinner_count,

            SUM(CASE WHEN request_type = 'Breakfast' AND location = 'Shar' AND date >= %(start)s AND date <= %(end)s AND need = 'Yes' THEN 1 ELSE 0 END) AS Shar_BF_count,
            SUM(CASE WHEN request_type = 'Lunch' AND location = 'Shar' AND date >= %(start)s AND date <= %(end)s AND need = 'Yes' THEN 1 ELSE 0 END) AS Shar_Lunch_count,
            SUM(CASE WHEN request_type = 'Dinner' AND location = 'Shar' AND date >= %(start)s AND date <= %(end)s AND need = 'Yes' THEN 1 ELSE 0 END) AS Shar_Dinner_count,

            SUM(CASE WHEN request_type = 'Refreshments' AND location = 'IITM RP' AND date >= %(start)s AND date <= %(end)s AND need = 'Yes' THEN 1 ELSE 0 END) AS RP_Ref_count,
            SUM(CASE WHEN request_type = 'Refreshments' AND location = 'Thaiyur' AND date >= %(start)s AND date <= %(end)s AND need = 'Yes' THEN 1 ELSE 0 END) AS Thaiyur_Ref_count,
            SUM(CASE WHEN request_type = 'Refreshments' AND location = 'Shar' AND date >= %(start)s AND date <= %(end)s AND need = 'Yes' THEN 1 ELSE 0 END) AS Shar_Ref_count
            -- Add similar lines for other counts
        FROM
            `tabFood Request`
    """

    result_request = frappe.db.sql(sql_query, {'start': start, 'end': end}, as_dict=True)

    sql_query_manual_count  = """
        SELECT
            SUM(CASE WHEN location = 'IITM RP' THEN COALESCE(breakfast_nveg, 0) + COALESCE(breakfast, 0) ELSE 0 END) AS RP_BF_count,
            SUM(CASE WHEN location = 'IITM RP' THEN COALESCE(lunch_nveg, 0) + COALESCE(lunch, 0) ELSE 0 END) AS RP_Lunch_count,
            SUM(CASE WHEN location = 'IITM RP' THEN COALESCE(dinner_nveg, 0) + COALESCE(dinner, 0) ELSE 0 END) AS RP_Dinner_count,

            SUM(CASE WHEN location = 'Thaiyur' THEN COALESCE(breakfast_nveg, 0) + COALESCE(breakfast, 0) ELSE 0 END) AS Thaiyur_BF_count,
            SUM(CASE WHEN location = 'Thaiyur' THEN COALESCE(lunch_nveg, 0) + COALESCE(lunch, 0) ELSE 0 END) AS Thaiyur_Lunch_count,
            SUM(CASE WHEN location = 'Thaiyur' THEN COALESCE(dinner_nveg, 0) + COALESCE(dinner, 0) ELSE 0 END) AS Thaiyur_Dinner_count,

            SUM(CASE WHEN location = 'Shar' THEN COALESCE(breakfast_nveg, 0) + COALESCE(breakfast, 0) ELSE 0 END) AS Shar_BF_count,
            SUM(CASE WHEN location = 'Shar' THEN COALESCE(lunch_nveg, 0) + COALESCE(lunch, 0) ELSE 0 END) AS Shar_Lunch_count,
            SUM(CASE WHEN location = 'Shar' THEN COALESCE(dinner_nveg, 0) + COALESCE(dinner, 0) ELSE 0 END) AS Shar_Dinner_count
        FROM
            `tabFood Manual Count`
        WHERE 
            date >= %(start)s AND date < %(end)s;
    """
    
    result_manual_count = frappe.db.sql(sql_query_manual_count , {'start': start , 'end': end}, as_dict=True)


    if result_request and result_manual_count:
        merged_result = {
            "RP_BF_count": (result_request[0].RP_BF_count or 0) + (result_manual_count[0].RP_BF_count or 0),
            "RP_Lunch_count": (result_request[0].RP_Lunch_count or 0) + (result_manual_count[0].RP_Lunch_count or 0),
            "RP_Dinner_count": (result_request[0].RP_Dinner_count or 0) + (result_manual_count[0].RP_Dinner_count or 0),
            "Thaiyur_BF_count": (result_request[0].Thaiyur_BF_count or 0) + (result_manual_count[0].Thaiyur_BF_count or 0),
            "Thaiyur_Lunch_count": (result_request[0].Thaiyur_Lunch_count or 0) + (result_manual_count[0].Thaiyur_Lunch_count or 0),
            "Thaiyur_Dinner_count": (result_request[0].Thaiyur_Dinner_count or 0) + (result_manual_count[0].Thaiyur_Dinner_count or 0),
            "Shar_BF_count": (result_request[0].Shar_BF_count or 0) + (result_manual_count[0].Shar_BF_count or 0),
            "Shar_Lunch_count": (result_request[0].Shar_Lunch_count or 0) + (result_manual_count[0].Shar_Lunch_count or 0),
            "Shar_Dinner_count": (result_request[0].Shar_Dinner_count or 0) + (result_manual_count[0].Shar_Dinner_count or 0),
            "RP_Ref_count": result_request[0].RP_Ref_count,
            "Thaiyur_Ref_count": result_request[0].Thaiyur_Ref_count,
            "Shar_Ref_count": result_request[0].Shar_Ref_count,
        }
        return merged_result





@frappe.whitelist()
def Food_details_Week(startdate , enddate):

    start = startdate
    end = enddate


    sql_query = """
        SELECT
            SUM(CASE WHEN request_type = 'Breakfast' AND location = 'IITM RP' AND date >= %(start)s AND date < %(end)s AND need = 'Yes' THEN 1 ELSE 0 END) AS RP_BF_count,
            SUM(CASE WHEN request_type = 'Lunch' AND location = 'IITM RP' AND date >= %(start)s AND date < %(end)s AND need = 'Yes' THEN 1 ELSE 0 END) AS RP_Lunch_count,
            SUM(CASE WHEN request_type = 'Dinner' AND location = 'IITM RP' AND date >= %(start)s AND date < %(end)s AND need = 'Yes' THEN 1 ELSE 0 END) AS RP_Dinner_count,
            
            SUM(CASE WHEN request_type = 'Breakfast' AND location = 'Thaiyur' AND date >= %(start)s AND date < %(end)s AND need = 'Yes' THEN 1 ELSE 0 END) AS Thaiyur_BF_count,
            SUM(CASE WHEN request_type = 'Lunch' AND location = 'Thaiyur' AND date >= %(start)s AND date < %(end)s AND need = 'Yes' THEN 1 ELSE 0 END) AS Thaiyur_Lunch_count,
            SUM(CASE WHEN request_type = 'Dinner' AND location = 'Thaiyur' AND date >= %(start)s AND date < %(end)s AND need = 'Yes' THEN 1 ELSE 0 END) AS Thaiyur_Dinner_count,

            SUM(CASE WHEN request_type = 'Breakfast' AND location = 'Shar' AND date >= %(start)s AND date < %(end)s AND need = 'Yes' THEN 1 ELSE 0 END) AS Shar_BF_count,
            SUM(CASE WHEN request_type = 'Lunch' AND location = 'Shar' AND date >= %(start)s AND date < %(end)s AND need = 'Yes' THEN 1 ELSE 0 END) AS Shar_Lunch_count,
            SUM(CASE WHEN request_type = 'Dinner' AND location = 'Shar' AND date >= %(start)s AND date < %(end)s AND need = 'Yes' THEN 1 ELSE 0 END) AS Shar_Dinner_count,

            SUM(CASE WHEN request_type = 'Refreshments' AND location = 'IITM RP' AND date >= %(start)s AND date < %(end)s AND need = 'Yes' THEN 1 ELSE 0 END) AS RP_Ref_count,
            SUM(CASE WHEN request_type = 'Refreshments' AND location = 'Thaiyur' AND date >= %(start)s AND date < %(end)s AND need = 'Yes' THEN 1 ELSE 0 END) AS Thaiyur_Ref_count,
            SUM(CASE WHEN request_type = 'Refreshments' AND location = 'Shar' AND date >= %(start)s AND date < %(end)s AND need = 'Yes' THEN 1 ELSE 0 END) AS Shar_Ref_count
            -- Add similar lines for other counts
        FROM
            `tabFood Request`
    """

    result_request = frappe.db.sql(sql_query, {'start': start, 'end': end}, as_dict=True)

    sql_query_manual_count  = """
        SELECT
            SUM(CASE WHEN location = 'IITM RP' THEN COALESCE(breakfast_nveg, 0) + COALESCE(breakfast, 0) ELSE 0 END) AS RP_BF_count,
            SUM(CASE WHEN location = 'IITM RP' THEN COALESCE(lunch_nveg, 0) + COALESCE(lunch, 0) ELSE 0 END) AS RP_Lunch_count,
            SUM(CASE WHEN location = 'IITM RP' THEN COALESCE(dinner_nveg, 0) + COALESCE(dinner, 0) ELSE 0 END) AS RP_Dinner_count,

            SUM(CASE WHEN location = 'Thaiyur' THEN COALESCE(breakfast_nveg, 0) + COALESCE(breakfast, 0) ELSE 0 END) AS Thaiyur_BF_count,
            SUM(CASE WHEN location = 'Thaiyur' THEN COALESCE(lunch_nveg, 0) + COALESCE(lunch, 0) ELSE 0 END) AS Thaiyur_Lunch_count,
            SUM(CASE WHEN location = 'Thaiyur' THEN COALESCE(dinner_nveg, 0) + COALESCE(dinner, 0) ELSE 0 END) AS Thaiyur_Dinner_count,

            SUM(CASE WHEN location = 'Shar' THEN COALESCE(breakfast_nveg, 0) + COALESCE(breakfast, 0) ELSE 0 END) AS Shar_BF_count,
            SUM(CASE WHEN location = 'Shar' THEN COALESCE(lunch_nveg, 0) + COALESCE(lunch, 0) ELSE 0 END) AS Shar_Lunch_count,
            SUM(CASE WHEN location = 'Shar' THEN COALESCE(dinner_nveg, 0) + COALESCE(dinner, 0) ELSE 0 END) AS Shar_Dinner_count
        FROM
            `tabFood Manual Count`
        WHERE 
            date >= %(start)s AND date < %(end)s;
    """
    
    result_manual_count = frappe.db.sql(sql_query_manual_count , {'start': start , 'end': end}, as_dict=True)


    if result_request and result_manual_count:
        merged_result = {
            "RP_BF_count": (result_request[0].RP_BF_count or 0) + (result_manual_count[0].RP_BF_count or 0),
            "RP_Lunch_count": (result_request[0].RP_Lunch_count or 0) + (result_manual_count[0].RP_Lunch_count or 0),
            "RP_Dinner_count": (result_request[0].RP_Dinner_count or 0) + (result_manual_count[0].RP_Dinner_count or 0),
            "Thaiyur_BF_count": (result_request[0].Thaiyur_BF_count or 0) + (result_manual_count[0].Thaiyur_BF_count or 0),
            "Thaiyur_Lunch_count": (result_request[0].Thaiyur_Lunch_count or 0) + (result_manual_count[0].Thaiyur_Lunch_count or 0),
            "Thaiyur_Dinner_count": (result_request[0].Thaiyur_Dinner_count or 0) + (result_manual_count[0].Thaiyur_Dinner_count or 0),
            "Shar_BF_count": (result_request[0].Shar_BF_count or 0) + (result_manual_count[0].Shar_BF_count or 0),
            "Shar_Lunch_count": (result_request[0].Shar_Lunch_count or 0) + (result_manual_count[0].Shar_Lunch_count or 0),
            "Shar_Dinner_count": (result_request[0].Shar_Dinner_count or 0) + (result_manual_count[0].Shar_Dinner_count or 0),
            "RP_Ref_count": result_request[0].RP_Ref_count,
            "Thaiyur_Ref_count": result_request[0].Thaiyur_Ref_count,
            "Shar_Ref_count": result_request[0].Shar_Ref_count,
        }
        return merged_result




# @frappe.whitelist()
# def Food_details_Day(Targetdate):
    
#     date_variable = Targetdate

#     sql_query = """
#         SELECT
#             SUM(CASE WHEN request_type = 'Breakfast' AND location = 'IITM RP' AND date = %(date_variable)s  AND need = 'Yes' THEN 1 ELSE 0 END) AS RP_BF_count,
#             SUM(CASE WHEN request_type = 'Lunch' AND location = 'IITM RP' AND date = %(date_variable)s  AND need = 'Yes' AND food_preference != 'Veg' THEN 1 ELSE 0 END) AS RP_Lunch_count,
#             SUM(CASE WHEN request_type = 'Dinner' AND location = 'IITM RP' AND date = %(date_variable)s  AND need = 'Yes' THEN 1 ELSE 0 END) AS RP_Dinner_count,
            
#             SUM(CASE WHEN request_type = 'Breakfast' AND location = 'Thaiyur' AND date = %(date_variable)s  AND need = 'Yes' THEN 1 ELSE 0 END) AS Thaiyur_BF_count,
#             SUM(CASE WHEN request_type = 'Lunch' AND location = 'Thaiyur' AND date = %(date_variable)s  AND need = 'Yes' AND food_preference != 'Veg' THEN 1 ELSE 0 END) AS Thaiyur_Lunch_count,
#             SUM(CASE WHEN request_type = 'Dinner' AND location = 'Thaiyur' AND date = %(date_variable)s  AND need = 'Yes' THEN 1 ELSE 0 END) AS Thaiyur_Dinner_count,

#             SUM(CASE WHEN request_type = 'Breakfast' AND location = 'Shar' AND date = %(date_variable)s  AND need = 'Yes' THEN 1 ELSE 0 END) AS Shar_BF_count,
#             SUM(CASE WHEN request_type = 'Lunch' AND location = 'Shar' AND date = %(date_variable)s  AND need = 'Yes' AND food_preference != 'Veg' THEN 1 ELSE 0 END) AS Shar_Lunch_count,
#             SUM(CASE WHEN request_type = 'Dinner' AND location = 'Shar' AND date = %(date_variable)s  AND need = 'Yes' THEN 1 ELSE 0 END) AS Shar_Dinner_count,

#             SUM(CASE WHEN request_type = 'Refreshments' AND location = 'IITM RP' AND date = %(date_variable)s  AND need = 'Yes' THEN 1 ELSE 0 END) AS RP_Ref_count,
#             SUM(CASE WHEN request_type = 'Refreshments' AND location = 'Thaiyur' AND date = %(date_variable)s  AND need = 'Yes' THEN 1 ELSE 0 END) AS Thaiyur_Ref_count,
#             SUM(CASE WHEN request_type = 'Refreshments' AND location = 'Shar' AND date = %(date_variable)s  AND need = 'Yes' THEN 1 ELSE 0 END) AS Shar_Ref_count,
            
#             SUM(CASE WHEN request_type = 'Lunch' AND location = 'IITM RP' AND date = %(date_variable)s  AND need = 'Yes' AND food_preference = 'Veg' THEN 1 ELSE 0 END) AS RP_Lunch_Veg_count,
#             SUM(CASE WHEN request_type = 'Lunch' AND location = 'Thaiyur' AND date = %(date_variable)s  AND need = 'Yes' AND food_preference = 'Veg' THEN 1 ELSE 0 END) AS Thaiyur_Lunch_Veg_count,
#             SUM(CASE WHEN request_type = 'Lunch' AND location = 'Shar' AND date = %(date_variable)s  AND need = 'Yes' AND food_preference = 'Veg' THEN 1 ELSE 0 END) AS Shar_Lunch_Veg_count

#         FROM
#             `tabFood Request`
#     """

#     # Execute the query
#     result_request = frappe.db.sql(sql_query, {'date_variable': date_variable}, as_dict=True)

#     sql_query_manual_count  = """
#         SELECT
#             SUM(CASE WHEN location = 'IITM RP' THEN breakfast ELSE 0 END) AS RP_BF_count,
#             SUM(CASE WHEN location = 'IITM RP' THEN lunch ELSE 0 END) AS RP_Lunch_count,
#             SUM(CASE WHEN location = 'IITM RP' THEN lunch_veg ELSE 0 END) AS RP_Lunch_Veg_count,
#             SUM(CASE WHEN location = 'IITM RP' THEN dinner ELSE 0 END) AS RP_Dinner_count,

#             SUM(CASE WHEN location = 'Thaiyur' THEN breakfast ELSE 0 END) AS Thaiyur_BF_count,
#             SUM(CASE WHEN location = 'Thaiyur' THEN lunch ELSE 0 END) AS Thaiyur_Lunch_count,
#             SUM(CASE WHEN location = 'Thaiyur' THEN lunch_veg ELSE 0 END) AS Thaiyur_Lunch_Veg_count,
#             SUM(CASE WHEN location = 'Thaiyur' THEN dinner ELSE 0 END) AS Thaiyur_Dinner_count,

#             SUM(CASE WHEN location = 'Shar' THEN breakfast ELSE 0 END) AS Shar_BF_count,
#             SUM(CASE WHEN location = 'Shar' THEN lunch ELSE 0 END) AS Shar_Lunch_count,
#             SUM(CASE WHEN location = 'Shar' THEN lunch_veg ELSE 0 END) AS Shar_Lunch_Veg_count,
#             SUM(CASE WHEN location = 'Shar' THEN dinner ELSE 0 END) AS Shar_Dinner_count
            
#         FROM
#             `tabFood Manual Count`
#         WHERE
#             date = %(date_variable)s

#     """

#     # Execute the query
#     result_manual_count = frappe.db.sql(sql_query_manual_count , {'date_variable': date_variable}, as_dict=True)

#     if result_request and result_manual_count:
#         merged_result = {
#             "RP_BF_count": (result_request[0].RP_BF_count or 0) + (result_manual_count[0].RP_BF_count or 0),
#             "RP_Lunch_count": (result_request[0].RP_Lunch_count or 0) + (result_manual_count[0].RP_Lunch_count or 0),
#             "RP_Lunch_Veg_count": (result_request[0].RP_Lunch_Veg_count or 0) + (result_manual_count[0].RP_Lunch_Veg_count or 0),
#             "RP_Dinner_count": (result_request[0].RP_Dinner_count or 0) + (result_manual_count[0].RP_Dinner_count or 0),
#             "Thaiyur_BF_count": (result_request[0].Thaiyur_BF_count or 0) + (result_manual_count[0].Thaiyur_BF_count or 0),
#             "Thaiyur_Lunch_count": (result_request[0].Thaiyur_Lunch_count or 0) + (result_manual_count[0].Thaiyur_Lunch_count or 0),
#             "Thaiyur_Lunch_Veg_count": (result_request[0].Thaiyur_Lunch_Veg_count or 0) + (result_manual_count[0].Thaiyur_Lunch_Veg_count or 0),
#             "Thaiyur_Dinner_count": (result_request[0].Thaiyur_Dinner_count or 0) + (result_manual_count[0].Thaiyur_Dinner_count or 0),
#             "Shar_BF_count": (result_request[0].Shar_BF_count or 0) + (result_manual_count[0].Shar_BF_count or 0),
#             "Shar_Lunch_count": (result_request[0].Shar_Lunch_count or 0) + (result_manual_count[0].Shar_Lunch_count or 0),
#             "Shar_Lunch_Veg_count": (result_request[0].Shar_Lunch_Veg_count or 0) + (result_manual_count[0].Shar_Lunch_Veg_count or 0),
#             "Shar_Dinner_count": (result_request[0].Shar_Dinner_count or 0) + (result_manual_count[0].Shar_Dinner_count or 0),
#             "RP_Ref_count": result_request[0].RP_Ref_count,
#             "Thaiyur_Ref_count": result_request[0].Thaiyur_Ref_count,
#             "Shar_Ref_count": result_request[0].Shar_Ref_count,
#         }
#         return merged_result






@frappe.whitelist()
def Food_details_Day(Targetdate):
    
    date_variable = Targetdate

    sql_query = """
        SELECT
            SUM(CASE WHEN request_type = 'Breakfast' AND location = 'IITM RP' AND date = %(date_variable)s  AND need = 'Yes' AND food_preference = 'Veg' THEN 1 ELSE 0 END) AS RP_BF_count_veg,
            SUM(CASE WHEN request_type = 'Lunch' AND location = 'IITM RP' AND date = %(date_variable)s  AND need = 'Yes' AND food_preference = 'Veg' THEN 1 ELSE 0 END) AS RP_Lunch_count_veg,
            SUM(CASE WHEN request_type = 'Dinner' AND location = 'IITM RP' AND date = %(date_variable)s  AND need = 'Yes' AND food_preference = 'Veg' THEN 1 ELSE 0 END) AS RP_Dinner_count_veg,
            
            SUM(CASE WHEN request_type = 'Breakfast' AND location = 'Thaiyur' AND date = %(date_variable)s  AND need = 'Yes' AND food_preference = 'Veg' THEN 1 ELSE 0 END) AS Thaiyur_BF_count_veg,
            SUM(CASE WHEN request_type = 'Lunch' AND location = 'Thaiyur' AND date = %(date_variable)s  AND need = 'Yes' AND food_preference = 'Veg' THEN 1 ELSE 0 END) AS Thaiyur_Lunch_count_veg,
            SUM(CASE WHEN request_type = 'Dinner' AND location = 'Thaiyur' AND date = %(date_variable)s  AND need = 'Yes' AND food_preference = 'Veg' THEN 1 ELSE 0 END) AS Thaiyur_Dinner_count_veg,

            SUM(CASE WHEN request_type = 'Breakfast' AND location = 'Shar' AND date = %(date_variable)s  AND need = 'Yes' AND food_preference = 'Veg' THEN 1 ELSE 0 END) AS Shar_BF_count_veg,
            SUM(CASE WHEN request_type = 'Lunch' AND location = 'Shar' AND date = %(date_variable)s  AND need = 'Yes' AND food_preference = 'Veg' THEN 1 ELSE 0 END) AS Shar_Lunch_count_veg,
            SUM(CASE WHEN request_type = 'Dinner' AND location = 'Shar' AND date = %(date_variable)s  AND need = 'Yes' AND food_preference = 'Veg' THEN 1 ELSE 0 END) AS Shar_Dinner_count_veg,

            SUM(CASE WHEN request_type = 'Breakfast' AND location = 'IITM RP' AND date = %(date_variable)s  AND need = 'Yes' AND food_preference != 'Veg' THEN 1 ELSE 0 END) AS RP_BF_count_Nveg,
            SUM(CASE WHEN request_type = 'Lunch' AND location = 'IITM RP' AND date = %(date_variable)s  AND need = 'Yes' AND food_preference != 'Veg' THEN 1 ELSE 0 END) AS RP_Lunch_count_Nveg,
            SUM(CASE WHEN request_type = 'Dinner' AND location = 'IITM RP' AND date = %(date_variable)s  AND need = 'Yes' AND food_preference != 'Veg' THEN 1 ELSE 0 END) AS RP_Dinner_count_Nveg,
            
            SUM(CASE WHEN request_type = 'Breakfast' AND location = 'Thaiyur' AND date = %(date_variable)s  AND need = 'Yes' AND food_preference != 'Veg' THEN 1 ELSE 0 END) AS Thaiyur_BF_count_Nveg,
            SUM(CASE WHEN request_type = 'Lunch' AND location = 'Thaiyur' AND date = %(date_variable)s  AND need = 'Yes' AND food_preference != 'Veg' THEN 1 ELSE 0 END) AS Thaiyur_Lunch_count_Nveg,
            SUM(CASE WHEN request_type = 'Dinner' AND location = 'Thaiyur' AND date = %(date_variable)s  AND need = 'Yes' AND food_preference != 'Veg' THEN 1 ELSE 0 END) AS Thaiyur_Dinner_count_Nveg,

            SUM(CASE WHEN request_type = 'Breakfast' AND location = 'Shar' AND date = %(date_variable)s  AND need = 'Yes' AND food_preference != 'Veg' THEN 1 ELSE 0 END) AS Shar_BF_count_Nveg,
            SUM(CASE WHEN request_type = 'Lunch' AND location = 'Shar' AND date = %(date_variable)s  AND need = 'Yes' AND food_preference != 'Veg' THEN 1 ELSE 0 END) AS Shar_Lunch_count_Nveg,
            SUM(CASE WHEN request_type = 'Dinner' AND location = 'Shar' AND date = %(date_variable)s  AND need = 'Yes' AND food_preference != 'Veg' THEN 1 ELSE 0 END) AS Shar_Dinner_count_Nveg,

            SUM(CASE WHEN request_type = 'Refreshments' AND location = 'IITM RP' AND date = %(date_variable)s  AND need = 'Yes' THEN 1 ELSE 0 END) AS RP_Ref_count,
            SUM(CASE WHEN request_type = 'Refreshments' AND location = 'Thaiyur' AND date = %(date_variable)s  AND need = 'Yes' THEN 1 ELSE 0 END) AS Thaiyur_Ref_count,
            SUM(CASE WHEN request_type = 'Refreshments' AND location = 'Shar' AND date = %(date_variable)s  AND need = 'Yes' THEN 1 ELSE 0 END) AS Shar_Ref_count
            

        FROM
            `tabFood Request`
    """

    # Execute the query
    result_request = frappe.db.sql(sql_query, {'date_variable': date_variable}, as_dict=True)

    sql_query_manual_count  = """
        SELECT
            SUM(CASE WHEN location = 'IITM RP' THEN breakfast ELSE 0 END) AS RP_BF_count_veg,
            SUM(CASE WHEN location = 'IITM RP' THEN lunch ELSE 0 END) AS RP_Lunch_count_veg,
            SUM(CASE WHEN location = 'IITM RP' THEN dinner ELSE 0 END) AS RP_Dinner_count_veg,

            SUM(CASE WHEN location = 'Thaiyur' THEN breakfast ELSE 0 END) AS Thaiyur_BF_count_veg,
            SUM(CASE WHEN location = 'Thaiyur' THEN lunch ELSE 0 END) AS Thaiyur_Lunch_count_veg,
            SUM(CASE WHEN location = 'Thaiyur' THEN dinner ELSE 0 END) AS Thaiyur_Dinner_count_veg,

            SUM(CASE WHEN location = 'Shar' THEN breakfast ELSE 0 END) AS Shar_BF_count_veg,
            SUM(CASE WHEN location = 'Shar' THEN lunch ELSE 0 END) AS Shar_Lunch_count_veg,
            SUM(CASE WHEN location = 'Shar' THEN dinner ELSE 0 END) AS Shar_Dinner_count_veg,

             SUM(CASE WHEN location = 'IITM RP' THEN breakfast_nveg ELSE 0 END) AS RP_BF_count_Nveg,
            SUM(CASE WHEN location = 'IITM RP' THEN lunch_nveg ELSE 0 END) AS RP_Lunch_count_Nveg,
            SUM(CASE WHEN location = 'IITM RP' THEN dinner_nveg ELSE 0 END) AS RP_Dinner_count_Nveg,

            SUM(CASE WHEN location = 'Thaiyur' THEN breakfast_nveg ELSE 0 END) AS Thaiyur_BF_count_Nveg,
            SUM(CASE WHEN location = 'Thaiyur' THEN lunch_nveg ELSE 0 END) AS Thaiyur_Lunch_count_Nveg,
            SUM(CASE WHEN location = 'Thaiyur' THEN dinner_nveg ELSE 0 END) AS Thaiyur_Dinner_count_Nveg,

            SUM(CASE WHEN location = 'Shar' THEN breakfast_nveg ELSE 0 END) AS Shar_BF_count_Nveg,
            SUM(CASE WHEN location = 'Shar' THEN lunch_nveg ELSE 0 END) AS Shar_Lunch_count_Nveg,
            SUM(CASE WHEN location = 'Shar' THEN dinner_nveg ELSE 0 END) AS Shar_Dinner_count_Nveg
            
        FROM
            `tabFood Manual Count`
        WHERE
            date = %(date_variable)s

    """

    # Execute the query
    result_manual_count = frappe.db.sql(sql_query_manual_count , {'date_variable': date_variable}, as_dict=True)

    if result_request and result_manual_count:
        merged_result = {
            "RP_BF_count_veg": (result_request[0].RP_BF_count_veg or 0) + (result_manual_count[0].RP_BF_count_veg or 0),
            "RP_Lunch_count_veg": (result_request[0].RP_Lunch_count_veg or 0) + (result_manual_count[0].RP_Lunch_count_veg or 0),
            "RP_Dinner_count_veg": (result_request[0].RP_Dinner_count_veg or 0) + (result_manual_count[0].RP_Dinner_count_veg or 0),
            "Thaiyur_BF_count_veg": (result_request[0].Thaiyur_BF_count_veg or 0) + (result_manual_count[0].Thaiyur_BF_count_veg or 0),
            "Thaiyur_Lunch_count_veg": (result_request[0].Thaiyur_Lunch_count_veg or 0) + (result_manual_count[0].Thaiyur_Lunch_count_veg or 0),
            "Thaiyur_Dinner_count_veg": (result_request[0].Thaiyur_Dinner_count_veg or 0) + (result_manual_count[0].Thaiyur_Dinner_count_veg or 0),
            "Shar_BF_count_veg": (result_request[0].Shar_BF_count_veg or 0) + (result_manual_count[0].Shar_BF_count_veg or 0),
            "Shar_Lunch_count_veg": (result_request[0].Shar_Lunch_count_veg or 0) + (result_manual_count[0].Shar_Lunch_count_veg or 0),
            "Shar_Dinner_count_veg": (result_request[0].Shar_Dinner_count_veg or 0) + (result_manual_count[0].Shar_Dinner_count_veg or 0),
            "RP_BF_count_Nveg": (result_request[0].RP_BF_count_Nveg or 0) + (result_manual_count[0].RP_BF_count_Nveg or 0),
            "RP_Lunch_count_Nveg": (result_request[0].RP_Lunch_count_Nveg or 0) + (result_manual_count[0].RP_Lunch_count_Nveg or 0),
            "RP_Dinner_count_Nveg": (result_request[0].RP_Dinner_count_Nveg or 0) + (result_manual_count[0].RP_Dinner_count_Nveg or 0),
            "Thaiyur_BF_count_Nveg": (result_request[0].Thaiyur_BF_count_Nveg or 0) + (result_manual_count[0].Thaiyur_BF_count_Nveg or 0),
            "Thaiyur_Lunch_count_Nveg": (result_request[0].Thaiyur_Lunch_count_Nveg or 0) + (result_manual_count[0].Thaiyur_Lunch_count_Nveg or 0),
            "Thaiyur_Dinner_count_Nveg": (result_request[0].Thaiyur_Dinner_count_Nveg or 0) + (result_manual_count[0].Thaiyur_Dinner_count_Nveg or 0),
            "Shar_BF_count_Nveg": (result_request[0].Shar_BF_count_Nveg or 0) + (result_manual_count[0].Shar_BF_count_Nveg or 0),
            "Shar_Lunch_count_Nveg": (result_request[0].Shar_Lunch_count_Nveg or 0) + (result_manual_count[0].Shar_Lunch_count_Nveg or 0),
            "Shar_Dinner_count_Nveg": (result_request[0].Shar_Dinner_count_Nveg or 0) + (result_manual_count[0].Shar_Dinner_count_Nveg or 0),
            "RP_Ref_count": result_request[0].RP_Ref_count,
            "Thaiyur_Ref_count": result_request[0].Thaiyur_Ref_count,
            "Shar_Ref_count": result_request[0].Shar_Ref_count,
        }
        return merged_result
