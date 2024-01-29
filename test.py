try:
    from main import app
    from receipt_processing import retailer_points, total_points, items_points, description_points, date_points, time_points
    import unittest
    import uuid
    import json

except Exception as e:
    print("Some modules are missing {}".format(e))

TEST_RECIEPT = {
  "retailer": "Target",
  "purchaseDate": "2022-01-01",
  "purchaseTime": "13:01",
  "items": [
    {
      "shortDescription": "Mountain Dew 12PK",
      "price": "6.49"
    },{
      "shortDescription": "Emils Cheese Pizza",
      "price": "12.25"
    },{
      "shortDescription": "Knorr Creamy Chicken",
      "price": "1.26"
    },{
      "shortDescription": "Doritos Nacho Cheese",
      "price": "3.35"
    },{
      "shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ",
      "price": "12.00"
    }
  ],
  "total": "35.35"
}

INVALID_TEST_RECIEPT = {'restaurant': 'McDonalds', 'total_price': '10.00'}

class FlaskTest(unittest.TestCase):

    # check if base url response is 200
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get("/")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    # check if content-type sent is application/json
    def test_process_receipts(self):
        tester = app.test_client(self)
        response = tester.post("/receipts/process", json=TEST_RECIEPT)
        self.assertEqual(response.content_type, "application/json")
        self.assertTrue(b'id' in response.data)
        response = tester.post("/receipts/process", json=INVALID_TEST_RECIEPT)
        self.assertTrue(b'Error' in response.data)
    
    def test_points_awarded(self):
        tester = app.test_client(self)
        id = str(uuid.uuid4())
        response = tester.get("/receipts/{id}/points")
        self.assertTrue(b'Error' in response.data)
        response = tester.post("/receipts/process", json=TEST_RECIEPT)
        decoded_string = response.data.decode('utf-8')
        response_id = json.loads(decoded_string)['id']
        response = tester.get("/receipts/" + response_id + "/points")
        decoded_string = response.data.decode('utf-8')
        data = json.loads(decoded_string)
        self.assertEqual(data['points'], 28)
        
    def test_retailer(self):
        self.assertEqual(retailer_points("Asmita"), 6)
        self.assertEqual(retailer_points("Target123"), 9)
        self.assertEqual(retailer_points("Target&&@"), 6)
    
    def test_total(self):
        self.assertEqual(total_points("10.00"), 75)
        self.assertEqual(total_points("10.25"), 25)
        self.assertEqual(total_points("10.78"), 0)
        
    def test_items(self):
        self.assertEqual(items_points(TEST_RECIEPT['items']), 10)
        self.assertEqual(items_points([]), 0)
    
    def test_description(self):
        self.assertEqual(description_points(TEST_RECIEPT['items']), 6)
        self.assertEqual(description_points([]), 0)
    
    def test_date(self):
        self.assertEqual(date_points("2022-01-01"), 6)
        self.assertEqual(date_points("2022-01-02"), 0)
        self.assertEqual(date_points("03-01-2022"), 0)
    
    def test_time(self):
        self.assertEqual(time_points("13:01"), 0)
        self.assertEqual(time_points("14:01"), 10)
        self.assertEqual(time_points("25:00"), 0)

if __name__ == "__main__":
    unittest.main()