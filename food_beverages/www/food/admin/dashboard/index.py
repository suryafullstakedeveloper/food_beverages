import frappe
from datetime import datetime,time ,timedelta
from collections import defaultdict
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

@frappe.whitelist()
def GetChartBsdDate(date_period):
    today = get_current_date()

    RP_booked = frappe.get_all(
        'Food Request',
        filters={'location': 'IITM RP','date':today,'need':'Yes','request_type': ['!=', 'Refreshments']},
        fields=['count(*) as total_count']
    )
    RP_booked_count = RP_booked[0].total_count if RP_booked else 0

    RP_Consumed = frappe.get_all(
        'Food Request',
        filters={'location': 'IITM RP','date':today,'need':'Yes','attend':'Yes','request_type': ['!=', 'Refreshments']},
        fields=['count(*) as total_count']
    )
    RP_Consumed_count = RP_Consumed[0].total_count if RP_Consumed else 0

    Thaiyur_booked = frappe.get_all(
        'Food Request',
        filters={'location': 'Thaiyur','date':today,'need':'Yes','request_type': ['!=', 'Refreshments']},
        fields=['count(*) as total_count']
    )
    Thaiyur_booked_count = Thaiyur_booked[0].total_count if Thaiyur_booked else 0

    Thaiyur_Consumed = frappe.get_all(
        'Food Request',
        filters={'location': 'Thaiyur','date':today,'need':'Yes','attend':'Yes','request_type': ['!=', 'Refreshments']},
        fields=['count(*) as total_count']
    )
    Thaiyur_Consumed_count = Thaiyur_Consumed[0].total_count if Thaiyur_Consumed else 0

    Shar_booked = frappe.get_all(
        'Food Request',
        filters={'location': 'Shar','date':today,'need':'Yes','request_type': ['!=', 'Refreshments']},
        fields=['count(*) as total_count']
    )
    Shar_booked_count = Shar_booked[0].total_count if Shar_booked else 0

    Shar_Consumed = frappe.get_all(
        'Food Request',
        filters={'location': 'Shar','date':today,'need':'Yes','attend':'Yes','request_type': ['!=', 'Refreshments']},
        fields=['count(*) as total_count']
    )
    Shar_Consumed_count = Shar_Consumed[0].total_count if Shar_Consumed else 0

    Total_food_count = RP_booked_count + Thaiyur_booked_count + Shar_booked_count

    Food_Count = [
        {
            'booked': RP_booked_count,  
            'consumed': RP_Consumed_count,
            'location':'IITM RP'
        },
        {
            'booked': Thaiyur_booked_count,
            'consumed': Thaiyur_Consumed_count,
            'location':'Thaiyur'
        },
        {
            'booked': Shar_booked_count,
            'consumed': Shar_Consumed_count,
            'location':'Shar'
        }
    ]
    return Food_Count,Total_food_count

   


# @frappe.whitelist()
# def GetChartBsdFilters(location,date_period,meal):
#     end_date = datetime.now()
#     today = get_current_date()

#     if date_period == 'Day':
#         today = get_current_date()
#     elif date_period == 'Week':
#         weekdays = end_date - timedelta(days=7)
#         start_date = date_convertion(weekdays)
#     elif date_period == 'Month':
#         monthdays = end_date - timedelta(days=30)
#         start_date = date_convertion(monthdays)

#     if location == 'All' and date_period == 'Day':
#         RP_booked = frappe.get_all(
#             'Food Request',
#             filters={'request_type' : meal, 'location': 'IITM RP','date':today,'need':'Yes'},
#             fields=['count(*) as total_count']
#         )
#         RP_booked_count = RP_booked[0].total_count if RP_booked else 0

#         RP_Consumed = frappe.get_all(
#             'Food Request',
#             filters={'request_type' : meal, 'location': 'IITM RP','date':today,'need':'Yes','attend':'Yes'},
#             fields=['count(*) as total_count']
#         )
#         RP_Consumed_count = RP_Consumed[0].total_count if RP_Consumed else 0

#         Thaiyur_booked = frappe.get_all(
#             'Food Request',
#             filters={'request_type' : meal, 'location': 'Thaiyur','date':today,'need':'Yes'},
#             fields=['count(*) as total_count']
#         )
#         Thaiyur_booked_count = Thaiyur_booked[0].total_count if Thaiyur_booked else 0

#         Thaiyur_Consumed = frappe.get_all(
#             'Food Request',
#             filters={'request_type' : meal, 'location': 'Thaiyur','date':today,'need':'Yes','attend':'Yes'},
#             fields=['count(*) as total_count']
#         )
#         Thaiyur_Consumed_count = Thaiyur_Consumed[0].total_count if Thaiyur_Consumed else 0

