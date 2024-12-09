from config import app, db, login_manager
# Import your User model
from models import User, Sponsor, Influencer, Campaign, Request
from auth import auth_bp  # Import your auth blueprint
from flask import render_template, jsonify, request, redirect, url_for
from forms import Campaignform, SponsorRequestform
from flask_login import current_user, login_required, logout_user
from functools import wraps
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
# Register your blueprint
app.register_blueprint(auth_bp)

# Set up the user loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


# Decorators Starts here 
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.admin == 1:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('auth.login'))
    return decorated_function


def influencer_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.role == 1: 
             return f(*args, **kwargs)
        elif current_user.role == 2:
            return redirect(url_for('spon_profile'))
        else:
            return redirect(url_for('login'))
    return decorated_function


def sponsor_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.role == 2: 
            return f(*args, **kwargs)
        elif current_user.role == 1:
            return redirect(url_for('influ_profile'))
        else:
            return redirect(url_for('login'))
    return decorated_function
# Decorators Ends here



# Admin Paths start
@app.route('/admin/info')
@login_required
@admin_required
def admin_info():
    accamp = db.session.query(Request, Campaign, User, ).join(
        Campaign,
        Campaign.campaign_id == Request.campaign_id
    ).join(
        User,
        User.id == Request.sponsor_id
    ).filter(
        Request.status == 1,
    ).all()
    # print(accamp)
    # print(accamp[0][2].name)
    return render_template('admin_info.html', accamp=accamp, username=current_user.username)


@app.route('/admin/find')
@login_required
@admin_required
def admin_find():
    query = request.args.get('q')
    Qtype = request.args.get('type')
    platforms = ['Youtube', 'Instagram', 'Twitter']
    if query:
        # print("entered query")
        if Qtype == 'campaign':
            campaign_results = Campaign.query.filter(Campaign.title.contains(
                query)).all()
            
            return render_template('admin_find.html', username=current_user.username, campresults=campaign_results)

        elif Qtype == 'influencer':
            influencer_results = db.session.query(User, Influencer).filter(User.username.contains(
                query)).join(Influencer, User.id == Influencer.influencer_id).all()
            
            return render_template('admin_find.html', username=current_user.username, influresults=influencer_results, platforms=platforms, sponsresults=sponsor_results)


    campaign_results = Campaign.query.all()
    influencer_results = db.session.query(User, Influencer).join(
        Influencer, User.id == Influencer.influencer_id).all()
    sponsor_results = db.session.query(User, Sponsor).join(
        Sponsor, User.id == Sponsor.sponsor_id).all()
    
    return render_template('admin_find.html', username=current_user.username, campresults=campaign_results, influresults=influencer_results, platforms=platforms, sponresults=sponsor_results)


