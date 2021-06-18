from logging import Formatter
from werkzeug.exceptions import HTTPException

from flask import Flask, json,jsonify,request,abort
from models import db,setup_db,Collection,Image
from flask_cors import CORS

from auth import AuthError,requires_auth
import sys
import os

app =Flask(__name__)
CORS(app)
setup_db(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})  # Gotta check this later?

URL="NONE"
if 'DATABASE_URL' in os.environ:
    URL =os.environ['DATABASE_URL']
@app.route('/')
def index():
    return jsonify({
        'message':'Hello',
        'DATABASE_URL':URL
    })


# @app.route('/collections')
# def get_collections():
#     try:
#         collections = Collection.query.all()
#         formatted_collections = []
        
#         for collection in collections:
#             formatted_collections.append(collection.format())

#         return jsonify({
#             'success':True,
#             'collections':formatted_collections
#         })
#     except Exception:
#         print("ERROR",sys.exc_info())
#         abort(422)


# @app.route('/collections/<int:id>')
# def get_specific_collection(id):
#     try:
#         collection = Collection.query.get(id)
#         if collection == None:
#             abort(404)

#         return jsonify({
#             'success':True,
#             'collection':collection.format()
#         })
#     except Exception as e:
#         if isinstance(e, HTTPException):
#             abort(e.code)

#         print(sys.exc_info())
#         abort(422)




# @app.route('/collections',methods=['POST'])
# @requires_auth(permission="post:collection")
# def add_collection():
#     try:
#         data = request.get_json()

#         newCollection = Collection(title=data['title'],description=data['description'])
#         newCollection.insert()

#         return jsonify({
#             'success':True,
#             'collections':newCollection.format()
#         })

#     except Exception:
#         print('ERROR',sys.exc_info())
#         abort(422)
    
    
        


# @app.route('/collections/<int:id>',methods=['PATCH'])
# @requires_auth(permission="patch:collection")
# def edit_collection(id):
#     try:

#         collection = Collection.query.get(id)
#         if collection == None:
#             print('NO COLLECTION FOUND TO PATCH')
#             abort(404)

#         data = request.get_json()

#         if 'title' in data:
#             collection.title =  data['title']
        
#         if 'description' in data:
#             collection.description =  data['description']
        
#         collection.update()
        
#         print('patched!',collection.title)
#         result =  jsonify({
#             'success':True,
#             'collection':collection.format()
#         })

#     except Exception as e:
#         print('errror in patching',sys.exc_info())
#         db.session.rollback()
#         db.session.close()
#         if isinstance(e, HTTPException):
#             abort(e.code)
#         abort(422)
#     finally:
#         db.session.close()

#     return result;



# @app.route('/collections/<int:id>',methods=['DELETE'])
# @requires_auth(permission="delete:collection")
# def delete_collection(id):
#     try:

#         collection = Collection.query.get(id)
#         if collection == None:
#             abort(404)

#         collection.delete()
#         print('deleted!')
#         print(Collection.query.all())
#         result =  jsonify({
#             'success':True,
#         })
#     except Exception as e:
#         if isinstance(e, HTTPException):
#             abort(e.code)
#         print("ERROR",sys.exc_info())
#         db.session.rollback()
#         db.session.close()
#         abort(422)

#     finally:
#         db.session.close()

#     return result

# # <<<<<<<<<<<<<<<<<<<<<<<<<<< Image Routes >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


# @app.route('/images')
# def get_images():
#     try:
#         images = Image.query.all()

#         formatted_images=[]

#         for image in images:
#             formatted_images.append(image.format())

#         return jsonify({
#             'success':True,
#             'images':formatted_images
#         })
#     except Exception as e:
#         if isinstance(e, HTTPException):
#             abort(e.code)
        
#         print(sys.exc_info())
#         abort(422)





# @app.route('/collections/<int:id>/images')
# def get_colleciton_images(id):
#     try:

#         collection = Collection.query.get(id)
#         if collection == None:
#             abort(404)

#         formatted_images=[]
#         for image in collection.images:
#             formatted_images.append(image.format())

#         return jsonify({
#             'success':True,
#             'title':collection.title,
#             'description':collection.description,
#             'images':formatted_images
#         })
#     except Exception as e:
#         if isinstance(e, HTTPException):
#             abort(e.code)
        
#         print(sys.exc_info())
#         abort(422)





# @app.route('/collections/<int:id>/images',methods=['POST'])
# @requires_auth(permission="post:image")
# def add_colleciton_images(id):
#     try:

#         collection = Collection.query.get(id)
#         if collection == None:
#             abort(404)
        
#         data = request.get_json()

#         newImage = Image(title=data['title'],image_link=data['image_link'])

#         collection.images.append(newImage)
#         db.session.add(collection)
#         db.session.commit()

#         return jsonify({
#             'success':True,
#             'image':newImage.format()
#         })
#     except Exception as e:
#         if isinstance(e, HTTPException):
#             abort(e.code)
    
#         print(sys.exc_info())
#         db.session.rollback()
#         db.session.close()
#         abort(422)





# @app.route('/images/<int:id>',methods=['PATCH'])
# @requires_auth(permission="patch:image")
# def edit_image(id):
#     try:

#         image = Image.query.get(id)
#         if image == None:
#             abort(404)
        
#         data = request.get_json()
    
#         print(image)
#         if 'title' in data:
#             image.title =  data['title']
        
#         if 'image_link' in data:
#             image.image_link =  data['image_link']
        
#         db.session.commit()

#         return jsonify({
#             'success':True,
#             'image':image.format()
#         })
#     except Exception as e:
#         if isinstance(e, HTTPException):
#             abort(e.code)
    
#         print(sys.exc_info())
#         db.session.rollback()
#         db.session.close()
#         abort(422)



# @app.route('/images/<int:id>',methods=['DELETE'])
# @requires_auth(permission="delete:image")
# def delete_image(id):
#     try:

#         image = Image.query.get(id)
#         if image == None:
#             abort(404)

#         db.session.delete(image)
#         db.session.commit()

#         return jsonify({
#             'success':True,
#         })
#     except Exception as e:
#         if isinstance(e, HTTPException):
#             abort(e.code)
    
#         print(sys.exc_info())
#         db.session.rollback()
#         db.session.close()
#         abort(422)




@app.errorhandler(404)
def handle_404_error(error):
    return jsonify({
        'success':False,
        'code':'404',
        'message':'requested resources could not be found'
    }),404



@app.errorhandler(422)
def handle_404_error(error):
    return jsonify({
        'success':False,
        'code':'422',
        'message':'Unprocessable'
    }),422


@app.errorhandler(400)
def handle_404_error(error):
    return jsonify({
        'success':False,
        'code':'400',
        'message':'BAD REQUEST'
    }),400



# @app.errorhandler(AuthError)
# def handle_auth_error(exception):
#     return jsonify(exception.error), exception.status_code




if __name__ =='__main__': 
    app.run(debug=True)