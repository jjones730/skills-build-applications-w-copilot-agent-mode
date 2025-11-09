from pymongo import MongoClient
from bson import ObjectId

# Connect to MongoDB
client = MongoClient('localhost', 27017)
db = client['octofit_db']

# Collection definitions
teams = db['teams']
users = db['users']
activities = db['activities']
workouts = db['workouts']
leaderboard = db['leaderboard']

# Example document structures
team_structure = {
    'name': str  # unique
}

user_structure = {
    'name': str,
    'email': str,  # unique
    'team_id': ObjectId
}

activity_structure = {
    'user_id': ObjectId,
    'type': str,
    'duration': int
}

workout_structure = {
    'name': str,
    'description': str,
    'suggested_for': str
}

leaderboard_structure = {
    'user_id': ObjectId,
    'points': int
}
