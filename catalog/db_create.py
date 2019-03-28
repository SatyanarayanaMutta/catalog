# Required modules are imported

import sys
import os
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

# Class-3 for Users


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))
    # JSON format data for users table

    @property
    def serialize(self):
        return{
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'picture': self.picture
            }

# Class -1 [branch table]


class Branch(Base):
    __tablename__ = "branch"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    user_id = Column(
        Integer,
        ForeignKey('users.id'))
    user = relationship(User, backref="category")

    # JSON format data for branch table

    @property
    def serialize(self):
        return {
            'name': self.name,
            'id': self.id
        }

# Class-2 [Branches wise Course List Table]


class Course(Base):
    __tablename__ = "course"

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(1000))
    date = Column(String(10), nullable=False)
    image = Column(String(1000))
    price = Column(String(10))
    level = Column(String(250))
    branch_id = Column(Integer, ForeignKey('branch.id'))
    branch = relationship(Branch)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(User)

    # JSON format data for course table

    @property
    def serialize(self):

        return {
            'name': self.name,
            'description': self.description,
            'date': self.date,
            'id': self.id,
            'image': self.image,
            'price': self.price,
            'level': self.level,
            'branch_id': self.branch_id
        }


# branchcourse.db File Creation

#engine = create_engine('sqlite:///branchcourse.db')
engine = create_engine('postgresql://catalog:catalog@localhost/catalog')
Base.metadata.create_all(engine)
print("Database Created Sucessfully.")
