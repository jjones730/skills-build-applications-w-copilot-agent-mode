from django.core.management.base import BaseCommand
from pymongo import MongoClient
from bson import ObjectId
import pymongo

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        # Connect to MongoDB
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']

        # Clear existing data
        self.stdout.write('Clearing existing collections...')
        collections = ['activities', 'leaderboard', 'users', 'teams', 'workouts']
        for collection in collections:
            db[collection].delete_many({})

        # Create indexes
        self.stdout.write('Creating indexes...')
        db.teams.create_index('name', unique=True)
        db.users.create_index('email', unique=True)

        # Create teams
        self.stdout.write('Creating teams...')
        marvel_id = db.teams.insert_one({
            'name': 'Marvel'
        }).inserted_id

        dc_id = db.teams.insert_one({
            'name': 'DC'
        }).inserted_id

        # Create users
        self.stdout.write('Creating users...')
        users = [
            {
                'name': 'Spider-Man',
                'email': 'spiderman@marvel.com',
                'team_id': marvel_id
            },
            {
                'name': 'Iron Man',
                'email': 'ironman@marvel.com',
                'team_id': marvel_id
            },
            {
                'name': 'Wonder Woman',
                'email': 'wonderwoman@dc.com',
                'team_id': dc_id
            },
            {
                'name': 'Batman',
                'email': 'batman@dc.com',
                'team_id': dc_id
            }
        ]

        user_ids = []
        for user in users:
            result = db.users.insert_one(user)
            user_ids.append(result.inserted_id)

        # Create activities
        self.stdout.write('Creating activities...')
        activities = [
            {'user_id': user_ids[0], 'type': 'Running', 'duration': 30},
            {'user_id': user_ids[1], 'type': 'Cycling', 'duration': 45},
            {'user_id': user_ids[2], 'type': 'Swimming', 'duration': 60},
            {'user_id': user_ids[3], 'type': 'Yoga', 'duration': 20}
        ]

        db.activities.insert_many(activities)

        # Create workouts
        self.stdout.write('Creating workouts...')
        workouts = [
            {
                'name': 'Hero HIIT',
                'description': 'High intensity for heroes',
                'suggested_for': 'Marvel'
            },
            {
                'name': 'Power Yoga',
                'description': 'Strength and flexibility',
                'suggested_for': 'DC'
            }
        ]

        db.workouts.insert_many(workouts)

        # Create leaderboard
        self.stdout.write('Creating leaderboard entries...')
        leaderboard = [
            {'user_id': user_ids[0], 'points': 100},
            {'user_id': user_ids[1], 'points': 90},
            {'user_id': user_ids[2], 'points': 95},
            {'user_id': user_ids[3], 'points': 85}
        ]

        db.leaderboard.insert_many(leaderboard)

        # Verify data
        self.stdout.write('\nVerifying data population...')
        for collection in collections:
            count = db[collection].count_documents({})
            self.stdout.write(f'- {collection}: {count} documents')

        # Show sample documents
        self.stdout.write('\nSample documents from each collection:')
        for collection in collections:
            sample = db[collection].find_one({})
            self.stdout.write(f'\n{collection}:')
            self.stdout.write(str(sample))

        self.stdout.write(self.style.SUCCESS('\nTest data populated successfully!'))
