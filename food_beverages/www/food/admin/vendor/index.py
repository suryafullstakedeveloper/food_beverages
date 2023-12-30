import frappe
from datetime import datetime,time ,timedelta
from collections import defaultdict

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

   


@frappe.whitelist()
def GetChartBsdFilters(location,date_period,meal):
    end_date = datetime.now()
    today = get_current_date()

    if date_period == 'Day':
        today = get_current_date()
    elif date_period == 'Week':
        weekdays = end_date - timedelta(days=7)
        start_date = date_convertion(weekdays)
    elif date_period == 'Month':
        monthdays = end_date - timedelta(days=30)
        start_date = date_convertion(monthdays)

    if location == 'All' and date_period == 'Day':
        RP_booked = frappe.get_all(
            'Food Request',
            filters={'request_type' : meal, 'location': 'IITM RP','date':today,'need':'Yes'},
            fields=['count(*) as total_count']
        )
        RP_booked_count = RP_booked[0].total_count if RP_booked else 0

        RP_Consumed = frappe.get_all(
            'Food Request',
            filters={'request_type' : meal, 'location': 'IITM RP','date':today,'need':'Yes','attend':'Yes'},
            fields=['count(*) as total_count']
        )
        RP_Consumed_count = RP_Consumed[0].total_count if RP_Consumed else 0

        Thaiyur_booked = frappe.get_all(
            'Food Request',
            filters={'request_type' : meal, 'location': 'Thaiyur','date':today,'need':'Yes'},
            fields=['count(*) as total_count']
        )
        Thaiyur_booked_count = Thaiyur_booked[0].total_count if Thaiyur_booked else 0

        Thaiyur_Consumed = frappe.get_all(
            'Food Request',
            filters={'request_type' : meal, 'location': 'Thaiyur','date':today,'need':'Yes','attend':'Yes'},
            fields=['count(*) as total_count']
        )
        Thaiyur_Consumed_count = Thaiyur_Consumed[0].total_count if Thaiyur_Consumed else 0

        Shar_booked = frappe.get_all(
            'Food Request',
            filters={'request_type' : meal, 'location': 'Shar','date':today,'need':'Yes'},
            fields=['count(*) as total_count']
        )
        Shar_booked_count = Shar_booked[0].total_count if Shar_booked else 0

        Shar_Consumed = frappe.get_all(
            'Food Request',
            filters={'request_type' : meal, 'location': 'Shar','date':today,'need':'Yes','attend':'Yes'},
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

    if location == 'All' and date_period != 'Day':
        if meal == 'All':
            RP_booked = frappe.get_all(
            'Food Request',
            filters={"date": (">=", start_date), "date": ("<=", today), 'location': 'IITM RP', 'need':'Yes','request_type': ['!=', 'Refreshments']},
            fields=['count(*) as total_count']
            )
            RP_booked_count = RP_booked[0].total_count if RP_booked else 0

            RP_Consumed = frappe.get_all(
                'Food Request',
                filters={"date": (">=", start_date), "date": ("<=", today), 'location': 'IITM RP', 'need':'Yes','attend':'Yes','request_type': ['!=', 'Refreshments']},
                fields=['count(*) as total_count']
            )
            RP_Consumed_count = RP_Consumed[0].total_count if RP_Consumed else 0

            Thaiyur_booked = frappe.get_all(
                'Food Request',
                filters={"date": (">=", start_date), "date": ("<=", today), 'location': 'Thaiyur', 'need':'Yes','request_type': ['!=', 'Refreshments']},
                fields=['count(*) as total_count']
            )
            Thaiyur_booked_count = Thaiyur_booked[0].total_count if Thaiyur_booked else 0

            Thaiyur_Consumed = frappe.get_all(
                'Food Request',
                filters={"date": (">=", start_date), "date": ("<=", today), 'location': 'Thaiyur', 'need':'Yes','attend':'Yes','request_type': ['!=', 'Refreshments']},
                fields=['count(*) as total_count']
            )
            Thaiyur_Consumed_count = Thaiyur_Consumed[0].total_count if Thaiyur_Consumed else 0

            Shar_booked = frappe.get_all(
                'Food Request',
                filters={"date": (">=", start_date), "date": ("<=", today), 'location': 'Shar', 'need':'Yes','request_type': ['!=', 'Refreshments']},
                fields=['count(*) as total_count']
            )
            Shar_booked_count = Shar_booked[0].total_count if Shar_booked else 0

            Shar_Consumed = frappe.get_all(
                'Food Request',
                filters={"date": (">=", start_date), "date": ("<=", today), 'location': 'Shar', 'need':'Yes','attend':'Yes','request_type': ['!=', 'Refreshments']},
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

        else:
            RP_booked = frappe.get_all(
            'Food Request',
            filters={'request_type' : meal, "date": (">=", start_date), "date": ("<=", today), 'location': 'IITM RP', 'need':'Yes'},
            fields=['count(*) as total_count']
            )
            RP_booked_count = RP_booked[0].total_count if RP_booked else 0

            RP_Consumed = frappe.get_all(
                'Food Request',
                filters={'request_type' : meal, "date": (">=", start_date), "date": ("<=", today), 'location': 'IITM RP', 'need':'Yes','attend':'Yes'},
                fields=['count(*) as total_count']
            )
            RP_Consumed_count = RP_Consumed[0].total_count if RP_Consumed else 0

            Thaiyur_booked = frappe.get_all(
                'Food Request',
                filters={'request_type' : meal, "date": (">=", start_date), "date": ("<=", today), 'location': 'Thaiyur', 'need':'Yes'},
                fields=['count(*) as total_count']
            )
            Thaiyur_booked_count = Thaiyur_booked[0].total_count if Thaiyur_booked else 0

            Thaiyur_Consumed = frappe.get_all(
                'Food Request',
                filters={'request_type' : meal, "date": (">=", start_date), "date": ("<=", today), 'location': 'Thaiyur', 'need':'Yes','attend':'Yes'},
                fields=['count(*) as total_count']
            )
            Thaiyur_Consumed_count = Thaiyur_Consumed[0].total_count if Thaiyur_Consumed else 0

            Shar_booked = frappe.get_all(
                'Food Request',
                filters={'request_type' : meal, "date": (">=", start_date), "date": ("<=", today), 'location': 'Shar', 'need':'Yes'},
                fields=['count(*) as total_count']
            )
            Shar_booked_count = Shar_booked[0].total_count if Shar_booked else 0

            Shar_Consumed = frappe.get_all(
                'Food Request',
                filters={'request_type' : meal, "date": (">=", start_date), "date": ("<=", today), 'location': 'Shar', 'need':'Yes','attend':'Yes'},
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

    if location != 'All' and date_period == 'Day':
        if meal == 'All':
            Booked = frappe.get_all(
            'Food Request',
            filters={'date':today, 'location': location, 'need':'Yes','request_type': ['!=', 'Refreshments']},
            fields=['count(*) as total_count']
            )
            Final_booked_count = Booked[0].total_count if Booked else 0

            Consumend = frappe.get_all(
                'Food Request',
                filters={'date':today, 'location': location, 'need':'Yes','attend':'Yes','request_type': ['!=', 'Refreshments']},
                fields=['count(*) as total_count']
            )
            Final_Consumed_count = Consumend[0].total_count if Consumend else 0

            Total_food_count = Final_booked_count

            Food_Count = [
                {
                    'booked': Final_booked_count,  
                    'consumed': Final_Consumed_count,
                    'location': location
                }
            ]
            return Food_Count,Total_food_count
        else:
            Booked = frappe.get_all(
            'Food Request',
            filters={'request_type' : meal, 'date':today, 'location': location, 'need':'Yes'},
            fields=['count(*) as total_count']
            )
            Final_booked_count = Booked[0].total_count if Booked else 0

            Consumend = frappe.get_all(
                'Food Request',
                filters={'request_type' : meal, 'date':today, 'location': location, 'need':'Yes','attend':'Yes'},
                fields=['count(*) as total_count']
            )
            Final_Consumed_count = Consumend[0].total_count if Consumend else 0

            Total_food_count = Final_booked_count

            Food_Count = [
                {
                    'booked': Final_booked_count,  
                    'consumed': Final_Consumed_count,
                    'location': location
                }
            ]
            return Food_Count,Total_food_count

    if location != 'All' and date_period != 'Day':
        if meal == 'All':
            Booked = frappe.get_all(
            'Food Request',
            filters={"date": (">=", start_date), "date": ("<=", today), 'location': location, 'need':'Yes','request_type': ['!=', 'Refreshments']},
            fields=['count(*) as total_count']
            )
            Final_booked_count = Booked[0].total_count if Booked else 0

            Consumend = frappe.get_all(
                'Food Request',
                filters={"date": (">=", start_date), "date": ("<=", today), 'location': location, 'need':'Yes','attend':'Yes','request_type': ['!=', 'Refreshments']},
                fields=['count(*) as total_count']
            )
            Final_Consumed_count = Consumend[0].total_count if Consumend else 0

            Total_food_count = Final_booked_count

            Food_Count = [
                {
                    'booked': Final_booked_count,  
                    'consumed': Final_Consumed_count,
                    'location': location
                }
            ]
            return Food_Count,Total_food_count
        else:
            Booked = frappe.get_all(
            'Food Request',
            filters={'request_type' : meal, "date": (">=", start_date), "date": ("<=", today), 'location': location, 'need':'Yes'},
            fields=['count(*) as total_count']
            )
            Final_booked_count = Booked[0].total_count if Booked else 0

            Consumend = frappe.get_all(
                'Food Request',
                filters={'request_type' : meal, "date": (">=", start_date), "date": ("<=", today), 'location': location, 'need':'Yes','attend':'Yes'},
                fields=['count(*) as total_count']
            )
            Final_Consumed_count = Consumend[0].total_count if Consumend else 0

            Total_food_count = Final_booked_count

            Food_Count = [
                {
                    'booked': Final_booked_count,  
                    'consumed': Final_Consumed_count,
                    'location': location
                }
            ]
            return Food_Count,Total_food_count



@frappe.whitelist()
def GetCardvalues(date_period, location):
    end_date = datetime.now()
    today = get_current_date()
    total_values = defaultdict(int)

    if date_period == 'Day':
        today = get_current_date()
    elif date_period == 'Week':
        weekdays = end_date - timedelta(days=7)
        start_date = date_convertion(weekdays)
    elif date_period == 'Month':
        monthdays = end_date - timedelta(days=30)
        start_date = date_convertion(monthdays)

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
        
        Cards_value = frappe.get_all(
        'Food Inventory Consumables',
        filters={"date": (">=", start_date), "date": ("<=", today)},
        fields=['coffee_beans','coffee_stirrers','tea_bags','sugar_sachet','packet_biscuits','paper_cups','water_cans',
        'milk_packets','butter_sheet'],
        )
        if Cards_value:
            for day_values in Cards_value:
                for header, value in day_values.items():
                    
                    total_values[header] += int(value)

            total_values_dict = dict(total_values)
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
        
        Cards_value = frappe.get_all(
        'Food Inventory Consumables',
        filters={"location":location,"date": (">=", start_date), "date": ("<=", today)},
        fields=['coffee_beans','coffee_stirrers','tea_bags','sugar_sachet','packet_biscuits','paper_cups','water_cans',
        'milk_packets','butter_sheet'],
        )
        if Cards_value:
            for day_values in Cards_value:
                for header, value in day_values.items():
                    
                    total_values[header] += int(value)

            total_values_dict = dict(total_values)
            return total_values_dict


            