from operator import mod
import os
from typing import Collection
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from main import app
from models import setup_db,Collection,Image,drop_and_create_all


ADMIN_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ijd6RW5qcWRrWjU3STc0WjFRSjZVZyJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtY291cnNlLmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MGNiZWQ3ZGI3MmE5ZjAwNmEyN2JjYjAiLCJhdWQiOiJldmVyeV9pbWFnZSIsImlhdCI6MTYyMzk3ODkzOSwiZXhwIjoxNjI0MDY1MzM5LCJhenAiOiJzTUE1cG4wNDFWd2doaUEwOHFrMWZWcUhEMlNhNGZwVSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmNvbGxlY3Rpb24iLCJkZWxldGU6aW1hZ2UiLCJwYXRjaDpjb2xsZWN0aW9uIiwicGF0Y2g6aW1hZ2UiLCJwb3N0OmNvbGxlY3Rpb24iLCJwb3N0OmltYWdlIl19.nA45rWFfSHe_F_Sw_T8jfIau1Fa1eC0QEuaoVVzNPC5Yz9Be8u9nvqpuk7uyr2oJCCW0l9jOCVlx2TY3rck7Tv02Lu7OiGfaQySSmwHKB7mFi0i71XDnXc8KMeCt_W7BYAdweTzZqDUjXUKmtIc72W5t_47QkAoCRicipfzwnam7P5XEXsCF3suSLrhcwdA7JiaLgGlbDQ3EYMVqjWb6jRjnKATnBCVEnZxWbFQTFfeYx9-PnEn7PTzs-UhZyFX02YOdNIZeIjgyT-Dem9D-0JYBfNJQC3fG8ezZ8gW0eegGnvFoxnQ4P4s233jUzyCV3WofjrFYF7qlI3oDPO5Wjw'

