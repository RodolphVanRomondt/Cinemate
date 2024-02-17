from models import db, List
from app import g


IMAGE_DEFAULT = "https://motivatevalmorgan.com/wp-content/uploads/2016/06/default-movie.jpg"


def add_remove_list(imdbID, user_list):

    list = [movie.movie_id for movie in user_list]

    if imdbID not in list:
        list = List(user_id=g.user.id, movie_id=imdbID)

        db.session.add(list)
    
    else:
        List.query.filter(List.movie_id == imdbID).delete()

    db.session.commit()