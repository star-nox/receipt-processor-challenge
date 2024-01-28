import uuid
import re
import math


RECEIPTS = {}

def generate_id(data: dict) -> dict:
    """
    This function generates a unique ID for a receipt.
    Args:
        data (dict): The receipt data.
    Returns:
        dict: The ID.
    """
    try: 
        id = str(uuid.uuid4())

        # check if ID already exists, if so, generate a new one.
        while id in RECEIPTS:
            id = str(uuid.uuid4())

        RECEIPTS[id] = data

        return {'id': id}
    except Exception as e:
        print(e)
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
        receipt = RECEIPTS.get(id)
        
        print("Retrieved receipt: ", receipt)
       
        total_points_awarded = retailer_points(receipt['retailer']) + total_points(receipt['total']) + items_points(receipt['items']) + description_points(receipt['items']) + date_points(receipt['purchaseDate']) + time_points(receipt['purchaseTime'])
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
        print("retailer: ", len(pattern.sub('', retailer)))
        return len(pattern.sub('', retailer))
    
    except Exception as e:
        print(e)
        return 0
    
def total_points(total: float) -> int:
    """
    This function calculates points awarded for a given total.
    Args:
        total (float): The total.
    Returns:
        int: The points awarded.
    """
    try:
        points = 0
        if total % 1 == 0:
            points += 50
        if total % 0.25 == 0:
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
        items (list): The items.
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
            print("description length: ", len(description.strip()))
            if len(description.strip()) % 3 == 0:
                print("price per item: ", price * 0.2)  
                print("rounded price per item: ", math.ceil(price * 0.2))
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
        if int(date.split('-')[2]) % 2 != 0:
            points += 6
        print("date: ", points)
        return points
    
    except Exception as e:
        print(e)
        return 0

def time_points(time: str) -> int:
    """
    This function calculates points awarded for a given time.
    Args:
        time (str): The time.
    Returns:
        int: The points awarded.
    """
    try:
        points = 0
        if 1400 <= int(time.split(':')[0]) <= 1600:
            points += 10
        print("time: ", points)
        return points
    
    except Exception as e:
        print(e)
        return 0