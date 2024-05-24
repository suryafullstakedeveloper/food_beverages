import frappe
from datetime import datetime,time ,timedelta
from collections import defaultdict
from frappe import db
import pytz

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
def GetBillingList():

    BillingList = frappe.get_all(
        'Food Billing',
        fields=['request_type','name','bill_no','bill_amount','amound_paid','balance','payment_type','payment_status','location']
    )
    if BillingList:
        return BillingList




@frappe.whitelist()
def Add_Billing(request_type,bill_no,bill_amount,amound_paid,balance,payment_type,payment_status,location,employeeId):

    doc = frappe.new_doc('Food Billing') 
    doc.request_type = request_type,
    doc.bill_no = bill_no,
    doc.bill_amount = bill_amount,
    doc.amound_paid = amound_paid,
    doc.balance = balance,
    doc.payment_type = payment_type,
    doc.payment_status = payment_status,
    doc.location = location,
    doc.created_by = employeeId,
    doc.insert()

    return "Request Successfull.."




@frappe.whitelist()
def Edit_billing(request_type,bill_no,bill_amount,amound_paid,balance,payment_type,payment_status,location,employeeId,id):
   
    doctype = "Food Billing"
    docname = id
    fields_to_update = {
    "request_type": request_type,
    "bill_no": bill_no,
    "bill_amount": bill_amount,
    "amound_paid": amound_paid,
    "balance": balance,
    "payment_type": payment_type,
    "payment_status": payment_status,
    "location": location,
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
def GetBillingList_bsd_filter(payment_type_filter,payment_status_filter):

    if payment_type_filter == '' and payment_status_filter == '':

        BillingList = frappe.get_all(
            'Food Billing',
            fields=['request_type','name','bill_no','bill_amount','amound_paid','balance','payment_type','payment_status','location']
        )
        if BillingList:
            return BillingList
    
    elif payment_type_filter != '' and payment_status_filter == '':

        BillingList = frappe.get_all(
            'Food Billing',
            fields=['request_type','name','bill_no','bill_amount','amound_paid','balance','payment_type','payment_status','location'],
            filters={'payment_type': payment_type_filter},
        )
        if BillingList:
            return BillingList
    
    elif payment_type_filter == '' and payment_status_filter != '':

        BillingList = frappe.get_all(
            'Food Billing',
            fields=['request_type','name','bill_no','bill_amount','amound_paid','balance','payment_type','payment_status','location'],
            filters={'payment_status': payment_status_filter},
        )
        if BillingList:
            return BillingList

    elif payment_type_filter != '' and payment_status_filter != '':

        BillingList = frappe.get_all(
            'Food Billing',
            fields=['request_type','name','bill_no','bill_amount','amound_paid','balance','payment_type','payment_status','location'],
            filters={'payment_status': payment_status_filter,'payment_type': payment_type_filter},
        )
        if BillingList:
            return BillingList




@frappe.whitelist()
def GetNotificationList(user_id):
    ist_timezone = pytz.timezone('Asia/Kolkata')
    today = get_current_date()
    sql_query = """
    SELECT
        CASE WHEN tnr.name IS NOT NULL THEN true ELSE false END as is_read,
        fn.name,
        fn.title,
        fn.description,
        fn.end_date,
        fn.location,
        fn.creation as creation_timestamp
    FROM
        `tabFood Notification` fn
    LEFT JOIN
        `tabFood Notification Read Record` tnr
    ON
        tnr.notification_id = fn.name AND tnr.user_id = %(user_id)s
    WHERE
        (fn.end_date = %(today)s OR fn.end_date > %(today)s)
    ORDER BY
        fn.creation DESC
    """
    # Execute the query
    result = frappe.db.sql(sql_query, {'user_id': user_id,'today': today}, as_dict=True)


    for item in result:
        if 'creation_timestamp' in item:
            creation_timestamp = item['creation_timestamp'].astimezone(ist_timezone)
            item['time_ago'] = calculate_time_difference(creation_timestamp, ist_timezone)
            

    # Return the results
    return result if result else []





# def calculate_time_difference(creation_timestamp):
#     current_time = datetime.utcnow()
#     time_difference = current_time - creation_timestamp

#     if time_difference.days > 7:
#         return creation_timestamp.strftime("%b %d, %Y %I:%M %p")
#     elif time_difference.days > 0:
#         return f"{time_difference.days}d ago"
#     elif time_difference.seconds >= 3600:
#         return f"{int(time_difference.seconds/3600)}h ago"
#     elif time_difference.seconds >= 60:
#         return f"{int(time_difference.seconds/60)}min ago"
#     else:
#         return "Just now"



# def calculate_time_difference(creation_timestamp):
#     current_time = datetime.now(creation_timestamp.tzinfo)
#     time_difference = current_time - creation_timestamp

#     if time_difference.seconds < 60:
#         return "Just now"
#     elif time_difference.seconds < 3600:
#         minutes_ago = int(time_difference.seconds / 60)
#         return f"{minutes_ago} min ago"
#     elif time_difference.seconds < 86400:
#         hours_ago = int(time_difference.seconds / 3600)
#         return f"{hours_ago} hours ago"
#     else:
#         return creation_timestamp.strftime("%b %d, %Y %I:%M %p")



# def calculate_time_difference(creation_timestamp):
#     current_time = datetime.now(creation_timestamp.tzinfo)
#     time_difference = current_time - creation_timestamp

#     if time_difference.seconds < 60:
#         return "Just now"
#     elif time_difference.seconds < 3600:
#         minutes_ago = int(time_difference.seconds / 60)
#         return f"{minutes_ago} min ago"
#     elif time_difference.seconds < 86400:
#         hours_ago = int(time_difference.seconds / 3600)
#         return f"{hours_ago} hours ago"
#     else:
#         days_ago = int(time_difference.days)
#         if days_ago == 1:
#             return "Yesterday"
#         else:
#             return creation_timestamp.strftime("%b %d, %Y %I:%M %p")




def calculate_time_difference(creation_timestamp, ist_timezone):
    current_time = datetime.now(ist_timezone)
    time_difference = current_time - creation_timestamp

    if time_difference.seconds < 60:
        return "Just now"
    elif time_difference.seconds < 3600:
        minutes_ago = int(time_difference.seconds / 60)
        return f"{minutes_ago} min ago"
    elif time_difference.seconds < 86400:
        hours_ago = int(time_difference.seconds / 3600)
        return f"{hours_ago} hours ago"
    else:
        days_ago = int(time_difference.days)
        if days_ago == 1:
            return "Yesterday"
        else:
            return creation_timestamp.strftime("%b %d, %Y %I:%M %p")




@frappe.whitelist()
def Add_read(user_id,id):

    check_notification_read = frappe.get_all(
        'Food Notification Read Record',
            fields=['name'],
            filters={'notification_id': id,'user_id': user_id},
        )

    if check_notification_read:
        return "Request Successfull.."

    else:
        doc = frappe.new_doc('Food Notification Read Record') 
        doc.notification_id = id,
        doc.user_id = user_id,
        doc.insert()

        return "Request Successfull.."
