import unittest
from peewee import *
from playhouse.shortcuts import model_to_dict

from app import TimelinePost

MODELS = [TimelinePost]

# use an in-memory SQLite for tests
test_db = SqliteDatabase(':memory:')

class TestTimelinePost(unittest.TestCase):
    def setUp(self):
        # Bind model classes to test db. Since we have a complete list of 
        # all models, we do not need to revursively bind dependencies
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)

        test_db.connect()
        test_db.create_tables(MODELS)

    def tearDown(self):
        test_db.drop_tables(MODELS)

        # Close connection to db.
        test_db.close()
    
    def test_timeline_post(self):
        # Create 2 timeline posts
        first_post = TimelinePost.create(
            name='John Doe',
            email='john@example.com', 
            content='Hello world, I\'m John!')

        assert first_post.id == 1

        second_post = TimelinePost.create(
            name='Jane Doe',
            email='jane@example.com',
            content='Hello world, I\'m Jane!')

        assert second_post.id == 2

        # Get timeline posts and assert that they are correct
        posts = [model_to_dict(p) for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())]

        for post in posts:
            if post['id'] == 1:
                self.assertEqual(post['name'], 'John Doe')
                self.assertEqual(post['email'], 'john@example.com')
                self.assertEqual(post['content'], 'Hello world, I\'m John!')
            elif post['id'] == 2:
                self.assertEqual(post['name'], 'Jane Doe')
                self.assertEqual(post['email'], 'jane@example.com')
                self.assertEqual(post['content'], 'Hello world, I\'m Jane!')
