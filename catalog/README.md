# FSND-catalog
FSND - Project 4 Catalog.

## Summary
This web app will display movie genres. This acts as the items.
When the user clicks on the genre(item) it will display movies 
within the genre. When the user clicks on that movie, it will 
display more information about the movie.

The user will also have the option to sign in. The user will need to
have a facebook account. The web application uses facebook authentication.

Once the user signed in a signout button will be displayed. 
when the user signs out genric public pages will be displayed for genres,
movies, and individual movies. 

When the user signs in the user will be presented with the ability to 
edit, delete, and create new. This ability is applicable to genres and
movies.


## Requirements
```
* vagrant VM
* python 2.7
* flask
* httplib2
* facebook account
```

## How to

If you want run this locally.
Used VSCode to code. Need to virtualenv to set up a python 2.7 env.
```
py -2 -m virtualenv env
```
Activate the env using: 
```
.\env\Scripts\activate - for windows.
or 
.\env\bin\activate - for linux.
```
Please have vagrant set up. This repo already has a vagrant file to use. 
This file is copied from what Udacity originally provided.
run the following command 

```
vagrant up
vagrant ssh
cd /vagrant
```
If the files from this repo are not found in '/vagrant' dir, 
try to cd into catalog after /vagrant.  

1. run database_setup.py - Creates a database.
```
python database_setup.py
```
2. run populatedatabase.py - this will populate the database, so that the applicaiton can display information.
```
python populatedatabase.py
```

Once you are there run: 
```
python application
```

when this runs - open a browser and type in: 
```
localhost:8000/genres
```
you should see a list of genres with login option. 
This will show the user a facebook button to login.
Once the user logs in they will be rerouted to the homepage, which is 
the genres page. THey will now have the ability to edit, delete, and add new.
This functionailty will also be availble on the movies page and 
individual movie page.

### Authentication
fb_client_secret.json:   
This contains Key and secret from my application in facebook.  
Google+ auth is not used google+ is not longer in use.  
Not using google auth either. 


### CRUD
Edit/update page:   
Click on the edit link - you will be routed to a page where
you can edit the genre title or a movie title or the description dependening on 
which page you are on.

Delete:   
Once the use logs in they can delete an item.
if clicked the user is confronted with a confirmation page.
If agreed - the database will udpate and the item will be deleted.

Add New:   
if the user is logged in they will have the ability to add new items.
click on add new.
if you are in the genres page. add a new genre.
if you are in the movies section under genres. you can add a new movie.
The user will have the option to add movie name, description, and year.
This will update the database. 

Read:   
Each items is read from the database.
list of genre is read from the database. 
when you click the genres it uses the genre_id  and list all movies under that.
when you click on the movei it uses genre_id and movie_id to read 
description, title, and year for that specific movie.

### JSON Endpoints
* localhost:8000/genres/json - will show all genres in json format.
* localhost:8000/movies/josn - shows all movies in json format.
* localhost:8000/genres/<int:genre_id>/movies/josn - prints movies in a specific genres in json form.
* localhost:8000/genres/<int:genre_id>/movies/<int:movies_id>/json - shows a speicific movie details in json format.

genre_id and movie_ids can be obtained by running the first two. 
Subsitute those values in.


## Resources: 
<strong>Movies</strong>  
* action: www.imdb.com/list/ls027328830
* Thriller: https://www.imdb.com/search/title?genres=thriller&groups=top_250&sort=user_rating,desc&ref_=adv_prv
* Classic: https://www.imdb.com/list/ls000183548/
* Comedy: https://www.imdb.com/search/title?genres=comedy&groups=top_250&sort=user_rating&title_type=feature
* Drama: https://www.imdb.com/list/ls009668711/
* Horror: https://www.imdb.com