#         Shar_booked = frappe.get_all(
#             'Food Request',
#             filters={'request_type' : meal, 'location': 'Shar','date':today,'need':'Yes'},
#             fields=['count(*) as total_count']
#         )
#         Shar_booked_count = Shar_booked[0].total_count if Shar_booked else 0

#         Shar_Consumed = frappe.get_all(
#             'Food Request',
#             filters={'request_type' : meal, 'location': 'Shar','date':today,'need':'Yes','attend':'Yes'},
#             fields=['count(*) as total_count']
#         )
#         Shar_Consumed_count = Shar_Consumed[0].total_count if Shar_Consumed else 0

#         Total_food_count = RP_booked_count + Thaiyur_booked_count + Shar_booked_count

#         Food_Count = [
#             {
#                 'booked': RP_booked_count,  
#                 'consumed': RP_Consumed_count,
#                 'location':'IITM RP'
#             },
#             {
#                 'booked': Thaiyur_booked_count,
#                 'consumed': Thaiyur_Consumed_count,
#                 'location':'Thaiyur'
#             },
#             {
#                 'booked': Shar_booked_count,
#                 'consumed': Shar_Consumed_count,
#                 'location':'Shar'
#             }
#         ]
#         return Food_Count,Total_food_count

#     if location == 'All' and date_period != 'Day':
#         if meal == 'All':
#             RP_booked = frappe.get_all(
#             'Food Request',
#             filters={"date": (">=", start_date), "date": ("<=", today), 'location': 'IITM RP', 'need':'Yes','request_type': ['!=', 'Refreshments']},
#             fields=['count(*) as total_count']
#             )
#             RP_booked_count = RP_booked[0].total_count if RP_booked else 0

#             RP_Consumed = frappe.get_all(
#                 'Food Request',
#                 filters={"date": (">=", start_date), "date": ("<=", today), 'location': 'IITM RP', 'need':'Yes','attend':'Yes','request_type': ['!=', 'Refreshments']},
#                 fields=['count(*) as total_count']
#             )
#             RP_Consumed_count = RP_Consumed[0].total_count if RP_Consumed else 0

#             Thaiyur_booked = frappe.get_all(
#                 'Food Request',
#                 filters={"date": (">=", start_date), "date": ("<=", today), 'location': 'Thaiyur', 'need':'Yes','request_type': ['!=', 'Refreshments']},
#                 fields=['count(*) as total_count']
#             )
#             Thaiyur_booked_count = Thaiyur_booked[0].total_count if Thaiyur_booked else 0

#             Thaiyur_Consumed = frappe.get_all(
#                 'Food Request',
#                 filters={"date": (">=", start_date), "date": ("<=", today), 'location': 'Thaiyur', 'need':'Yes','attend':'Yes','request_type': ['!=', 'Refreshments']},
#                 fields=['count(*) as total_count']
#             )
#             Thaiyur_Consumed_count = Thaiyur_Consumed[0].total_count if Thaiyur_Consumed else 0

#             Shar_booked = frappe.get_all(
#                 'Food Request',
#                 filters={"date": (">=", start_date), "date": ("<=", today), 'location': 'Shar', 'need':'Yes','request_type': ['!=', 'Refreshments']},
#                 fields=['count(*) as total_count']
#             )
#             Shar_booked_count = Shar_booked[0].total_count if Shar_booked else 0

#             Shar_Consumed = frappe.get_all(
#                 'Food Request',
#                 filters={"date": (">=", start_date), "date": ("<=", today), 'location': 'Shar', 'need':'Yes','attend':'Yes','request_type': ['!=', 'Refreshments']},
#                 fields=['count(*) as total_count']
#             )
#             Shar_Consumed_count = Shar_Consumed[0].total_count if Shar_Consumed else 0

#             Total_food_count = RP_booked_count + Thaiyur_booked_count + Shar_booked_count

#             Food_Count = [
#                 {
#                     'booked': RP_booked_count,  
#                     'consumed': RP_Consumed_count,
#                     'location':'IITM RP'
#                 },
#                 {
#                     'booked': Thaiyur_booked_count,
#                     'consumed': Thaiyur_Consumed_count,
#                     'location':'Thaiyur'
#                 },
#                 {
#                     'booked': Shar_booked_count,
#                     'consumed': Shar_Consumed_count,
#                     'location':'Shar'
#                 }
#             ]
#             return Food_Count,Total_food_count

#         else:
#             RP_booked = frappe.get_all(
#             'Food Request',
#             filters={'request_type' : meal, "date": (">=", start_date), "date": ("<=", today), 'location': 'IITM RP', 'need':'Yes'},
#             fields=['count(*) as total_count']
#             )
#             RP_booked_count = RP_booked[0].total_count if RP_booked else 0

