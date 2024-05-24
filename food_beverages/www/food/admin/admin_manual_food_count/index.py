import frappe
from datetime import datetime,time ,timedelta
from collections import defaultdict
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
def GetExistingValues(date,location):

    listvalues = frappe.get_all(
        'Food Manual Count',
        fields=['category','breakfast','lunch','dinner','breakfast_nveg','lunch_nveg','dinner_nveg'],
        filters={'date': date , 'location':location},
    )
    if listvalues:
        return listvalues




@frappe.whitelist()
def Add(Painters_breakfast,Painters_lunch,Painters_dinner,
SecurityGuards_breakfast,SecurityGuards_lunch,SecurityGuards_dinner,
Housekeepers_breakfast,Housekeepers_lunch,Housekeepers_dinner,Advisors_breakfast,
Advisors_lunch,Advisors_dinner,Investors_breakfast,Investors_lunch,
Investors_dinner,Others_breakfast,Others_lunch,Others_dinner,Painters_breakfast_Nveg,
Painters_lunch_Nveg,Painters_dinner_Nveg,SecurityGuards_breakfast_Nveg,
SecurityGuards_lunch_Nveg,SecurityGuards_dinner_Nveg,Housekeepers_breakfast_Nveg,
Housekeepers_lunch_Nveg,Housekeepers_dinner_Nveg,Advisors_breakfast_Nveg,
Advisors_lunch_Nveg,Advisors_dinner_Nveg,Investors_breakfast_Nveg,
Investors_lunch_Nveg,Investors_dinner_Nveg,Others_breakfast_Nveg,Others_lunch_Nveg,
Others_dinner_Nveg,date,location,employeeId):

    List = frappe.get_all(
        'Food Manual Count',
        fields=['name'],
        filters={'date': date , 'location':location},
    )
    if List:
        sql_query = """
            DELETE FROM `tabFood Manual Count`
            WHERE location = %(location)s AND date = %(date)s
        """
        frappe.db.sql(sql_query, {'location': location, 'date': date})

    if Painters_breakfast != '0' or Painters_lunch != '0' or Painters_dinner != '0' or Painters_breakfast_Nveg != '0' or Painters_lunch_Nveg != '0' or Painters_dinner_Nveg != '0':
        doc = frappe.new_doc('Food Manual Count')
        doc.category = 'Painters',
        doc.date = date,
        doc.location = location,
        doc.breakfast = Painters_breakfast,
        doc.lunch = Painters_lunch,
        doc.dinner = Painters_dinner,
        doc.breakfast_nveg = Painters_breakfast_Nveg,
        doc.lunch_nveg = Painters_lunch_Nveg,
        doc.dinner_nveg = Painters_dinner_Nveg,
        doc.created_by = employeeId,
        doc.insert()

    if SecurityGuards_breakfast != '0' or SecurityGuards_lunch != '0' or SecurityGuards_dinner != '0' or SecurityGuards_breakfast_Nveg != '0' or SecurityGuards_lunch_Nveg != '0' or SecurityGuards_dinner_Nveg != '0':
        doc = frappe.new_doc('Food Manual Count')
        doc.category = 'SecurityGuards',
        doc.date = date,
        doc.location = location,
        doc.breakfast = SecurityGuards_breakfast,
        doc.lunch = SecurityGuards_lunch,
        doc.dinner = SecurityGuards_dinner,
        doc.breakfast_nveg = SecurityGuards_breakfast_Nveg,
        doc.lunch_nveg = SecurityGuards_lunch_Nveg,
        doc.dinner_nveg = SecurityGuards_dinner_Nveg,
        doc.created_by = employeeId,
        doc.insert()

    if Housekeepers_breakfast != '0' or Housekeepers_lunch != '0' or Housekeepers_dinner != '0' or Housekeepers_breakfast_Nveg != '0' or Housekeepers_lunch_Nveg != '0' or Housekeepers_dinner_Nveg != '0':
        doc = frappe.new_doc('Food Manual Count')
        doc.category = 'Housekeepers',
        doc.date = date,
        doc.location = location,
        doc.breakfast = Housekeepers_breakfast,
        doc.lunch = Housekeepers_lunch,
        doc.dinner = Housekeepers_dinner,
        doc.breakfast_nveg = Housekeepers_breakfast_Nveg,
        doc.lunch_nveg = Housekeepers_lunch_Nveg,
        doc.dinner_nveg = Housekeepers_dinner_Nveg,
        doc.created_by = employeeId,
        doc.insert()

    if Advisors_breakfast != '0' or Advisors_lunch != '0' or Advisors_dinner != '0' or Advisors_breakfast_Nveg != '0' or Advisors_lunch_Nveg != '0' or Advisors_dinner_Nveg != '0':
        doc = frappe.new_doc('Food Manual Count')
        doc.category = 'Advisors',
        doc.date = date,
        doc.location = location,
        doc.breakfast = Advisors_breakfast,
        doc.lunch = Advisors_lunch,
        doc.dinner = Advisors_dinner,
        doc.breakfast_nveg = Advisors_breakfast_Nveg,
        doc.lunch_nveg = Advisors_lunch_Nveg,
        doc.dinner_nveg = Advisors_dinner_Nveg,
        doc.created_by = employeeId,
        doc.insert()

    if Investors_breakfast != '0' or Investors_lunch != '0' or Investors_dinner != '0' or Investors_breakfast_Nveg != '0' or Investors_lunch_Nveg != '0' or Investors_dinner_Nveg != '0':
        doc = frappe.new_doc('Food Manual Count')
        doc.category = 'Investors',
        doc.date = date,
        doc.location = location,
        doc.breakfast = Investors_breakfast,
        doc.lunch = Investors_lunch,
        doc.dinner = Investors_dinner,
        doc.breakfast_nveg = Investors_breakfast_Nveg,
        doc.lunch_nveg = Investors_lunch_Nveg,
        doc.dinner_nveg = Investors_dinner_Nveg,
        doc.created_by = employeeId,
        doc.insert()

    if Others_breakfast != '0' or Others_lunch != '0' or Others_dinner != '0' or Others_breakfast_Nveg != '0' or Others_lunch_Nveg != '0' or Others_dinner_Nveg != '0':
        doc = frappe.new_doc('Food Manual Count')
        doc.category = 'Others',
        doc.date = date,
        doc.location = location,
        doc.breakfast = Others_breakfast,
        doc.lunch = Others_lunch,
        doc.dinner = Others_dinner,
        doc.breakfast_nveg = Others_breakfast_Nveg,
        doc.lunch_nveg = Others_lunch_Nveg,
        doc.dinner_nveg = Others_dinner_Nveg,
        doc.created_by = employeeId,
        doc.insert()

    return "Request Successfull.."

