# !/usr/bin/env python
# Catalog Items Application is Copyright 2015 by Deanna M. Wagner.  This app
# displays a selection of exercises, based on their category.  This file
# db_setup.py creates and serializes the list of exercises and categories.
#


import os
import sys
import psycopg2
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine


Base = declarative_base()


# Class Category represents the necessary columns for the table category
class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    url = Column(String(100), nullable=False)

    @property
    def serialize(self):

        return {
            'id': self.id,
            'name': self.name,
            'url': self.url
            }

# Class Exercise represents the necessary columns for the table exercise
class Exercise(Base):
    __tablename__ = 'exercise'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(String(300))
    image_link = Column(String(80))
    category_id = Column(Integer, ForeignKey('category.id'))
    creator_id = Column(String(256))
    category = relationship(Category)

    @property
    def serialize(self):

        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'image_link': self.image_link,
            'category_id': self.category_id,
            'creator_id': self.creator_id,
            }

if __name__ == '__main__':
    engine = create_engine('postgresql://catalog:cVGy7@localhost:5432/' \
                       'fitcollection')
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
