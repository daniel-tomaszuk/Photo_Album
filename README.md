# Photo_Album
Photo Album web-service.

To acces service you need to log as user - try creating your own account. Main page shows all photos in the DB, number of each photo likes. It is possible to like or dislike a photo (if it was already liked by user). When clicked on a photo, service shows details of the photo - date of creation, who added it. Photo information site shows all comments and allows adding your own comment. You can add new photos by inserting link to the photo that is hosted in 
external server or putting photo file in the Photo Album server ("Browse.." button).

Default localhost:8000 urls:

- /admin - admin service page, to use create superuser first: ./manage.py createsuperuser
- / - main page of service, avalible only after loging in
- /login - page for loggng in, avalible only after loging in
- /logout - allows logging out, avalible only after loging in
- /add_user - displays form for adding new user, avalible only after loging in
- /add_photo - displays form for adding new photo, avalible only after loging in
- /user_info - displays details about logged user
- /user_update/{pk} (POST with form only) - takes data from form and updates user (with PK=pk) info
- /photo_info/{photo_id} - shows details abot photo with PK = photo_id

