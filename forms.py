from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField
from wtforms.validators import DataRequired, Email, Length

class Loginform(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=1, max=25)])
    password = PasswordField('Password', validators=[ DataRequired()])#password lenght validation

class Influencerform(FlaskForm):
    email = StringField('Email', validators=[Email(), DataRequired()])
    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=25)])
    username = StringField('Username', validators=[DataRequired(), Length(min=1, max=25)])
    password = PasswordField('Password', validators=[ DataRequired()])#password lenght validation
    platform = StringField('Platform', validators=[DataRequired()])
    followers = StringField('Followers', validators=[DataRequired()])

class Sponsorform(FlaskForm):
    email = StringField('Email', validators=[Email(), DataRequired()])
    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=25)])
    username = StringField('Username', validators=[DataRequired(), Length(min=1, max=25)])
    password = PasswordField('Password', validators=[ DataRequired()])#password lenght validation
    company = StringField('Company', validators=[DataRequired(), Length(min=1, max=25)])
    industry = StringField('Industry', validators=[DataRequired()])

class Campaignform(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=25)])
    description = StringField('Description', validators=[DataRequired(), Length(min=1, max=25)])
    start_date = DateField('Start Date', validators=[DataRequired()])
    end_date = DateField('End Date', validators=[DataRequired()])
    budget = StringField('Budget', validators=[DataRequired()])
    visibility = StringField('Visibility', validators=[DataRequired()]) 

class SponsorRequestform(FlaskForm):
    #sponsor_id = StringField('Sponsor ID', validators=[DataRequired()])
    influencer_id = StringField('Influencer ID', validators=[DataRequired()])
    campaign_id = StringField('Campaign ID', validators=[DataRequired()])
    message = StringField('Message', validators=[DataRequired()])
    status = StringField('Status', validators=[DataRequired()],default="pending")

class InfluencerRequestform(FlaskForm):
    #influencer_id = StringField('Influencer ID', validators=[DataRequired()])
    sponsor_id = StringField('Sponsor ID', validators=[DataRequired()])
    campaign_id = StringField('Campaign ID', validators=[DataRequired()])
    status = StringField('Status', validators=[DataRequired()],default="pending")