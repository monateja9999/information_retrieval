from weaviate import Client
import json

# Initialize the Weaviate client
client = Client("http://localhost:8080")

# Check if the class exists before trying to delete it
try:
    client.schema.delete_class("SimSearch")
except Exception as e:
    print(f"Class 'SimSearch' does not exist or cannot be deleted: {e}")

# Define the schema for the class
class_obj = {
    "class": "SimSearch",
    "vectorizer": "text2vec-transformers"
}
client.schema.create_class(class_obj)

# Load JSON data from local server
import requests
url = 'http://localhost:8000/data.json'
resp = requests.get(url)
data = json.loads(resp.text)

# Batch upload the data to the client
with client.batch as batch:
    batch.batch_size = 100  # Set batch size for efficient upload
    for i, d in enumerate(data):
        print(f"\nImporting datum: {i}")  # Log the current datum being imported
        
        # Extract properties from each datum
        properties = {
            "school": d.get("School", ""),           # School name
            "course_name": d.get("CourseName", ""),  # Course name
            "course_desc": d.get("CourseDesc", ""),  # Course description
        }
        
        # Print the properties to verify the data before upload
        print(f"Properties: {properties}")
        
        # Add the properties as a data object to the batch
        client.batch.add_data_object(properties, "SimSearch")


