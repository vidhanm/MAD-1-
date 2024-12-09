from sqlalchemy import event
from flask_login import UserMixin

from config import login_manager, db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)
    role = db.Column(db.Integer, nullable=True)
    password = db.Column(db.String, nullable=False)
    admin = db.Column(db.Boolean, default=False)

class Influencer(db.Model):
    influencer_id = db.Column(db.Integer, db.ForeignKey('user.id'),primary_key=True)
    platform = db.Column(db.Integer, nullable=False)
    followers = db.Column(db.Integer, nullable=True)

    
class Sponsor(db.Model):
    sponsor_id = db.Column(db.Integer, db.ForeignKey('user.id'),primary_key=True)
    company = db.Column(db.Text, nullable=False)
    industry = db.Column(db.Text, nullable=False)
    

class Campaign(db.Model):
    campaign_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    sponsor_id = db.Column(db.Integer, db.ForeignKey('sponsor.sponsor_id'))
    title = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    budget = db.Column(db.Integer, nullable=False)
    visibility = db.Column(db.Integer, nullable=False)

class Request(db.Model):
    request_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    sponsor_id = db.Column(db.Integer, db.ForeignKey('sponsor.sponsor_id'))
    influencer_id = db.Column(db.Integer, db.ForeignKey('influencer.influencer_id'))
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.campaign_id'))
    message = db.Column(db.Text, nullable=True)
    sendby = db.Column(db.Integer, nullable=False) # 1 For Sponsor to Influencer and 0 for vice-versa
    status = db.Column(db.Integer, nullable=False)  
    