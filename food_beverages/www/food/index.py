# import schedule
# import time as tm
# from datetime import time, timedelta, datetime
# import frappe

# @frappe.whitelist()
# def job():
#     print("hihihihi")
    
#     records = frappe.get_all(
#         'Quotes',
#         fields=['name'],
#         order_by='date asc',
#         limit_page_length=1
#     )
#     if records:
#         record = records[0]
#         id = record.get('name')

#         doctype = "Quotes"
#         docname = id
#         fields_to_update = {
#         "date": frappe.utils.nowdate()
#         }
#         try:
#             db.set_value(doctype, docname, fields_to_update)
#             return 'Success'
#         except Exception as e:
#             return e

# schedule.every(1).seconds.do(job)


# while True:
#     schedule.run_pending()
#     tm.sleep(1)