header_admin = {'Authorization':f'Bearer {ADMIN_TOKEN}'}
isNewTest =True;
class CapstoneTestCase(unittest.TestCase):

    isNewTest=True

    def setUp(self):
        self.app = app
        self.client = self.app.test_client
        self.database_name = "capstone_test"
        self.database_path = "postgresql://postgres:postgres@{}/{}".format('localhost:5432', self.database_name)
        

        setup_db(self.app, self.database_path,testing=True)
        
        
        if CapstoneTestCase.isNewTest: ## In here I want to reset the database when the first test is executed 
            CapstoneTestCase.isNewTest=False 
            drop_and_create_all()


    dummy_collection1 ={'title':'Beach',
                        'description':'photos of beaches'
                        }
    
    dummy_collection2 ={'title':'Skyscrapers',
                        'description':'photos of skyscrapers'
                        }

    dummy_image1 ={'title':'Fuji Mountain',
                        'image_link':'link to image'
                        }
    

    def tearDown(self):
        """Executed after reach test"""
        pass

    
    def test_get_collections_true(self):
        res  = self.client().get('/collections')

        data = res.get_json()

        self.assertEqual(res.status_code,200)
        self.assertTrue(type(data['collections'])== list)


    def test_get_specific_collection_true(self):
        res  = self.client().get('/collections/1')

        data = res.get_json()
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertEqual(data['collection']['id'],1)


    def test_get_specific_collection_false(self):
        res  = self.client().get('/collections/144')

        data = res.get_json()
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)



    def test_add_collection1_true(self):
        res = self.client().post('/collections',json=self.dummy_collection1, headers= header_admin)

        collection_db = Collection.query.filter_by(title=self.dummy_collection1['title']).first()
        print('added to db:',collection_db)

        self.assertEqual(res.status_code,200)
        self.assertEqual(res.get_json()['success'],True)    
        self.assertTrue(collection_db)


    

    def test_add_collection2_true(self):
        res = self.client().post('/collections',json=self.dummy_collection2, headers= header_admin)

        collection_db = Collection.query.filter_by(title=self.dummy_collection2['title']).first()

        print('added to db:',collection_db)

        self.assertEqual(res.status_code,200)
        self.assertEqual(res.get_json()['success'],True)    
        self.assertTrue(collection_db)



    def test_add_collection_false(self):
        res = self.client().post('/collections', headers= header_admin)
        self.assertEqual(res.status_code,422)
        self.assertEqual(res.get_json()['success'],False)  

    

    def test_edit_collection_true(self):
        res = self.client().patch('/collections/1',json={'title':'In The Jungle'}, headers= header_admin)

        collection_db = Collection.query.get(1)

        self.assertEqual(res.status_code,200)
        self.assertEqual(res.get_json()['success'],True)    
        self.assertEqual(collection_db.title,'In The Jungle')
    

    def test_edit_collection_false(self):
        res = self.client().patch('/collections/360',json={'title':'In The Forest'}, headers= header_admin)

        self.assertEqual(res.status_code,404)
        self.assertEqual(res.get_json()['success'],False)    


    def test_delete_collection_true(self):
        res = self.client().delete('/collections/2', headers= header_admin)
        collection_db = Collection.query.get(2)
        self.assertEqual(res.status_code,200)
        self.assertEqual(res.get_json()['success'],True)
        self.assertEqual(collection_db,None)   


    def test_delete_collection_false(self):
        res = self.client().delete('/collections/313', headers= header_admin)
       
        self.assertEqual(res.status_code,404)
        self.assertEqual(res.get_json()['success'],False)
           

    def test_get_all_images_true(self):
        res  = self.client().get('/images')

        data = res.get_json()

        self.assertEqual(res.status_code,200)
        self.assertEqual(res.get_json()['success'],True)
        self.assertTrue(type(data['images'])== list)


    def test_get_collection_images_true(self):
        res  = self.client().get('/collections/1/images')

        data = res.get_json()

        self.assertEqual(res.status_code,200)
        self.assertEqual(res.get_json()['success'],True)
        self.assertTrue(type(data['images'])== list)


    def test_get_collection_images_false(self):
        res  = self.client().get('/collections/144/images')

        self.assertEqual(res.status_code,404)
        self.assertEqual(res.get_json()['success'],False)


    def test_add_image_to_collection_true(self):
        res  = self.client().post('/collections/1/images',json=self.dummy_image1, headers= header_admin)
        img_db = Image.query.filter_by(title=self.dummy_image1['title']).first()
        self.assertEqual(res.status_code,200)
        self.assertEqual(res.get_json()['success'],True)
        self.assertTrue(img_db)


    def test_add_image_to_collection_false(self):
        res  = self.client().post('/collections/1/images',json={'title':'image with no link'}, headers= header_admin)
        self.assertEqual(res.status_code,422)
        self.assertEqual(res.get_json()['success'],False)


    def test_edit_image_true(self):
        res  = self.client().patch('images/1',json={'title':'something interesting'}, headers= header_admin)
        img_db = Image.query.get(1)
        self.assertEqual(res.status_code,200)
        self.assertEqual(res.get_json()['success'],True)
        self.assertEqual('something interesting',img_db.title)

    def test_edit_image_false(self):
        res  = self.client().patch('images/144',json={'title':'something interesting'}, headers= header_admin)
        self.assertEqual(res.status_code,404)
        self.assertEqual(res.get_json()['success'],False)


    def test_delete_image_True(self):
        res  = self.client().delete('images/2', headers= header_admin )
        img_db = Image.query.get(2)
        self.assertEqual(res.status_code,200)
        self.assertEqual(res.get_json()['success'],True)
        self.assertEqual(img_db,None)

    def test_delete_image_True(self):
        res  = self.client().delete('images/44', headers= header_admin)
        self.assertEqual(res.status_code,404)
        self.assertEqual(res.get_json()['success'],False)

    

    
################################## RBAC TEST ############################################
#
    

    
    
           




# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()