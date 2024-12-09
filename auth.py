from flask import Blueprint, render_template, url_for, flash, redirect,request
from flask_login import login_user, login_required, logout_user, current_user
from models import User, Influencer, Sponsor, Campaign
from config import db
from forms import Influencerform, Sponsorform,Loginform

auth_bp = Blueprint('auth', __name__)

#login route
@auth_bp.route('/', methods=['GET','POST']) 
def login():
    form = Loginform(request.form)

    #print(form.data)
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data,password=form.password.data).first()
        #print(user)
        if user is None:
            print("login failed")
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))

        if user.role == 1:
            login_user(user)
            return redirect(url_for('influ_profile'))   
        if user.role == 2:
            login_user(user)
            return redirect(url_for('spon_profile'))
        if user.admin == 1:
            login_user(user)
            return redirect(url_for('admin_info'))
        print("login successful")
    return render_template('login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')

#Adding influencer registration routes
@auth_bp.route('/register/influencer', methods=[ 'POST'])
def influencer_register():
    form = Influencerform(request.form)
  
    #for field in form:
    #    print(f"{field.name}: {field.data}")
    #print(form.validate()) #validate the form
    #print(form.error)
  
    if request.method == 'POST' and form.validate():
        user = User(
            email=form.email.data,
            name=form.name.data, 
            username=form.username.data,
            password=form.password.data,
            role=1)  # Assuming role 1 is for influencers
        db.session.add(user)
        db.session.commit()

        influencer = Influencer(
            influencer_id=user.id,
            platform=form.platform.data,
            followers=form.followers.data)
        db.session.add(influencer)
        db.session.commit()
        login_user(user)
        return redirect(url_for('influ_profile'))
    return "" ,400

#adding sponsor registration routes
@auth_bp.route('/register/sponsor', methods=[ 'POST'])
def sponsor_register():
    form = Sponsorform(request.form)
    
    #for field in form:
    #    print(f"{field.name}: {field.data}")
    #print(form.validate()) #validate the form
   
    if request.method == 'POST' and form.validate():
        user = User(
            email=form.email.data, 
            name=form.name.data, 
            username=form.username.data, 
            password=form.password.data, 
            role=2)
        db.session.add(user)
        db.session.commit()

        sponsor = Sponsor(
            sponsor_id=user.id, 
            company=form.company.data, 
            industry=form.industry.data)
        db.session.add(sponsor)
        db.session.commit()
        login_user(user)
        return redirect(url_for('spon_profile'))
    return "" ,400



'''
@auth_bp.route('/register/influencer', methods=['GET', 'POST'])
def influencer_register():
    print(dir())
    print(globals().keys())
    form = Influencerform()
    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            name=form.name.data, 
            username=form.username.data,
            password=form.password.data,
            role=1)
        db.session.add(user)
        db.session.commit()
        influencer = Influencer(
            influencer_id=form.id, 
            platform=form.platform.data)
        db.session.add(influencer)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form, role='influencer')

@auth_bp.route('/register/sponsor', methods=['GET', 'POST'])
def sponsor_register():
    form = Sponsorform()
    if form.validate_on_submit():
        user = User(email=form.email.data, name=form.name.data, username=form.username.data, password=form.password.data, role=2)
        db.session.add(user)
        db.session.commit()
        sponsor = Sponsor(sponsor_id=user.id, company=form.company.data, Industry=form.Industry.data)
        db.session.add(sponsor)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('login.html', form=form,role='sponsor')
'''
'''
@auth_bp.route("/register/influencer", methods=['GET', 'POST'])
def registerinflu():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = Influencerform()

    try:
        user = User(
            username=form.username.data,
            name=form.name.data,
            email=form.email.data,
            password=form.password.data,
            role=1
        )
        db.session.add(user)
        db.session.commit()
        Influ = Influencer(
            influencer_id=user.id,
            platform=form.platform.data
        )
        db.session.add(Influ)
        db.session.commit()
   
        flash('Account created successfully', 'success')
        return redirect(url_for('auth.login'))
    except Exception as e:
        db.session.rollback()
        flash(f'Account creation failed: {str(e)}', 'danger')
    return render_template('login.html', form=form)

# Add other auth routes (login, logout, etc.) here


@auth_bp.route("/register/sponsor", methods=['GET', 'POST'])
def register_sponsor():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = Sponsorform()

    try:
            user = User(
                username=form.username.data,
                name=form.name.data,
                email=form.email.data,
                password=form.password.data,
                role=2  # Assuming role 2 is for sponsors
            )
            db.session.add(user)
            db.session.commit()

            sponsor = Sponsor(
                sponsor_id=user.id,
                company=form.company.data,
                industry=form.industry.data
            )
            db.session.add(sponsor)
            db.session.commit()

            flash('Sponsor account created successfully', 'success')
            return redirect(url_for('auth.login'))
    except Exception as e:
            db.session.rollback()
            flash(f'Account creation failed: {str(e)}', 'danger')

    return render_template('register_sponsor.html', form=form)
'''