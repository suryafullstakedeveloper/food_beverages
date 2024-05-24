import frappe
from datetime import datetime,time ,timedelta

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
def Getreportlist_bsd_filter(Location_filter,Food_Type_filter,Report_Type_filter,date):

    sql_query = """
            SELECT
                user_name as Emp_Name, emp_id as Emp_Id, request_type as Food_Type, date as Date, location as Location
            FROM
                `tabFood Request`
            WHERE
                date = %(date)s and request_type != 'Refreshments' and location != '' and need = 'Yes'
        """
    
    if Location_filter != '':
        sql_query = sql_query + " and location = %(Location_filter)s "
    
    if Food_Type_filter != '':
        sql_query = sql_query + " and request_type = %(Food_Type_filter)s "

    if Report_Type_filter == 'Not Consumed':
        sql_query = sql_query + " and attend = 'No' "

    result = frappe.db.sql(sql_query, {'date': date, 'Location_filter': Location_filter,'Food_Type_filter': Food_Type_filter}, as_dict=True)


    sql_query2 = """
            SELECT
                sum() as Emp_Name, emp_id as Emp_Id, request_type as Food_Type, date as Date, location as Location
            FROM
                `tabFood Request`
            WHERE
                date = %(date)s 
        """
    
    if Location_filter != '':
        sql_query2 = sql_query2 + " and location = %(Location_filter)s "
    
    if Food_Type_filter != '':
        sql_query2 = sql_query2 + " and request_type = %(Food_Type_filter)s "

    result2 = frappe.db.sql(sql_query2, {'date': date, 'Location_filter': Location_filter,'Food_Type_filter': Food_Type_filter}, as_dict=True)

    if result:
        return result



