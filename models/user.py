from db import db
class UserProfile(db.Model):
    __tablename__ = 'userprofiles'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    isadmin = db.Column(db.Boolean())
    no_of_posts = db.Column(db.Integer)
    posts = db.relationship('UserPosts',backref = 'user',lazy = True)
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls,name):
        return cls.query.filter_by(username = name).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

class UserPosts(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer(), primary_key=True)
    user_name = db.Column(db.String(80))
    victim_name = db.Column(db.String(80))
    home_town = db.Column(db.String(80))
    OutingNo = db.Column(db.Integer)
    RatioOut = db.Column(db.Integer)
    RatioIn = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('userprofiles.id'), nullable=False)


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()




