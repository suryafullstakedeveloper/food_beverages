import frappe
from datetime import datetime,time
# import schedule
import time
from frappe import db

def get_current_date():
    today = datetime.now()
    dd = today.strftime('%d')
    mm = today.strftime('%m')
    yyyy = today.strftime('%Y')

    return f"{yyyy}-{mm}-{dd}"


@frappe.whitelist()
def get_consumables_data(location):
    sql_query = """
        SELECT
            item,
            SUM(CASE WHEN quantity_type = 'Consumed_Quantity' THEN quantity ELSE 0 END) as consumed,
            SUM(CASE WHEN quantity_type = 'Add_Quantity' THEN quantity ELSE 0 END) - 
                SUM(CASE WHEN quantity_type = 'Consumed_Quantity' THEN quantity ELSE 0 END) as available
        FROM
            `tabFood Inventory Consumable Record`
        WHERE
            location = %(location)s
        GROUP BY
            item
    """
    # Execute the query
    result = frappe.db.sql(sql_query, {'location': location}, as_dict=True)

    # Return the results
    return result if result else []


@frappe.whitelist()
def Add_Consumables(Consumable_Item,location_variable,employeeId):

    inventory_consumables = frappe.get_all(
        'Food Consumable Master',
        filters={'location': location_variable,'item':Consumable_Item},
        fields=['name']
    )

    if inventory_consumables:
        return 'recordExists'
    
    else:
    
        doc = frappe.new_doc('Food Consumable Master') 
        doc.item = Consumable_Item,
        doc.location = location_variable,
        doc.created_by = employeeId,
        doc.insert()

        return "Request Successfull.."




@frappe.whitelist()
def Update_consumables(Consumable_Item,employeeId,location_variable,quantity_type,quantity):
   
    doc = frappe.new_doc('Food Inventory Consumable Record') 
    doc.item = Consumable_Item,
    doc.location = location_variable,
    doc.created_by = employeeId,
    doc.quantity_type = quantity_type,
    doc.quantity = quantity,
    doc.insert()

    return 'success'
