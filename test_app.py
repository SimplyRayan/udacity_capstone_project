from operator import mod
import os
from typing import Collection
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from main import app
from models import setup_db, Collection, Image, drop_and_create_all


ADMIN_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ijd6RW5qcWRrWjU3STc0WjFRSjZVZyJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtY291cnNlLmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MGNiZWQ3ZGI3MmE5ZjAwNmEyN2JjYjAiLCJhdWQiOiJldmVyeV9pbWFnZSIsImlhdCI6MTYyNDA2Mzg2MywiZXhwIjoxNjI0MTUwMjYzLCJhenAiOiJzTUE1cG4wNDFWd2doaUEwOHFrMWZWcUhEMlNhNGZwVSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmNvbGxlY3Rpb24iLCJkZWxldGU6aW1hZ2UiLCJwYXRjaDpjb2xsZWN0aW9uIiwicGF0Y2g6aW1hZ2UiLCJwb3N0OmNvbGxlY3Rpb24iLCJwb3N0OmltYWdlIl19.mDKsyMDvhReCX4KQtHpSrPkldEISVRhPnpCYhF5F2Qwoof2N5MNz7WtTa4HQvJ-Za5832cxuETIv6K3_L74dJjEToAUpnTEBwkHCodnbHQo26xWUi2N0alyIJApu2QjdJaqO9aRuiw7daqinOSDSs-ci91AFQIdFRhHhgTDrP8qeRvgChunMznNpSeSONRZM4M37O1WrgyydsTL4d1cDBtINpl-1_JPJ1hSXRyWSeeUA48TStPbIarexSmPIlO4JudbLZjXIPiJlNNv_INOEwtGTRE44g1JKgLUwN94UUlBTaOZcm2u8ZPO8CA2ieDhCoyM1KFtVtGUddN8cnfU-Aw'

AUTHENTICATED_USER_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ijd6RW5qcWRrWjU3STc0WjFRSjZVZyJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtY291cnNlLmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MGNjMjJmNmFkZTExNDAwNzE0NWQ4YWQiLCJhdWQiOiJldmVyeV9pbWFnZSIsImlhdCI6MTYyNDA2MzkyMywiZXhwIjoxNjI0MTUwMzIzLCJhenAiOiJzTUE1cG4wNDFWd2doaUEwOHFrMWZWcUhEMlNhNGZwVSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsicG9zdDpjb2xsZWN0aW9uIiwicG9zdDppbWFnZSJdfQ.olLG42lh8Kh7JPO-CN1mMyYD5aWMjB-lbwfRtnwZilu9M494xiPyxJsCYlGPrtgvOEcmW93T8Vy_4v-ccrdCZgaDuVuz9Llnh56mUOjgRMoBH_9x_2jAAwSjBrMw5XmJqv8HsQka_88L-kgHBZu4_zK_UPkYI8OLc5C7_mwzyPBN8vyHNT89xaB31-d_O_3MBb9igib9g_hBIWoN_fq0qf1RbhUJyxMqko_2MyAa19dKYAcHkiw5XHeUa-Z4yH6iG-ZEpqjCDkazxa6tdBNYlMKcIM2EbxPcay7mR7Lf16jkWIEIJePKMtmBoN0o-og-440H4E5Ed7TXnWSUSvm3gQ'

admin_header = {'Authorization': f'Bearer {ADMIN_TOKEN}'}
authenticated_user_header = {
    'Authorization': f'Bearer {AUTHENTICATED_USER_TOKEN}'}


