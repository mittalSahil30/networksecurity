from pymongo.mongo_client import MongoClient

uri = "mongodb+srv://sahilmittal3003:T9HzHGgWqEbM8MFu@cluster0.tbtvtha.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)