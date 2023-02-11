import csv 
import json
import time

def csv_to_json(csvFilePath, jsonFilePath):
    jsonArray = []
      
    #read csv file
    with open(csvFilePath, encoding='utf-8') as csvf: 
        #load csv file data using csv library's dictionary reader
        csvReader = csv.DictReader(csvf) 

        #convert each csv row into python dict
        for row in csvReader: 
            #add this python dict to json array
            jsonArray.append(row)
  
    #convert python jsonArray to JSON String and write to file
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf: 
        jsonString = json.dumps(jsonArray, indent=4)
        jsonf.write(jsonString)

csv_to_json('seller_phone_money.csv', 'seller.json')
csv_to_json('category.csv', 'category.json')
csv_to_json('food_no_id.csv', 'food.json')
csv_to_json('account.csv', 'account.json')
csv_to_json('group_detail.csv', 'group_detail.json')