#             RP_Consumed = frappe.get_all(
#                 'Food Request',
#                 filters={'request_type' : meal, "date": (">=", start_date), "date": ("<=", today), 'location': 'IITM RP', 'need':'Yes','attend':'Yes'},
#                 fields=['count(*) as total_count']
#             )
#             RP_Consumed_count = RP_Consumed[0].total_count if RP_Consumed else 0

#             Thaiyur_booked = frappe.get_all(
#                 'Food Request',
#                 filters={'request_type' : meal, "date": (">=", start_date), "date": ("<=", today), 'location': 'Thaiyur', 'need':'Yes'},
#                 fields=['count(*) as total_count']
#             )
#             Thaiyur_booked_count = Thaiyur_booked[0].total_count if Thaiyur_booked else 0

#             Thaiyur_Consumed = frappe.get_all(
#                 'Food Request',
#                 filters={'request_type' : meal, "date": (">=", start_date), "date": ("<=", today), 'location': 'Thaiyur', 'need':'Yes','attend':'Yes'},
#                 fields=['count(*) as total_count']
#             )
#             Thaiyur_Consumed_count = Thaiyur_Consumed[0].total_count if Thaiyur_Consumed else 0

#             Shar_booked = frappe.get_all(
#                 'Food Request',
#                 filters={'request_type' : meal, "date": (">=", start_date), "date": ("<=", today), 'location': 'Shar', 'need':'Yes'},
#                 fields=['count(*) as total_count']
#             )
#             Shar_booked_count = Shar_booked[0].total_count if Shar_booked else 0

#             Shar_Consumed = frappe.get_all(
#                 'Food Request',
#                 filters={'request_type' : meal, "date": (">=", start_date), "date": ("<=", today), 'location': 'Shar', 'need':'Yes','attend':'Yes'},
#                 fields=['count(*) as total_count']
#             )
#             Shar_Consumed_count = Shar_Consumed[0].total_count if Shar_Consumed else 0

#             Total_food_count = RP_booked_count + Thaiyur_booked_count + Shar_booked_count

#             Food_Count = [
#                 {
#                     'booked': RP_booked_count,  
#                     'consumed': RP_Consumed_count,
#                     'location':'IITM RP'
#                 },
#                 {
#                     'booked': Thaiyur_booked_count,
#                     'consumed': Thaiyur_Consumed_count,
#                     'location':'Thaiyur'
#                 },
#                 {
#                     'booked': Shar_booked_count,
#                     'consumed': Shar_Consumed_count,
#                     'location':'Shar'
#                 }
#             ]
#             return Food_Count,Total_food_count

#     if location != 'All' and date_period == 'Day':
#         if meal == 'All':
#             Booked = frappe.get_all(
#             'Food Request',
#             filters={'date':today, 'location': location, 'need':'Yes','request_type': ['!=', 'Refreshments']},
#             fields=['count(*) as total_count']
#             )
#             Final_booked_count = Booked[0].total_count if Booked else 0

#             Consumend = frappe.get_all(
#                 'Food Request',
#                 filters={'date':today, 'location': location, 'need':'Yes','attend':'Yes','request_type': ['!=', 'Refreshments']},
#                 fields=['count(*) as total_count']
#             )
#             Final_Consumed_count = Consumend[0].total_count if Consumend else 0

#             Total_food_count = Final_booked_count

#             Food_Count = [
#                 {
#                     'booked': Final_booked_count,  
#                     'consumed': Final_Consumed_count,
#                     'location': location
#                 }
#             ]
#             return Food_Count,Total_food_count
#         else:
#             Booked = frappe.get_all(
#             'Food Request',
#             filters={'request_type' : meal, 'date':today, 'location': location, 'need':'Yes'},
#             fields=['count(*) as total_count']
#             )
#             Final_booked_count = Booked[0].total_count if Booked else 0

#             Consumend = frappe.get_all(
#                 'Food Request',
#                 filters={'request_type' : meal, 'date':today, 'location': location, 'need':'Yes','attend':'Yes'},
#                 fields=['count(*) as total_count']
#             )
#             Final_Consumed_count = Consumend[0].total_count if Consumend else 0

#             Total_food_count = Final_booked_count

#             Food_Count = [
#                 {
#                     'booked': Final_booked_count,  
#                     'consumed': Final_Consumed_count,
#                     'location': location
#                 }
#             ]
#             return Food_Count,Total_food_count

#     if location != 'All' and date_period != 'Day':
#         if meal == 'All':
#             Booked = frappe.get_all(
#             'Food Request',
#             filters={"date": (">=", start_date), "date": ("<=", today), 'location': location, 'need':'Yes','request_type': ['!=', 'Refreshments']},
#             fields=['count(*) as total_count']
#             )
#             Final_booked_count = Booked[0].total_count if Booked else 0

