from botFlask import db

user_to_category = db.Table("association", db.Model.metadata,
    db.Column("category_id", db.String, db.ForeignKey("categories.id")),
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"))
)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.SmallInteger, default=0)

    categories = db.relationship("Category", secondary=user_to_category,
                                 back_populates="user")

    def __repr__(self):
        return "<User id={}, position={}>".format(self.id, self.position)


class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    index = db.Column(db.SmallInteger)
    name = db.Column(db.String, nullable=False)
    points = db.Column(db.Numeric, default=0)

    user = db.relationship("User", secondary=user_to_category,
                           back_populates="categories")

    history = db.relationship("HistoryItem", back_populates="category")


class HistoryItem(db.Model):
    __tablename__ = "history"
    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.SmallInteger)
    points = db.Column(db.Numeric, default=0)

    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
    category = db.relationship("Category", back_populates="history")
