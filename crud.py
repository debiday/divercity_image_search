"""CRUD operations."""

from model import db, User, Collection, Picture, connect_to_db
from datetime import datetime

# <!--------------------------------------------------------------->
# <-- Routes for user -->
# <!--------------------------------------------------------------->
def create_user(email, password):
    """Create and return a new user."""

    new_user = User(email=email, password=password)

    db.session.add(new_user)
    db.session.commit()

    return new_user


def get_user_by_id(user_id):
    """Return a user by primary key."""

    return User.query.get(user_id)


def get_user_by_email(email):
    """Return a user by email."""

    return User.query.filter(User.email == email).first()


# <!--------------------------------------------------------------->
# <-- Routes for collections -->
# <!--------------------------------------------------------------->
def get_collections():
    """Return all collections."""

    return Collection.query.all()


def get_collection_by_id(collection_id):
    """Return a collection by primary key."""

    return Collection.query.get(collection_id)


def create_collection(user_id, notes, date_saved=datetime.today()):
    """Create and return a new collection."""

    new_collection = Collection(user_id=user_id, notes=notes, date_saved=date_saved)

    db.session.add(new_collection)
    db.session.commit()

    return new_collection


def get_collection_by_email(email):
    """Return all collections belonging to a user"""
    
    user_collection = Collection.query.join(User)

    return user_collection.filter(User.email == email).all()


#TODO: Create a get notes by collection function.
def get_city_by_collection(collection_id):
    """Get city name in notes with collection_id"""
    
    city = get_collection_by_id(collection_id)

    return city.notes



def delete_collection(collection_id):
    """Delete a collection object from the database."""

    collection_object = get_collection_by_id(collection_id)

    db.session.delete(collection_object)
    db.session.commit()

    return collection_object


# <!--------------------------------------------------------------->
# <-- Routes for pictures -->
# <!--------------------------------------------------------------->
def create_picture(collection_id, url):
    """Create and return a new picture."""

    new_picture = Picture(collection_id=collection_id, url=url)

    db.session.add(new_picture)
    db.session.commit()

    return new_picture


def get_pictures_by_collection(collection_id):
    """Return all pictures in collection."""

    collection_pictures = Picture.query.join(Collection)

    return collection_pictures.filter(Collection.collection_id == collection_id).all()


def get_first_image(collection_id):
    """Get the first image in the collection. """

    collection = get_pictures_by_collection(collection_id)
    first_image = collection[0]

    return first_image.url


def get_first_image_all_collections(email):
    """Get a dictionary of user collection and first image in each collection per user"""

    #get collection from user_id
    #get pictures from collection
    #get first picture from collection

    collections = get_collection_by_email(email)
    first_in_collection = {}

    for collection in collections:
        first_in_collection[collection] = get_first_image(collection.collection_id)

    return first_in_collection

    
if __name__ == '__main__':
    from server import app
    connect_to_db(app)