#             Consumend = frappe.get_all(
#                 'Food Request',
#                 filters={"date": (">=", start_date), "date": ("<=", today), 'location': location, 'need':'Yes','attend':'Yes','request_type': ['!=', 'Refreshments']},
#                 fields=['count(*) as total_count']
#             )
#             Final_Consumed_count = Consumend[0].total_count if Consumend else 0

#             Total_food_count = Final_booked_count

#             Food_Count = [
#                 {
#                     'booked': Final_booked_count,  
#                     'consumed': Final_Consumed_count,
#                     'location': location
#                 }
#             ]
#             return Food_Count,Total_food_count
#         else:
#             Booked = frappe.get_all(
#             'Food Request',
#             filters={'request_type' : meal, "date": (">=", start_date), "date": ("<=", today), 'location': location, 'need':'Yes'},
#             fields=['count(*) as total_count']
#             )
#             Final_booked_count = Booked[0].total_count if Booked else 0

#             Consumend = frappe.get_all(
#                 'Food Request',
#                 filters={'request_type' : meal, "date": (">=", start_date), "date": ("<=", today), 'location': location, 'need':'Yes','attend':'Yes'},
#                 fields=['count(*) as total_count']
#             )
#             Final_Consumed_count = Consumend[0].total_count if Consumend else 0

#             Total_food_count = Final_booked_count

#             Food_Count = [
#                 {
#                     'booked': Final_booked_count,  
#                     'consumed': Final_Consumed_count,
#                     'location': location
#                 }
#             ]
#             return Food_Count,Total_food_count



@frappe.whitelist()
def GetCardvalues(date_period, location):
    end_date = datetime.now()
    today = get_current_date()
    total_values = defaultdict(int)

    if date_period == 'Day':
        today = get_current_date()
    elif date_period == 'Week':
       dates = get_current_week_range()
       start_date = dates['start_date']
       end_date = dates['end_date']

    elif date_period == 'Month':
        dates = get_current_month_range()
        start_date = dates['start_date']
        end_date = dates['end_date']

    if location == 'All' and date_period == 'Day':
        Cards_value = frappe.get_all(
            'Food Inventory Consumables',
            filters={"date": today},
            fields=['coffee_beans', 'coffee_stirrers', 'tea_bags', 'sugar_sachet', 'packet_biscuits',
                    'paper_cups', 'water_cans', 'milk_packets', 'butter_sheet'],
        )
        if Cards_value:
            for day_values in Cards_value:
                for header, value in day_values.items():
                    
                    total_values[header] += int(value)

            total_values_dict = dict(total_values)
            return total_values_dict  



    elif location == 'All' and date_period != 'Day':
        
        sql_query = """
            SELECT
                COALESCE(SUM(coffee_beans), 0) as coffee_beans,
                COALESCE(SUM(coffee_stirrers), 0) as coffee_stirrers,
                COALESCE(SUM(tea_bags), 0) as tea_bags,
                COALESCE(SUM(sugar_sachet), 0) as sugar_sachet,
                COALESCE(SUM(packet_biscuits), 0) as packet_biscuits,
                COALESCE(SUM(paper_cups), 0) as paper_cups,
                COALESCE(SUM(water_cans), 0) as water_cans,
                COALESCE(SUM(milk_packets), 0) as milk_packets,
                COALESCE(SUM(butter_sheet), 0) as butter_sheet
            FROM
                `tabFood Inventory Consumables`
            WHERE
                date >= %(start_date)s AND date <= %(end_date)s
        """

        # Execute the query
        result = frappe.db.sql(sql_query, {'start_date': start_date, 'end_date': end_date}, as_dict=True)

        # Extract the results
        total_values_dict = result[0] if result else {}

        # Return the results
        return total_values_dict

    
    elif location != 'All' and date_period == 'Day':
        
        Cards_value = frappe.get_all(
        'Food Inventory Consumables',
        filters={"date": today,"location":location},
        fields=['coffee_beans','coffee_stirrers','tea_bags','sugar_sachet','packet_biscuits','paper_cups','water_cans',
        'milk_packets','butter_sheet'],
        )

        if Cards_value:

            return Cards_value[0]  

    elif location != 'All' and date_period != 'Day':
        
        sql_query = """
            SELECT
                SUM(coffee_beans) as coffee_beans,
                SUM(coffee_stirrers) as coffee_stirrers,
                SUM(tea_bags) as tea_bags,
                SUM(sugar_sachet) as sugar_sachet,
                SUM(packet_biscuits) as packet_biscuits,
                SUM(paper_cups) as paper_cups,
                SUM(water_cans) as water_cans,
                SUM(milk_packets) as milk_packets,
                SUM(butter_sheet) as butter_sheet
            FROM
                `tabFood Inventory Consumables`
            WHERE
                location = %(location)s AND date >= %(start_date)s AND date <= %(end_date)s
        """

        # Execute the query
        result = frappe.db.sql(sql_query, {'location': location, 'start_date': start_date, 'end_date': end_date}, as_dict=True)

        # Extract the results
        total_values_dict = result[0] if result else {}

        # Return the results
        return total_values_dict











