import uuid
import re
import math
import json


RECEIPTS = {}

def generate_id(data) -> dict:
    """
    This function generates a unique ID for a receipt.
    Args:
        data (dict): The receipt data.
    Returns:
        dict: The ID.
    """
    try: 
        # check if receipt already exists
        json_string = json.dumps(data, sort_keys=True)
        existing_id = None
        for key, value in RECEIPTS.items():
            if json.dumps(value, sort_keys=True) == json_string:
                existing_id = key
                break

        if existing_id: # return existing ID if receipt already exists
            return {'id': existing_id}
        else: # generate new ID if receipt does not exist
            required_keys = set(['retailer', 'total', 'items', 'purchaseDate', 'purchaseTime'])
            
            if required_keys.issubset(set(data.keys())):
                id = str(uuid.uuid4())
                RECEIPTS[id] = data
                print("Receipts: ", RECEIPTS)
                return {'id': id}
            else:
                return {'message': 'Error! Missing required keys. Required keys: {}'.format(required_keys)}
    except Exception as e:
        return {'message': 'Something went wrong! Error: {}'.format(e)}


def generate_points(id: str) -> dict:
    """
    This function calculates points awarded for a given receipt ID.
    1 point for every alphanumeric character in retailer name
    50 points if total is round number with no cents
    25 points if total is multiple of 0.25
    5 points for every 2 items
    if trimmed length of desc is multiple of 3, multiply price by 0.2 and round to nearest int. 
    6 points if the day of purchase date is odd
    10 points if time of purchase is between 2pm and 4pm
    Args:
        id (str): The receipt ID.
    Returns:
        dict: The points awarded.
    """
    try: 
        print("ID: ", id)
        receipt = RECEIPTS[id]
        
        print("Retrieved receipt: ", receipt)
        total_points_awarded = 0
        total_points_awarded += retailer_points(receipt['retailer']) + total_points(receipt['total']) + items_points(receipt['items']) + description_points(receipt['items']) + date_points(receipt['purchaseDate']) + time_points(receipt['purchaseTime'])
        print(total_points_awarded)
        return {'points': total_points_awarded}
    except Exception as e:
        print(e)
        return {'message': 'Something went wrong! Enter a valid receipt ID. Error: {}'.format(e)} 
    

def retailer_points(retailer: str) -> int:
    """
    This function counts alphanumeric chars in a given retailer name.
    Args:
        retailer (str): The retailer name.
    Returns:
        int: The points awarded.
    """
    try:
        pattern = re.compile(r"[^\w]")
        return len(pattern.sub('', retailer))
    
    except Exception as e:
        print(e)
        return 0
    
def total_points(total: str) -> int:
    """
    This function calculates points awarded for a given total.
    Args:
        total (str): The total.
    Returns:
        int: The points awarded.
    """
    try:
        points = 0
        total = float(total)
        if total % 1 == 0.0:
            points += 50
        if total % 0.25 == 0.0:
            points += 25
        print("total: ", points)
        return points
    
    except Exception as e:
        print(e)
        return 0

def items_points(items: list) -> int:
    """
    This function calculates points awarded for a given list of items.
    Args:
        items (list): List of dictionaries containing item details.
    Returns:
        int: The points awarded.
    """
    try:
        print("items: ", len(items) // 2 * 5)
        return len(items) // 2 * 5
    
    except Exception as e:
        print(e)
        return 0

def description_points(items: list) -> int:
    """
    This function calculates points awarded for a given description.
    Args:
        items (list): The list of items containing description and price.
    Returns:
        int: The points awarded.
    """
    try:
        points = 0
        for item in items:
            description = item['shortDescription']
            price = float(item['price'])
            if len(description.strip()) % 3 == 0:
                points += math.ceil(price * 0.2)
        print("description: ", points)
        return points
    
    except Exception as e:
        print(e)
        return 0

def date_points(date: str) -> int:
    """
    This function calculates points awarded for a given date.
    Args:
        date (str): The date.
    Returns:
        int: The points awarded.
    """
    try:
        points = 0
        # check if date string is in YYYY-MM-DD format
        if len(date.split('-')) != 3 and len(date.split('-')[0]) != 4:
            return 0
        if int(date.split('-')[2]) % 2 != 0:
            points += 6
        return points
    
    except Exception as e:
        print(e)
        return 0

def time_points(time: str) -> int:
    """
    This function calculates points awarded for a given time.
    Args:
        time (str): The time in 24-hour format -> HH:MM
    Returns:
        int: The points awarded.
    """
    try:
        points = 0
        # check if time string is valid
        if len(time.split(':')) != 2:
            return 0
        if 14 <= int(time.split(':')[0]) <= 16:
            points += 10
        print("time: ", points)
        return points
    
    except Exception as e:
        print(e)
        return 0