class CapstoneTestCase(unittest.TestCase):

    isNewTest = True

    def setUp(self):
        self.app = app
        self.client = self.app.test_client
        self.database_name = "capstone_test"
        self.database_path = "postgresql://postgres:postgres@{}/{}".format(
            'localhost:5432', self.database_name)

        setup_db(self.app, self.database_path, testing=True)

        if CapstoneTestCase.isNewTest:  # In here I want to reset the database when the first test is executed
            CapstoneTestCase.isNewTest = False
            drop_and_create_all()

    dummy_collection1 = {'title': 'Beach',
                         'description': 'photos of beaches'
                         }

    dummy_collection2 = {'title': 'Skyscrapers',
                         'description': 'photos of skyscrapers'
                         }

    dummy_image1 = {'title': 'Fuji Mountain',
                    'image_link': 'link to image'
                    }

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_collections_true(self):
        res = self.client().get('/collections')

        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(type(data['collections']) == list)

    def test_get_specific_collection_true(self):
        res = self.client().get('/collections/1')

        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['collection']['id'], 1)

    def test_get_specific_collection_false(self):
        res = self.client().get('/collections/144')

        data = res.get_json()
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_add_collection1_true(self):
        res = self.client().post(
            '/collections', json=self.dummy_collection1, headers=admin_header)

        collection_db = Collection.query.filter_by(
            title=self.dummy_collection1['title']).first()
        print('added to db:', collection_db)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()['success'], True)
        self.assertTrue(collection_db)

    def test_add_collection2_true(self):
        res = self.client().post(
            '/collections', json=self.dummy_collection2, headers=admin_header)

        collection_db = Collection.query.filter_by(
            title=self.dummy_collection2['title']).first()

        print('added to db:', collection_db)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()['success'], True)
        self.assertTrue(collection_db)

    def test_add_collection_false(self):
        res = self.client().post('/collections', headers=admin_header)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(res.get_json()['success'], False)

    def test_edit_collection_true(self):
        res = self.client().patch('/collections/1',
                                  json={'title': 'In The Jungle'}, headers=admin_header)

        collection_db = Collection.query.get(1)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()['success'], True)
        self.assertEqual(collection_db.title, 'In The Jungle')

    def test_edit_collection_false(self):
        res = self.client().patch('/collections/360',
                                  json={'title': 'In The Forest'}, headers=admin_header)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.get_json()['success'], False)

    def test_delete_collection_true(self):
        res = self.client().delete('/collections/2', headers=admin_header)
        collection_db = Collection.query.get(2)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()['success'], True)
        self.assertEqual(collection_db, None)

    def test_delete_collection_false(self):
        res = self.client().delete('/collections/313', headers=admin_header)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.get_json()['success'], False)

    def test_get_all_images_true(self):
        res = self.client().get('/images')

        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()['success'], True)
        self.assertTrue(type(data['images']) == list)

    def test_get_collection_images_true(self):
        res = self.client().get('/collections/1/images')

        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()['success'], True)
        self.assertTrue(type(data['images']) == list)

    def test_get_collection_images_false(self):
        res = self.client().get('/collections/144/images')

        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.get_json()['success'], False)

    def test_add_image_to_collection_true(self):
        res = self.client().post('/collections/1/images',
                                 json=self.dummy_image1, headers=admin_header)
        img_db = Image.query.filter_by(
            title=self.dummy_image1['title']).first()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()['success'], True)
        self.assertTrue(img_db)

    def test_add_image_to_collection_false(self):
        res = self.client().post('/collections/1/images',
                                 json={'title': 'image with no link'}, headers=admin_header)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(res.get_json()['success'], False)

    def test_edit_image_true(self):
        res = self.client().patch(
            'images/1', json={'title': 'something interesting'}, headers=admin_header)
        img_db = Image.query.get(1)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()['success'], True)
        self.assertEqual('something interesting', img_db.title)

    def test_edit_image_false(self):
        res = self.client().patch(
            'images/144', json={'title': 'something interesting'}, headers=admin_header)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.get_json()['success'], False)

    def test_delete_image_True(self):
        res = self.client().delete('images/2', headers=admin_header)
        img_db = Image.query.get(2)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()['success'], True)
        self.assertEqual(img_db, None)

    def test_delete_image_True(self):
        res = self.client().delete('images/44', headers=admin_header)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.get_json()['success'], False)


################################## RBAC TEST ############################################


######### ADMIN Role ##########


    def test_edit_collection_as_admin_true(self):
        res = self.client().patch('/collections/1',
                                  json={'title': 'test_collection'}, headers=admin_header)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()['success'], True)

    def test_edit_collection_as_admin_false(self):
        res = self.client().patch('/collections/1',
                                  json={'description': 'test_collection description'})
        self.assertEqual(res.status_code, 401)


######### authenticated User Role ##########


    def test_add_collection_as_authenticated_user_true(self):
        res = self.client().post('/collections',
                                 json={'title': 'zebras', 'description': 'zebras!!'}, headers=authenticated_user_header)

        collection_db = Collection.query.filter_by(
            title=self.dummy_collection1['title']).first()
        print('added to db:', collection_db)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()['success'], True)
        self.assertTrue(collection_db)

    # this should fail because the user has no permsission to delete stuff
    def test_delete_collection_as_authenticated_user_false(self):
        res = self.client().delete('/collections/1', headers=authenticated_user_header)

        self.assertEqual(res.status_code, 403)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