def get_current_week_range():
    # Get today's date
    current_date = datetime.now()

    # Calculate the start date of the current week (Sunday)
    start_date = current_date - timedelta(days=current_date.weekday() + 1)
    
    # Calculate the end date of the current week (Saturday)
    end_date = start_date + timedelta(days=6)

    # Format the dates as strings
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')

    # Return the result as a dictionary
    return {'start_date': start_date_str, 'end_date': end_date_str}


def get_current_month_range():
    # Get today's date
    current_date = datetime.now()

    # Calculate the first day of the current month
    start_date = current_date.replace(day=1)

    # Calculate the last day of the current month
    _, last_day = calendar.monthrange(current_date.year, current_date.month)
    end_date = current_date.replace(day=last_day)

    # Format the dates as strings
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')

    # Return the result as a dictionary
    return {'start_date': start_date_str, 'end_date': end_date_str}


@frappe.whitelist()
def GetChartBsdFilters(location,date_period,meal):
    end_date = datetime.now()
    today = get_current_date()

    if date_period == 'Day':
        today = get_current_date()
    elif date_period == 'Week':
       dates = get_current_week_range()
       start_date = dates['start_date']
       end_date = dates['end_date']

    elif date_period == 'Month':
        dates = get_current_month_range()
        start_date = dates['start_date']
        end_date = dates['end_date']

    if location == 'All' and date_period == 'Day':
        sql_query = """
            SELECT
                SUM(CASE WHEN request_type = %(meal)s AND location = 'IITM RP' AND date = %(today)s AND need = 'Yes' THEN 1 ELSE 0 END) AS RP_booked_count,
                SUM(CASE WHEN request_type = %(meal)s AND location = 'IITM RP' AND date = %(today)s AND need = 'Yes' AND attend = 'Yes' THEN 1 ELSE 0 END) AS RP_Consumed_count,
                
                SUM(CASE WHEN request_type = %(meal)s AND location = 'Thaiyur' AND date = %(today)s AND need = 'Yes' THEN 1 ELSE 0 END) AS Thaiyur_booked_count,
                SUM(CASE WHEN request_type = %(meal)s AND location = 'Thaiyur' AND date = %(today)s AND need = 'Yes' AND attend = 'Yes' THEN 1 ELSE 0 END) AS Thaiyur_Consumed_count,
                
                SUM(CASE WHEN request_type = %(meal)s AND location = 'Shar' AND date = %(today)s AND need = 'Yes' THEN 1 ELSE 0 END) AS Shar_booked_count,
                SUM(CASE WHEN request_type = %(meal)s AND location = 'Shar' AND date = %(today)s AND need = 'Yes' AND attend = 'Yes' THEN 1 ELSE 0 END) AS Shar_Consumed_count,
                
                SUM(CASE WHEN request_type = %(meal)s AND location = 'IITM RP' AND date = %(today)s AND need = 'Yes' THEN 1 ELSE 0 END) +
                SUM(CASE WHEN request_type = %(meal)s AND location = 'Thaiyur' AND date = %(today)s AND need = 'Yes' THEN 1 ELSE 0 END) +
                SUM(CASE WHEN request_type = %(meal)s AND location = 'Shar' AND date = %(today)s AND need = 'Yes' THEN 1 ELSE 0 END) AS Total_food_count
                
            FROM
                `tabFood Request`
        """

        # Execute the query
        result = frappe.db.sql(sql_query, {'meal': meal, 'today': today}, as_dict=True)
                
        # Extract the results
        RP_booked_count = result[0].RP_booked_count
        RP_Consumed_count = result[0].RP_Consumed_count
        Thaiyur_booked_count = result[0].Thaiyur_booked_count
        Thaiyur_Consumed_count = result[0].Thaiyur_Consumed_count
        Shar_booked_count = result[0].Shar_booked_count
        Shar_Consumed_count = result[0].Shar_Consumed_count
        Total_food_count = result[0].Total_food_count

        Food_Count = [
            {
                'booked': RP_booked_count,
                'consumed': RP_Consumed_count,
                'location': 'IITM RP'
            },
            {
                'booked': Thaiyur_booked_count,
                'consumed': Thaiyur_Consumed_count,
                'location': 'Thaiyur'
            },
            {
                'booked': Shar_booked_count,
                'consumed': Shar_Consumed_count,
                'location': 'Shar'
            }
        ]

        # Return the results
        return Food_Count, Total_food_count

    if location == 'All' and date_period != 'Day':
        if meal == 'All':
            sql_query = """
                SELECT
                    SUM(CASE WHEN request_type != 'Refreshments' AND location = 'IITM RP' AND date >= %(start_date)s AND date <= %(end_date)s AND need = 'Yes' THEN 1 ELSE 0 END) AS RP_booked_count,
                    SUM(CASE WHEN request_type != 'Refreshments' AND location = 'IITM RP' AND date >= %(start_date)s AND date <= %(end_date)s AND need = 'Yes' AND attend = 'Yes' THEN 1 ELSE 0 END) AS RP_Consumed_count,
                    
                    SUM(CASE WHEN request_type != 'Refreshments' AND location = 'Thaiyur' AND date >= %(start_date)s AND date <= %(end_date)s AND need = 'Yes' THEN 1 ELSE 0 END) AS Thaiyur_booked_count,
                    SUM(CASE WHEN request_type != 'Refreshments' AND location = 'Thaiyur' AND date >= %(start_date)s AND date <= %(end_date)s AND need = 'Yes' AND attend = 'Yes' THEN 1 ELSE 0 END) AS Thaiyur_Consumed_count,
                    
                    SUM(CASE WHEN request_type != 'Refreshments' AND location = 'Shar' AND date >= %(start_date)s AND date <= %(end_date)s AND need = 'Yes' THEN 1 ELSE 0 END) AS Shar_booked_count,
                    SUM(CASE WHEN request_type != 'Refreshments' AND location = 'Shar' AND date >= %(start_date)s AND date <= %(end_date)s AND need = 'Yes' AND attend = 'Yes' THEN 1 ELSE 0 END) AS Shar_Consumed_count,
                    
                    SUM(CASE WHEN request_type != 'Refreshments' AND location IN ('IITM RP', 'Thaiyur', 'Shar') AND date >= %(start_date)s AND date <= %(end_date)s AND need = 'Yes' THEN 1 ELSE 0 END) AS Total_food_count
                FROM
                    `tabFood Request`
            """
        else:
            sql_query = """
                SELECT
                    SUM(CASE WHEN request_type = %(meal)s AND location = 'IITM RP' AND date >= %(start_date)s AND date <= %(end_date)s AND need = 'Yes' THEN 1 ELSE 0 END) AS RP_booked_count,
                    SUM(CASE WHEN request_type = %(meal)s AND location = 'IITM RP' AND date >= %(start_date)s AND date <= %(end_date)s AND need = 'Yes' AND attend = 'Yes' THEN 1 ELSE 0 END) AS RP_Consumed_count,
                    
                    SUM(CASE WHEN request_type = %(meal)s AND location = 'Thaiyur' AND date >= %(start_date)s AND date <= %(end_date)s AND need = 'Yes' THEN 1 ELSE 0 END) AS Thaiyur_booked_count,
                    SUM(CASE WHEN request_type = %(meal)s AND location = 'Thaiyur' AND date >= %(start_date)s AND date <= %(end_date)s AND need = 'Yes' AND attend = 'Yes' THEN 1 ELSE 0 END) AS Thaiyur_Consumed_count,
                    
                    SUM(CASE WHEN request_type = %(meal)s AND location = 'Shar' AND date >= %(start_date)s AND date <= %(end_date)s AND need = 'Yes' THEN 1 ELSE 0 END) AS Shar_booked_count,
                    SUM(CASE WHEN request_type = %(meal)s AND location = 'Shar' AND date >= %(start_date)s AND date <= %(end_date)s AND need = 'Yes' AND attend = 'Yes' THEN 1 ELSE 0 END) AS Shar_Consumed_count,
                    
                    SUM(CASE WHEN request_type = %(meal)s AND location IN ('IITM RP', 'Thaiyur', 'Shar') AND date >= %(start_date)s AND date <= %(end_date)s AND need = 'Yes' THEN 1 ELSE 0 END) AS Total_food_count
                FROM
                    `tabFood Request`
            """

        # Execute the query
        result = frappe.db.sql(sql_query, {'meal': meal, 'start_date': start_date, 'end_date': end_date}, as_dict=True)
        # Check if the result is not empty

        if result:
            # Extract the results
            RP_booked_count = result[0].RP_booked_count
            RP_Consumed_count = result[0].RP_Consumed_count
            Thaiyur_booked_count = result[0].Thaiyur_booked_count
            Thaiyur_Consumed_count = result[0].Thaiyur_Consumed_count
            Shar_booked_count = result[0].Shar_booked_count
            Shar_Consumed_count = result[0].Shar_Consumed_count
            Total_food_count = result[0].Total_food_count

            Food_Count = [
                {
                    'booked': RP_booked_count,  
                    'consumed': RP_Consumed_count,
                    'location': 'IITM RP'
                },
                {
                    'booked': Thaiyur_booked_count,
                    'consumed': Thaiyur_Consumed_count,
                    'location': 'Thaiyur'
                },
                {
                    'booked': Shar_booked_count,
                    'consumed': Shar_Consumed_count,
                    'location': 'Shar'
                }
            ]
            return Food_Count, Total_food_count

    if location != 'All' and date_period == 'Day':
        if meal == 'All':
            sql_query = """
                SELECT
                    SUM(CASE WHEN request_type != 'Refreshments' AND date = %(today)s AND location = %(location)s AND need = 'Yes' THEN 1 ELSE 0 END) AS Final_booked_count,
                    SUM(CASE WHEN request_type != 'Refreshments' AND date = %(today)s AND location = %(location)s AND need = 'Yes' AND attend = 'Yes' THEN 1 ELSE 0 END) AS Final_Consumed_count,
                    SUM(CASE WHEN request_type != 'Refreshments' AND date = %(today)s AND location = %(location)s AND need = 'Yes' THEN 1 ELSE 0 END) AS Total_food_count
                FROM
                    `tabFood Request`
            """
        else:
            sql_query = """
                SELECT
                    SUM(CASE WHEN request_type = %(meal)s AND date = %(today)s AND location = %(location)s AND need = 'Yes' THEN 1 ELSE 0 END) AS Final_booked_count,
                    SUM(CASE WHEN request_type = %(meal)s AND date = %(today)s AND location = %(location)s AND need = 'Yes' AND attend = 'Yes' THEN 1 ELSE 0 END) AS Final_Consumed_count,
                    SUM(CASE WHEN request_type = %(meal)s AND date = %(today)s AND location = %(location)s AND need = 'Yes' THEN 1 ELSE 0 END) AS Total_food_count
                FROM
                    `tabFood Request`
            """

        # Execute the query
        result = frappe.db.sql(sql_query, {'meal': meal, 'today': today, 'location': location}, as_dict=True)

        # Check if the result is not empty
        if result:
            # Extract the results
            Final_booked_count = result[0].Final_booked_count
            Final_Consumed_count = result[0].Final_Consumed_count
            Total_food_count = result[0].Total_food_count

            Food_Count = [
                {
                    'booked': Final_booked_count,
                    'consumed': Final_Consumed_count,
                    'location': location
                }
            ]
            return Food_Count, Total_food_count

    if location != 'All' and date_period != 'Day':
        if meal == 'All':
            sql_query = """
                SELECT
                    SUM(CASE WHEN request_type != 'Refreshments' AND date >= %(start_date)s AND date <= %(end_date)s AND location = %(location)s AND need = 'Yes' THEN 1 ELSE 0 END) AS Final_booked_count,
                    SUM(CASE WHEN request_type != 'Refreshments' AND date >= %(start_date)s AND date <= %(end_date)s AND location = %(location)s AND need = 'Yes' AND attend = 'Yes' THEN 1 ELSE 0 END) AS Final_Consumed_count,
                    SUM(CASE WHEN request_type != 'Refreshments' AND date >= %(start_date)s AND date <= %(end_date)s AND location = %(location)s AND need = 'Yes' THEN 1 ELSE 0 END) AS Total_food_count
                FROM
                    `tabFood Request`
            """
        else:
            sql_query = """
                SELECT
                    SUM(CASE WHEN request_type = %(meal)s AND date >= %(start_date)s AND date <= %(end_date)s AND location = %(location)s AND need = 'Yes' THEN 1 ELSE 0 END) AS Final_booked_count,
                    SUM(CASE WHEN request_type = %(meal)s AND date >= %(start_date)s AND date <= %(end_date)s AND location = %(location)s AND need = 'Yes' AND attend = 'Yes' THEN 1 ELSE 0 END) AS Final_Consumed_count,
                    SUM(CASE WHEN request_type = %(meal)s AND date >= %(start_date)s AND date <= %(end_date)s AND location = %(location)s AND need = 'Yes' THEN 1 ELSE 0 END) AS Total_food_count
                FROM
                    `tabFood Request`
            """

        # Execute the query
        result = frappe.db.sql(sql_query, {'meal': meal, 'start_date': start_date, 'end_date': end_date, 'location': location}, as_dict=True)

        # Check if the result is not empty
        if result:
            # Extract the results
            Final_booked_count = result[0].Final_booked_count
            Final_Consumed_count = result[0].Final_Consumed_count
            Total_food_count = result[0].Total_food_count

            Food_Count = [
                {
                    'booked': Final_booked_count,
                    'consumed': Final_Consumed_count,
                    'location': location
                }
            ]

            # Return the results
            return Food_Count, Total_food_count




