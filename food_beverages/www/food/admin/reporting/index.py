import frappe
import hashlib
from frappe.utils.file_manager import save_file
from datetime import datetime,time ,timedelta
from collections import defaultdict
from frappe import db
import os
import base64

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
def GetReportingList():

    ReportingList = frappe.get_all(
        'Food Reporting',
        fields=['issue','name','description','image','priority','status','location'],
        order_by='name desc',
        limit_page_length=20
    )
    if ReportingList:
        return ReportingList



@frappe.whitelist()
def Add_Reporting(issue, description, imagelink, location, Priority, status, employeeId):
    
    if imagelink:
        doc = frappe.new_doc('Food Reporting') 
        doc.issue = issue
        doc.description = description
        doc.image = imagelink
        doc.priority = Priority
        doc.status = status
        doc.location = location
        doc.created_by = employeeId
        doc.insert()
        return "Request Success"
       
    else:
        doc = frappe.new_doc('Food Reporting') 
        doc.issue = issue
        doc.description = description
        doc.priority = Priority
        doc.status = status
        doc.location = location
        doc.created_by = employeeId
        doc.insert()
        return "Request Success"


@frappe.whitelist()
def Edit_Reporting(issue,description,image,location,Priority,status,employeeId,id):

    if image:
        doctype = "Food Reporting"
        docname = id
        fields_to_update = {
        "issue": issue,
        "description": description,
        "image": image,
        "location": location,
        "Priority": Priority,
        "status": status,
        "modyfied_by": employeeId,
        # Add more fields as needed
        }
        try:
            db.set_value(doctype, docname, fields_to_update)
            # time.sleep(5)
            return True 
        except Exception as e:
            return e
    else:
        doctype = "Food Reporting"
        docname = id
        fields_to_update = {
        "issue": issue,
        "description": description,
        "location": location,
        "Priority": Priority,
        "status": status,
        "modyfied_by": employeeId,
        # Add more fields as needed
        }
        try:
            db.set_value(doctype, docname, fields_to_update)
            # time.sleep(5)
            return True 
        except Exception as e:
            return e


@frappe.whitelist()
def GetReportingList_bsd_filter(priority_filter,status_filter):

    if priority_filter == '' and status_filter == '':

        ReportingList = frappe.get_all(
            'Food Reporting',
            fields=['issue','name','description','image','priority','status','location']
        )
        if ReportingList:
            return ReportingList
    
    elif priority_filter != '' and status_filter == '':

        ReportingList = frappe.get_all(
            'Food Reporting',
            fields=['issue','name','description','image','priority','status','location'],
            filters={'priority': priority_filter},
        )
        if ReportingList:
            return ReportingList
    
    elif priority_filter == '' and status_filter != '':

        ReportingList = frappe.get_all(
            'Food Reporting',
            fields=['issue','name','description','image','priority','status','location'],
            filters={'status': status_filter},
        )
        if ReportingList:
            return ReportingList

    elif priority_filter != '' and status_filter != '':

        ReportingList = frappe.get_all(
            'Food Reporting',
            fields=['issue','name','description','image','priority','status','location'],
            filters={'priority': priority_filter,'status': status_filter},
        )
        if ReportingList:
            return ReportingList
