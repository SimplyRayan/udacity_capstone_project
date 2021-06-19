
# EVERY IMAGE
##### This is an app that enables people to share pictures with others and classify pictures to collection of related pictures.


## Running the project

### THE SERVER IS UP AND RUNNING HERE: https://capstone-every-image.herokuapp.com/
#### But In case you wanted to run it locally you can follow these steps
##### first you might want to create a virtual environment, after that you can run the following:  

```
pip install -r requirements.txt
```
 
##### Running the server :  
 ````
$env:FLASK_APP="app"
flask run
 ````
 
## Docs

### Error Handling
##### Error are returned as JSON 
```
{'success':False,

'message':'bad request',

'code':400}
```

#####  Error types:
##### 1. 400 : BAD REQUEST
##### 2. 401 : UNATHOURIZED
#####  3. 403 : FORBIDDEN 
##### 4. 404: RESOURCES NOT FOUND
##### 5. 422:  UNPROCESSABLE REQUEST
##### 6. 500: INTERNAL SERVER ERROR


## ENDPOINTS
### GET /collections
##### returns all collections
#####  Request Body: None
#####  Request arguments : None
##### Request Sample : `curl --request GET 'http://127.0.0.1:5000/collections'`
##### Response Sample: 
```
{

"collections":  [
	{
		"description":  "interesting description",
		"id":  2,
		"images_count":  0,
		"title":  "My New Collection"
		}
	],
"success":  true
}
```

### GET /collections/{id}
##### returns the collection info with the requested id
#####  Request Body: None
#####  Request arguments : `id (required): id of the collection`
##### Request Sample : `curl --location --request GET 'http://127.0.0.1:5000/collections/2'`
##### Response Sample: 
```
{

"collection":  {
	"description":  "interesting description",
	"id":  2,
	"images_count":  0,
	"title":  "My New Collection"
	},
"success":  true
}  
```

### POST /collections

##### adding a collection 
##### Permission post:collection
##### (Required) Request Body Example: 
```
{
"title":"My New Collection",
"description":"interesting description"
}
```
#####  Request arguments : None
##### Request Sample : 
```
curl --location --request POST 'http://127.0.0.1:5000/collections' \
--header 'Content-Type: application/json' \
--data-raw '{
"title":"My New Collection",
"description":"interesting description"
}'
```

##### Response Sample: 
```
{
"collections":  {
"description":  "interesting description",
"id":  2,
"images_count":  0,
"title":  "My New Collection"
},
"success":  true
}
```

### PATCH /collections/{id}
##### editing the collection which has an id: {id}
##### Permission: patch:collection
#####  (optional keys) Request Body: 
```
{
"title":"updated title",
"description":"updated description"
}
```
#####  Request arguments : None
##### Request Sample :  
```
curl --location --request PATCH 'http://127.0.0.1:5000/collections/2' \
--header 'Content-Type: application/json' \
--data-raw '{
"title":"updated title",
"description":"updated"
}'
```
##### Response Sample: 
```
{
"collection":  {
	"description":  "updated",
	"id":  2,
	"images_count":  0,
	"title":  "updated title"
},
"success":  true
}
```



### DELETE /collections/{id}
##### delete the specified collection 
##### Permission: delete:collection
#####  Request Body: None
#####  Request arguments : None
##### Request Sample : `curl --location --request DELETE 'http://127.0.0.1:5000/collections/1'`
##### Response Sample: 
```
{
"success":  true
}
```


### GET /images
##### returns all images 
#####  Request Body: None
#####  Request arguments : None
##### Request Sample : `curl --location --request GET 'http://127.0.0.1:5000/images'`
##### Response Sample: 
```
{
"images":  [
	{
	"collection_title":  "updated title",
	"id":  1,
	"image_link":  "an image link",
	"title":  "cool picture"
	}
],
"success":  true
}
```

### GET /collections/{id}/images
##### returns all images that belong the collection with {id}
#####  Request Body: None
#####  Request arguments : `id (required): id of the collection`
##### Request Sample : `curl --location --request GET 'http://127.0.0.1:5000/collections/2/images'`
##### Response Sample: 
```
{
"description":  "updated",
"images":  [
	{
	"collection_title":  "random pictueres",
	"id":  1,
	"image_link":  "an image link",
	"title":  "cool picture"
	}
],
"success":  true,
"title":  "updated title"
}
```

### POST /collection/{id}/images
##### post an image to the collection with id {id}
##### Permission post:images
##### (Required) Request Body Example: 
```
{
"title":"cool picture",
"image_link":"an image link"
}
```
#####  Request arguments : None
##### Request Sample : 
```
curl --location --request POST 'http://127.0.0.1:5000//collections/2/images' \
--header 'Content-Type: application/json' \
--data-raw '{
"title":"cool picture",
"image_link":"an image link"
}'
```

##### Response Sample: 
```
{
"image":  {
	"collection_title":  "random pictures",
	"id":  1,
	"image_link":  "an image link",
	"title":  "cool picture"
	},
"success":  true
}
```


### PATCH /images/{id}
##### editing the collection which has an id: {id}
##### Permission: patch:image
#####  (optional keys) Request Body: 
```
{
"title":"updated title",
"image_link":"updated link"
}
```
#####  Request arguments : None
##### Request Sample :  
```
curl --location --request PATCH 'http://127.0.0.1:5000/images/1' \
--header 'Content-Type: application/json' \
--data-raw '{
"title":"updated title",
"image_link":"updated link"
}'
```
##### Response Sample: 
```
{

"image":  {
	"collection_title":  "updated title",
	"id":  1,
	"image_link":  "updated link",
	"title":  "new title"
	},
"success":  true
}
```

### DELETE /images/{id}
##### delete the specified image
##### Permission: delete:image
#####  Request Body: None
#####  Request arguments : None
##### Request Sample : `curl --location --request DELETE 'http://127.0.0.1:5000/images/1'`
##### Response Sample: 
```
{
"success":  true
}
```
## Testing 

### To Run test make sure to update the tokens in the file `test_app.py` so that tests that require authentication can be performed properly !
### After that you can simply run: `python test_app.py`


## References 
#### [Handling AuthError](https://stackoverflow.com/questions/53285452/internal-server-error-rather-than-raised-autherror-response-from-auth0) 
#### [Heroku Postgres plugin issues](https://stackoverflow.com/questions/66690321/flask-and-heroku-sqlalchemy-exc-nosuchmoduleerror-cant-load-plugin-sqlalchemy)
