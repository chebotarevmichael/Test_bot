from botFlask import db


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.SmallInteger)
    category_index = db.Column(db.SmallInteger)

    categories = db.relationship("Category", back_populates="user")

    def __init__(self, user_id, **kwargs):
        super().__init__(id=user_id, **kwargs)
        self.position = 0
        self.category_index = 0

    def __repr__(self):
        return "<User(id={}, categores={}) cat. #{}, quest. #{}>".format(
            self.id, self.categories, self.category_index, self.position)


class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    index = db.Column(db.SmallInteger)
    name = db.Column(db.String, nullable=False)
    points = db.Column(db.Float)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User", back_populates="categories", uselist=False)

    history = db.relationship("HistoryItem", back_populates="category")

    def __init__(self, index, name, user, **kwargs):
        super().__init__(index=index, name=name, user=user, **kwargs)
        self.points = 0

    def __repr__(self):
        return "<Category(user_id={}, index={}, name={}, points={})>".format(
            self.user_id, self.index, self.name, self.points)


class HistoryItem(db.Model):
    __tablename__ = "history"
    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.SmallInteger)
    points = db.Column(db.Float)

    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
    category = db.relationship("Category", back_populates="history", uselist=False)

    def __repr__(self):
        return "<HistoryItem(category={}, position={}, points={})>".format(
            self.category, self.position, self.points)
