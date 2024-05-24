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
def Get_VendorList():

    Vendor_list = frappe.get_all(
        'Food Vendor',
        fields=['name','vendor_id','vendor_name','phone_number','alternate_number','address','gst_number']
    )
    if Vendor_list:
        return Vendor_list





@frappe.whitelist()
def Add_vendor(vendor_id,vendor_name,phone_number,alternate_number,address,gst_Number,employeeId):

    Vendor_list = frappe.get_all(
        'Food Vendor',
        filters={"vendor_id":vendor_id},
        fields=['name']
    )

    if Vendor_list:
        return 'Record exists!'
    
    else:
    
        doc = frappe.new_doc('Food Vendor') 
        doc.vendor_id = vendor_id,
        doc.vendor_name = vendor_name,
        doc.phone_number = phone_number,
        doc.alternate_number = alternate_number,
        doc.address = address,
        doc.gst_number = gst_Number,
        doc.created_by = employeeId,
        doc.insert()

        return "Request Successfull.."




@frappe.whitelist()
def Edit_vendor(vendor_id,vendor_name,phone_number,alternate_number,address,gst_Number,employeeId,id):
   
    doctype = "Food Vendor"
    docname = id
    fields_to_update = {
    "vendor_id": vendor_id,
    "vendor_name": vendor_name,
    "phone_number": phone_number,
    "alternate_number": alternate_number,
    "address": address,
    "gst_Number": gst_Number,
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
def vendor_delete(id):
    try:
        # Specify the doctype
        doctype = "Food Vendor"
        
        # Get the document
        doc = frappe.get_doc(doctype, id)
        
        # Delete the document
        doc.delete()
        
        return True
    except Exception as e:
        return str(e)