@app.route('/admin/find/camp/delete/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_find_camp_delete(id):
    campaign = Campaign.query.filter_by(
        campaign_id=id).first()
    if campaign:
        db.session.delete(campaign)
        db.session.commit()

    return redirect(url_for('admin_find'))


@app.route('/admin/find/influ/delete/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_find_influ_delete(id):
    influencer = Influencer.query.filter_by(
        influencer_id=id).first()
    user = User.query.filter_by(
        id=id).first()
    if influencer:
        db.session.delete(influencer)
    if user:
        db.session.delete(user)
    db.session.commit()

    return redirect(url_for('admin_find'))


@app.route('/admin/find/spon/delete/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_find_spon_delete(id):
    sponsor = Sponsor.query.filter_by(
        sponsor_id=id).first()
    user = User.query.filter_by(
        id=id).first()
    if sponsor:
        db.session.delete(sponsor)
    if user:
        db.session.delete(user)
    db.session.commit()
    return redirect(url_for('admin_find'))


@app.route('/admin/stats')
@login_required
@admin_required
def admin_stats():
    total_users = User.query.count()
    total_influencers = Influencer.query.count()
    total_sponsors = Sponsor.query.count()
    total_campaigns = Campaign.query.count()
    total_requests = Request.query.count()

    # Generate plots
    plots = []

    # User distribution pie chart
    plt.figure(figsize=(8, 6))
    plt.pie([total_influencers, total_sponsors], labels=['Influencers', 'Sponsors'], autopct='%1.1f%%')
    plt.title('User Distribution')
    plots.append(get_plot_url())

    # Campaign visibility bar chart
    public_campaigns = Campaign.query.filter_by(visibility="Public").count()
    private_campaigns = Campaign.query.filter_by(visibility="Private").count()
    plt.figure(figsize=(8, 6))
    plt.bar(['Public', 'Private'], [public_campaigns, private_campaigns])
    plt.title('Campaign Visibility')
    plt.ylabel('Number of Campaigns')
    plots.append(get_plot_url())

    # Request status pie chart
    pending_requests = Request.query.filter_by(status=0).count()
    accepted_requests = Request.query.filter_by(status=1).count()
    
    plt.figure(figsize=(8, 6))
    plt.pie([pending_requests, accepted_requests], labels=['Pending', 'Accepted'], autopct='%1.1f%%')
    plt.title('Request Status')
    plots.append(get_plot_url())

    return render_template('admin_stats.html', username=current_user.username,
                           total_users=total_users, total_influencers=total_influencers,
                           total_sponsors=total_sponsors, total_campaigns=total_campaigns,
                           total_requests=total_requests, plots=plots)

def get_plot_url():
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return plot_url
    #return render_template('admin_stats.html')
# admin path end



# Influencer paths start
@app.route('/influencer/profile')
@login_required
@influencer_required
def influ_profile():
    activecamp = db.session.query(Request, Campaign, User).join(
        Request,  # for above section of influener profile page
        (current_user.id == Request.influencer_id) &
        (Campaign.campaign_id == Request.campaign_id) &
        (Request.status == 1)
    ).join(
        User,
        (User.id == Request.sponsor_id)
    ).all()
    #print(activecamp)


    newcamp = db.session.query(Campaign, Request, User).join(
        Request,  # for accepting sponsor request
        (current_user.id == Request.influencer_id) &
        (Campaign.campaign_id == Request.campaign_id) &
        (Request.status == 0) &
        (Request.sendby == 1)
    ).join(
        User,
        (User.id == Request.sponsor_id)
    ).all()
    
    return render_template('influ_profile.html', username=current_user.username, newcamp=newcamp, activecamp=activecamp)


@app.route('/influencer/profile/accept/<int:id>', methods=['GET', 'POST'])
@login_required
@influencer_required
def influ_profile_accept(id):
    sponsor_request = Request.query.filter_by(
        request_id=id, influencer_id=current_user.id).first()
    if sponsor_request:
        # Update the status
        sponsor_request.status = 1
        # Commit the session to save the changes
        db.session.commit()
   # SponsorRequest.Update().values(status='accepted').where(SponsorRequest.request_id == id, SponsorRequest.influencer_id == current_user.id)
    return redirect(url_for('influ_profile'))


@app.route('/influencer/profile/reject/<int:id>', methods=['GET', 'POST'])
@login_required
@influencer_required
def influ_profile_reject(id):
    sponsor_request = Request.query.filter_by(
        request_id=id, influencer_id=current_user.id).first()
    if sponsor_request:
        # Update the status
        db.session.delete(sponsor_request)
        # Commit the session to save the changes
        db.session.commit()
        # SponsorRequest.Update().values(status='accepted').where(SponsorRequest.request_id == id, SponsorRequest.influencer_id == current_user.id)

        return redirect(url_for('influ_profile'))
    
    return render_template('influ_profile.html', username=current_user.username)


@app.route('/influencer/find')
@login_required
@influencer_required
def influ_find():
    campaign_results = Campaign.query.filter(
        Campaign.visibility == "Public").all()
    sponsorr = Sponsor.query.all()
    # print(campaign_results)
    return render_template('influ_find.html', username=current_user.username, campaign_results=campaign_results, sponsorr=sponsorr)


@app.route('/influencer/find/request/<int:id>', methods=['GET', 'POST'])
@login_required
@influencer_required
def influ_find_request(id):
    # form = InfluencerRequestform(request.form)
    if Request.query.filter(Request.campaign_id == id,Request.influencer_id==current_user.id).first() != None: 
        return redirect(url_for('influ_find'))
    

    camp = Campaign.query.filter_by(campaign_id=id).first()
    if camp:
        influ_request = Request()
        influ_request.campaign_id = camp.campaign_id
        influ_request.influencer_id = current_user.id
        influ_request.sponsor_id = camp.sponsor_id
        influ_request.status = 0
        influ_request.sendby = 0
        db.session.add(influ_request)
        db.session.commit()
        print("database updated")

    return redirect(url_for('influ_find'))

# infuencer path end

# sponsor paths start


@app.route('/sponsor/profile')
@login_required
@sponsor_required
def spon_profile():
    campnames = db.session.query(Campaign, Request, User, Influencer).join(
        Request,
        (current_user.id == Request.sponsor_id) &
        (Campaign.campaign_id == Request.campaign_id) &
        (Request.status == 0) &
        (Request.sendby == 0)
    ).join(
        User,
        (User.id == Request.influencer_id)
    ).join(Influencer, 
        (Influencer.influencer_id == User.id)).all()
    
    platforms = ['Youtube', 'Instagram', 'Twitter']

    # print(campnames)
    # print(campnames[0][0].title)
    activecamp = db.session.query(Request, Campaign, User,).join(
        Request,  # for above section of sponsor profile page
        (current_user.id == Request.sponsor_id) &
        (Campaign.campaign_id == Request.campaign_id) &
        (Request.status == 1)
    ).join(
        User,
        (User.id == Request.influencer_id)
    ).all()
    return render_template('spon_profile.html', username=current_user.username, platforms=platforms,campnames=campnames, activecamp=activecamp)


@app.route('/sponsor/profile/accept/<int:id>', methods=['GET', 'POST'])
@login_required
@sponsor_required
def spon_profile_accept(id):
    influencer_request = Request.query.filter_by(
        request_id=id, sponsor_id=current_user.id).first()
    if influencer_request:
        # Update the status
        influencer_request.status = 1

        # Commit the session to save the changes
        db.session.commit()
        print("accepted")
        return redirect(url_for('spon_profile'))
    return render_template('spon_profile.html', username=current_user.username)


@app.route('/sponsor/profile/reject/<int:id>', methods=['GET', 'POST'])
@login_required
@sponsor_required
def spon_profile_reject(id):
    influencer_request = Request.query.filter_by(
        request_id=id, sponsor_id=current_user.id).first()
    if influencer_request:
        # Update the status
        db.session.delete(influencer_request)
        # Commit the session to save the changes
        db.session.commit()
        print("rejected")
        return redirect(url_for('spon_profile'))
    return render_template('spon_profile.html', username=current_user.username)


@app.route('/sponsor/find', methods=['GET', 'POST'])
@login_required
@sponsor_required
def spon_find():
    query = request.args.get('q')
    Qtype = request.args.get('type')
    edit_id = request.args.get('edit_id')
    platforms = ['Youtube', 'Instagram', 'Twitter']
    if query:
        # print("entered query")
        if Qtype == 'campaign':
            campaign_results = Campaign.query.filter(Campaign.title.contains(
                query), Campaign.sponsor_id == current_user.id,).all()
            return render_template('spon_find.html', username=current_user.username, campresults=campaign_results)

        elif Qtype == 'influencer':
            influencer_results = db.session.query(User, Influencer).filter(User.username.contains(
                query)).join(Influencer, User.id == Influencer.influencer_id).all()
            return render_template('spon_find.html', username=current_user.username, influresults=influencer_results, platforms=platforms)

    else:
        campaign_results = Campaign.query.filter(Campaign.sponsor_id == current_user.id).all()
        influencer_results = db.session.query(User, Influencer).join(Influencer, User.id == Influencer.influencer_id).all()
    
    edit_form= None
    if edit_id != None:
        edit_form= Campaign.query.filter(Campaign.campaign_id==edit_id).first()
        
    
    return render_template('spon_find.html', 
                           username=current_user.username, 
                           campresults=campaign_results, 
                           influresults=influencer_results, 
                           platforms=platforms,
                           edit_form=edit_form)


# @app.route('/sponsor/camp', methods=['GET'])
# @login_required
# @sponsor_required
# def sponGetCamp():
#     id = request.args.get("id")
#     if id == None:
#         return 403, ""

#     camp = Campaign.query.filter(Campaign.campaign_id == id).first()
#     if camp == None:
#         return 404, ""
#     return jsonify(title = camp.title, 
#                    description = camp.description, 
#                    start_date = camp.start_date, 
#                    end_date = camp.end_date, 
#                    budget= camp.budget, 
#                    visibility = camp.visibility)



@app.route('/sponsor/find/camp/delete/<int:id>', methods=['GET', 'POST'])
@login_required
@sponsor_required
def spon_find_camp_delete(id):
    campaign = Campaign.query.filter_by(
        campaign_id=id).first()
    if campaign:
        db.session.delete(campaign)
        db.session.commit()
    return redirect(url_for('spon_find'))


@app.route('/sponsor/find/camp/edit/<int:id>', methods=['POST'])
@login_required
@sponsor_required
def spon_find_camp_edit(id):
    form = Campaignform(request.form)
    #print(form.errors)

    if form.validate():
        campaign = Campaign.query.filter(Campaign.campaign_id==id).first();
        if campaign != None:
            #print("DDDD")
            form.populate_obj(campaign)
            db.session.commit()
            
    return redirect(url_for('spon_find'))




@app.route('/sponsor/find/request', methods=['GET', 'POST'])
@login_required
@sponsor_required
def spon_find_request():
    form = SponsorRequestform(request.form)
    if form.validate():
        if Request.query.filter(Request.campaign_id == form.campaign_id.data,Request.influencer_id==form.influencer_id.data).first() != None: 
            return redirect(url_for('spon_find'))
    

        sponsor_request = Request(
            sponsor_id=current_user.id,
            influencer_id=form.influencer_id.data,
            campaign_id=form.campaign_id.data,
            message=form.message.data,
            status=0,
            sendby=1
            )
        db.session.add(sponsor_request)
        db.session.commit()
    
    return (redirect(url_for('spon_find')))



@app.route('/sponsor/campaign', methods=['GET', 'POST'])
@login_required
@sponsor_required
def spon_campaign():
    form = Campaignform(request.form)

    # print(form.validate())
    # print(form.data)
    # print(form.errors)

    if form.validate_on_submit():
        campaign = Campaign(
            sponsor_id=current_user.id,  # Assuming sponsor_id 1 is the current sponsor
            title=form.title.data,
            description=form.description.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            budget=form.budget.data,
            visibility=form.visibility.data)
        db.session.add(campaign)
        db.session.commit()

    return render_template('spon_campaign.html', username=current_user.username)
# sponsor path end


if __name__ == "__main__":
    app.run(debug=True)
