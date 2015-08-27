from flaskbb.extensions import db

def persist(item):
    db.session.add(item)
    db.session.commit()


def delete(item):
    db.session.delete(item)
    db.session.commit()
