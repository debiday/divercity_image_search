"""CRUD operations."""

from model import db, User, Collection, Picture, connect_to_db
from datetime import datetime


def create_user(email, password):
    """Create and return a new user."""

    new_user = User(email=email, password=password)

    db.session.add(new_user)
    db.session.commit()

    return new_user

# def create_collection():
#     """Create and return a collection"""


def get_user_by_id(user_id):
    """Return a user by primary key."""

    return User.query.get(user_id)


def get_user_by_email(email):
    """Return a user by email."""

    return User.query.filter(User.email == email).first()


def get_collections():
    """Return all collections."""

    return Collection.query.all()


def get_collection_by_id(collection_id):
    """Return a collection by primary key."""

    return Collection.query.get(collection_id)


def create_collection(user_id, notes, date_saved=datetime.today()):
    """Create and return a new rating."""

    new_collection = Collection(user_id=user_id, notes=notes, date_saved=date_saved)

    db.session.add(new_collection)
    db.session.commit()

    return new_collection

def create_picture(collection_id, url):
    """Create and return a new picture."""

    new_picture = Picture(collection_id=collection_id, url=url)

    db.session.add(new_picture)
    db.session.commit()

    return new_picture


def get_collection_by_email(email):
    """Return all collections belonging to a user"""
    
    user_collection = Collection.query.join(User)

    return user_collection.filter(User.email == email).all()

# TODO: Fix this function
def get_pictures_by_collection():
    """Return all pictures in collection."""

    return Pictures.query.all()




# def get_user_id_by_email(email):
#     """Return a user id by email."""

#     user_query = Tracking.query.join(User)

#     return user_query.filter(User.email == email).all()

# <-----Test CRUD Functions----->
# def get_photos(image_tag):
#     extras = ','.join(SIZES)
#     flickr = FlickrAPI(KEY, SECRET)
#     photos = flickr.walk(text=image_tag,  # it will search by image title and image tags
#                             extras=extras,  # get the urls for each size we want
#                             privacy_filter=1,  # search only for public photos
#                             per_page=50,
#                             sort='relevance')  # we want what we are looking for to appear first
#     return photos


# def get_url(photo):
#     for i in range(len(SIZES)):  # makes sure the loop is done in the order we want
#         url = photo.get(SIZES[i])
#         if url:  # if url is None try with the next size
#             return url


# def get_urls(image_tag, max):
#     photos = get_photos(image_tag)
#     counter=0
#     urls=[]

#     for photo in photos:
#         if counter < max:
#             url = get_url(photo)  # get preffered size url
#             if url:
#                 urls.append(url)
#                 counter += 1
#             # if no url for the desired sizes then try with the next photo
#         else:
#             break

#     return urls


if __name__ == '__main__':
    from server import app
    connect_to_db(app)
