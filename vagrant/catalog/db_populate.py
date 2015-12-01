# !/usr/bin/env python
# Catalog Items Application is Copyright 2015 by Deanna M. Wagner.  This app
# displays a selection of exercises, based on their category.  This file
# db_populate.py creates and commits the complete list of exercise categories.
#


import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setup import Base, Category, Exercise


engine = create_engine('postgresql://fcuser:uhbVCXdr5!Q@localhost:5432/' \
                       'fitcollection')
#engine = create_engine('postgresql://fcuser:mPo75!QsCr89K@localhost:5432/' \
#                       'fitcollection')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
db_session = DBSession()
warmup = Category(name='Warm Up', url='/warmup')
db_session.add(warmup)
cardio = Category(name='Cardio', url='/cardio')
db_session.add(cardio)
strength = Category(name='Strength', url='/strength')
db_session.add(strength)
mindbody = Category(name='Mind Body', url='/mindbody')
db_session.add(mindbody)
cooldown = Category(name='Cool Down', url='/cooldown')
db_session.add(cooldown)
db_session.commit()


def get_cat(category_url):
    """Get category id for a given category url"""
    category = db_session.query(Category).filter_by(url = category_url).one()
    return category


DBSession = sessionmaker(bind=engine)
db_session = DBSession()
walk = Exercise(name='Walk',
                description='5-10 min low intensity walk and dynamic stretches', 
                image_link='/static/images/walk.jpg',
                category_id=get_cat('/warmup').id,
                creator_id=1,
                category=get_cat('/warmup'))
db_session.add(walk)
soccer = Exercise(name='Soccer',
                description='15-45 min moderate to high intensity soccer play', 
                image_link='/static/images/Soccer.png',
                category_id=get_cat('/cardio').id,
                creator_id=1,
                category=get_cat('/cardio'))
db_session.add(soccer)
skate = Exercise(name='Skate',
                description='15-45 min moderate to high intensity skating', 
                image_link='/static/images/Skate.jpg',
                category_id=get_cat('/cardio').id,
                creator_id=1,
                category=get_cat('/cardio'))
db_session.add(skate)
press = Exercise(name='Overhead Press',
                description='2-3 sets of 8-15 reps at a moderate weight', 
                image_link='/static/images/PressSpot.png',
                category_id=get_cat('/strength').id,
                creator_id=1,
                category=get_cat('/strength'))
db_session.add(press)
down_dog = Exercise(name='Adho Mukha Svanasana',
                description='1-2 min in down dog, breathing in and out',
                image_link='/static/images/AdhoMukhaSvanasana.png',
                category_id=get_cat('/mindbody').id,
                creator_id=1,
                category=get_cat('/mindbody'))
db_session.add(down_dog)
stretch = Exercise(name='Stretch',
                description='5-10 min stretching after conditioning phase', 
                image_link='/static/images/UpavistaKonasana.png',
                category_id=get_cat('/cooldown').id,
                creator_id=1,
                category=get_cat('/cooldown'))
db_session.add(stretch)
db_session.commit()