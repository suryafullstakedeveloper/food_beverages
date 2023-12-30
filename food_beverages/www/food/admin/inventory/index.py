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

    inventory_consumables = frappe.get_all(
        'Food Inventory Consumables',
        filters={'location': location},
        fields=['name','coffee_beans','coffee_stirrers','tea_bags','sugar_sachet','packet_biscuits','paper_cups','water_cans',
        'milk_packets','butter_sheet','date'],
        order_by='name desc',
        limit_page_length=5
    )

    if inventory_consumables:
        return inventory_consumables





@frappe.whitelist()
def Add_Consumables(coffee_beans,coffee_stirrers,tea_bags,sugar_sachet,butter_sheet,packet_biscuits,paper_cups,water_cans,
milk_packets,employeeId,location_variable):

    date = get_current_date()

    inventory_consumables = frappe.get_all(
        'Food Inventory Consumables',
        filters={'location': location_variable,'date':date},
        fields=['name']
    )

    if inventory_consumables:
        return 'recordExists'
    
    else:
    
        doc = frappe.new_doc('Food Inventory Consumables') 
        doc.coffee_beans = coffee_beans,
        doc.coffee_stirrers = coffee_stirrers,
        doc.tea_bags = tea_bags,
        doc.sugar_sachet = sugar_sachet,
        doc.butter_sheet = butter_sheet,
        doc.packet_biscuits = packet_biscuits,
        doc.paper_cups = paper_cups,
        doc.water_cans = water_cans,
        doc.milk_packets = milk_packets,
        doc.location = location_variable,
        doc.date = date,
        doc.created_by = employeeId,
        doc.insert()

        return "Request Successfull.."




@frappe.whitelist()
def Edit_Consumables(coffee_beans,coffee_stirrers,tea_bags,sugar_sachet,butter_sheet,packet_biscuits,paper_cups,water_cans,
milk_packets,employeeId,id):
   
    doctype = "Food Inventory Consumables"
    docname = id
    fields_to_update = {
    'coffee_beans' : coffee_beans,
    'coffee_stirrers' : coffee_stirrers,
    'tea_bags' : tea_bags,
    'sugar_sachet' : sugar_sachet,
    'butter_sheet' : butter_sheet,
    'packet_biscuits' : packet_biscuits,
    'paper_cups' : paper_cups,
    'water_cans' : water_cans,
    'milk_packets' : milk_packets,
    "modifyed_by": employeeId,
    # Add more fields as needed
    }
    try:
        db.set_value(doctype, docname, fields_to_update)
        # time.sleep(5)
        return True 
    except Exception as e:
        return e