# @frappe.whitelist()
# def get_consumables_cards_data(date_period,location):
#     if location != 'All' and date_period == 'Day':
#         sql_query = """
#             SELECT
#                 item as name,
#                 SUM(CASE WHEN quantity_type = 'Consumed_Quantity' THEN quantity ELSE 0 END) as value
#             FROM
#                 `tabFood Inventory Consumable Record`
#             WHERE
#                 location = %(location)s and date(creation) = curdate()
#             GROUP BY
#                 item
#             ORDER BY
#                 id
#         """
#         # Execute the query
#         result = frappe.db.sql(sql_query, {'location': location}, as_dict=True)

#         # Return the results
#         return result if result else []

#     if location == 'All' and date_period == 'Day':
#         sql_query = """
#             SELECT
#                 item as name,
#                 SUM(CASE WHEN quantity_type = 'Consumed_Quantity' THEN quantity ELSE 0 END) as value
#             FROM
#                 `tabFood Inventory Consumable Record`
#             WHERE
#                  date(creation) = curdate()
#             GROUP BY
#                 item
#             ORDER BY
#                 id
#         """
#         # Execute the query
#         result = frappe.db.sql(sql_query, {'location': location}, as_dict=True)

#         # Return the results
#         return result if result else []


@frappe.whitelist()
def get_consumables_cards_data(date_period, location):

    if date_period == 'Week':
        dates = get_current_week_range()
        start_date = dates['start_date']
        end_date = dates['end_date']

    elif date_period == 'Month':
        dates = get_current_month_range()
        start_date = dates['start_date']
        end_date = dates['end_date']


    if location != 'All' and date_period == 'Day':
        sql_query = """
            SELECT
                i.item as name,
                COALESCE(SUM(CASE WHEN r.quantity_type = 'Consumed_Quantity' THEN r.quantity ELSE 0 END), 0) as value
            FROM
                (SELECT DISTINCT item FROM `tabFood Inventory Consumable Record` WHERE location = %(location)s) as i
            LEFT JOIN
                `tabFood Inventory Consumable Record` as r
            ON
                i.item = r.item AND date(r.creation) = curdate() AND r.location = %(location)s
            GROUP BY
                i.item
            ORDER BY
                i.item
        """
        # Execute the query
        result = frappe.db.sql(sql_query, {'location': location}, as_dict=True)

        # Return the results
        return result if result else []

    if location == 'All' and date_period == 'Day':
        sql_query = """
            SELECT
                i.item as name,
                COALESCE(SUM(CASE WHEN r.quantity_type = 'Consumed_Quantity' THEN r.quantity ELSE 0 END), 0) as value
            FROM
                (SELECT DISTINCT item FROM `tabFood Inventory Consumable Record`) as i
            LEFT JOIN
                `tabFood Inventory Consumable Record` as r
            ON
                i.item = r.item AND date(r.creation) = curdate()
            GROUP BY
                i.item
            ORDER BY
                i.item
        """
        # Execute the query
        result = frappe.db.sql(sql_query, {'location': location}, as_dict=True)

        # Return the results
        return result if result else []

    
    if location == 'All' and date_period != 'Day':
        sql_query = """
            SELECT
                i.item as name,
                COALESCE(SUM(CASE WHEN r.quantity_type = 'Consumed_Quantity' THEN r.quantity ELSE 0 END), 0) as value
            FROM
                (SELECT DISTINCT item FROM `tabFood Inventory Consumable Record`) as i
            LEFT JOIN
                `tabFood Inventory Consumable Record` as r
            ON
                i.item = r.item AND date(r.creation) BETWEEN %(start_date)s AND %(end_date)s
            GROUP BY
                i.item
            ORDER BY
                i.item
        """
        # Execute the query
        result = frappe.db.sql(sql_query, {'start_date': start_date, 'end_date': end_date}, as_dict=True)

        # Return the results
        return result if result else []

    if location != 'All' and date_period != 'Day':
        sql_query = """
            SELECT
                i.item as name,
                COALESCE(SUM(CASE WHEN r.quantity_type = 'Consumed_Quantity' THEN r.quantity ELSE 0 END), 0) as value
            FROM
                (SELECT DISTINCT item FROM `tabFood Inventory Consumable Record` WHERE location = %(location)s) as i
            LEFT JOIN
                (SELECT * FROM `tabFood Inventory Consumable Record` WHERE location = %(location)s) as r
            ON
                i.item = r.item AND date(r.creation) BETWEEN %(start_date)s AND %(end_date)s
            GROUP BY
                i.item
            ORDER BY
                i.item
        """
        # Execute the query
        result = frappe.db.sql(sql_query, {'location': location, 'start_date': start_date, 'end_date': end_date}, as_dict=True)

        # Return the results
        return result if result else []