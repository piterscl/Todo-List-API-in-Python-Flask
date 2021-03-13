from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    done = db.Column(db.String(100), nullable=False)
    label = db.Column(db.String(100), nullable=False)

    def serialize(self):
        return{
            "done": self.done,
            "label": self.label
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

