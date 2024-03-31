from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class DomainRank(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    domain_name = db.Column(db.String(255), unique=True, nullable=False)
    rank = db.Column(db.Integer, nullable=False)


    def __repr__(self):
        return f'<DomainRank {self.domain_name}: {self.rank}>'

