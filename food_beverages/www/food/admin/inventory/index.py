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
def GetInventory_assets(location):

    inventory_assets = frappe.get_all(
        'Food Inventory Assets',
        filters={'location': location},
        fields=['name','item','quantity']
    )

    if inventory_assets:
        return inventory_assets
    


@frappe.whitelist()
def Add_Asset(Asset_Item,Asset_Quantity,employeeId,location_variable):
    
    doc = frappe.new_doc('Food Inventory Assets') 
    doc.item = Asset_Item,
    doc.quantity = Asset_Quantity,
    doc.location = location_variable,
    doc.created_by = employeeId,
    doc.insert()

    return "Request Successfull.."


@frappe.whitelist()
def Update_Asset(id,Asset_Item,Asset_Quantity,employeeId):
   
    doctype = "Food Inventory Assets"
    docname = id
    fields_to_update = {
    "item": Asset_Item,
    "quantity": Asset_Quantity,
    "modifyed_by": employeeId,
    # Add more fields as needed
    }
    try:
        db.set_value(doctype, docname, fields_to_update)
        # time.sleep(5)
        return True 
    except Exception as e:
        return e


@frappe.whitelist()
def Delete_Asset(id):
    try:
        # Specify the doctype
        doctype = "Food Inventory Assets"
        
        # Get the document
        doc = frappe.get_doc(doctype, id)
        
        # Delete the document
        doc.delete()
        
        return True
    except Exception as e:
        return str(e)



@frappe.whitelist()
def GetConsumables_data(location):

    sql_query = """
        SELECT
            name,
            item
        FROM
            `tabFood Consumable Master`
        WHERE
            location = %(location)s
        ORDER BY
            name DESC
    """
    
    # DATE_FORMAT(creation, '%%Y-%%m-%%d %%H:%%i:%%s') as creation

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

        doc = frappe.new_doc('Food Inventory Consumable Record') 
        doc.item = Consumable_Item,
        doc.location = location_variable,
        doc.created_by = employeeId,
        doc.quantity_type = 'Add_Quantity',
        doc.quantity = '0',
        doc.insert()

        return "Request Successfull.."




@frappe.whitelist()
def Edit_Consumables(Consumable_Item, location_variable, employeeId, id):
    try:
        # Check if the record exists in 'Food Consumable Master'
        inventory_consumables = frappe.get_all(
            'Food Consumable Master',
            filters={'location': location_variable, 'item': Consumable_Item},
            fields=['name', 'item']
        )

        if inventory_consumables:
            return 'recordExists'

        else:
            # Retrieve the original item value

            consumables_name = frappe.get_all(
            'Food Consumable Master',
            filters={'name': id},
            fields=['item']
            )

            original_item = consumables_name[0]['item']

            # Update 'Food Consumable Master' record
            frappe.set_value('Food Consumable Master', id, 'item', Consumable_Item)

            # Update 'tabFood Inventory Consumable Record'
            sql_query = """
                UPDATE `tabFood Inventory Consumable Record`
                SET item = %(Consumable_Item)s
                WHERE location = %(location_variable)s AND item = %(original_item)s
            """
            frappe.db.sql(sql_query, {'Consumable_Item': Consumable_Item, 'location_variable': location_variable, 'original_item': original_item})

            return 'Success'

    except Exception as e:
        return str(e)