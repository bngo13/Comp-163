from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')

db = client['HealthCare']

collection = db['patients']

patient_data_1 = {
    "name": "Bob",
    "age": 23,
    "gender": "Male",
    "contact_information": {
        "phone": "111-222-3333",
        "email": "bob@email.com"
    },
    "physician_visits": [
        {
            "visit_date": "2022-04-01",
            "physician_name": "Dr. Smith",
            "reason_for_visit": "Annual check-up",
            "treatment": "No specific treatment required"
        }
    ]
}

patient_data_2 = {
    "name": "Alice",
    "age": 20,
    "gender": "Female",
    "contact_information": {
        "phone": "222-111-3333",
        "email": "alice@email.com"
    },
    "physician_visits": [
        {
            "visit_date": "2022-04-01",
            "physician_name": "Dr. Jane",
            "reason_for_visit": "Semi-Annual check-up",
            "treatment": "She's gone."
        }
    ]
}

result = collection.insert_one(patient_data_1)
result = collection.insert_one(patient_data_2)

# Find a document in the collection
query = {"name": "Bob"}
patient = collection.find_one(query)
print("Found patient:", patient)

query = {"name": "Alice"}
patient = collection.find_one(query)
print("Found patient: ", patient)

exit()

# Update a document in the collection
update_query = {"brand": "Trek"}
new_values = {"$set": {"price": 750}}
collection.update_one(update_query, new_values)
print("Updated bike price")

# Find all documents in the collection
all_bikes = collection.find()
print("All bikes in the collection:")
for bike in all_bikes:
    print(bike)

# Delete a document from the collection
#delete_query = {"brand": "Trek"}
#collection.delete_one(delete_query)
#print("Deleted bike")

# Drop the entire collection (use with caution)
# collection.drop()

# Close the connection to MongoDB
client.close()
