from flask import redirect, url_for, session, request, render_template, jsonify
from flask_oauth import OAuth
from algorithm import User, app, db, fb

DEBUG = True
oauth = OAuth()
facebook = oauth.remote_app('facebook',
                            base_url='https://graph.facebook.com/',
                            request_token_url=None,
                            access_token_url='/oauth/access_token',
                            authorize_url='https://www.facebook.com/dialog/oauth',
                            consumer_key="YOUR KEY HERE",
                            consumer_secret="YOUR SECRET HERE",
                            request_token_params={
                                'scope': 'user_likes, user_photos, user_friends, user_status, user_posts, read_insights, read_audience_network_insights, read_custom_friendlists, public_profile'}
                            )


@app.route('/')
def index():
    return render_template("login.html")


@app.route('/login')
def login():
    return facebook.authorize(callback=url_for('facebook_authorized',
                                               next=request.args.get('next') or request.referrer or None,
                                               _external=True))


@app.route('/login/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['oauth_token'] = (resp['access_token'], '')
    try:
        user_id = fb(resp['access_token'], "me")["id"]
        session['user_id'] = (str(user_id), '')
    except:
        return authorise()
    return redirect(url_for('profile', user_id=user_id))
    # return "Base Score: " + str(me.naive_score) + ", Bonus: " + str(me.bonus)
    # return 'Logged in as id=%s name=%s redirect=%s' % \
    #         (me.data['id'], me.data['name'], request.args.get('next'))


@app.route('/profile/<int:user_id>')
def profile(user_id):
    try:
        user = User.query.get(user_id)
    except:
        user = False
    if not user:
        try:
            token = get_facebook_oauth_token()
        except:
            return authorise()
        me = User(token, user_id)
        return render_template("incomplete_profile.html", user=me)
    else:
        token = get_facebook_oauth_token()
        recalculate = False
        if token:
            try:
                visit_user_id = fb(token, "me")["id"]
                if str(user_id) == visit_user_id:
                    recalculate = True
            except:
                pass
        return render_template("profile.html", user=user, recalculate=recalculate)


@app.route('/calculate/')
def calculate():
    try:
        token = get_facebook_oauth_token()
        me = User(token)
        me.get_scores()
        try:
            db.session.add(me)
            db.session.commit()
        except:
            pass
        rounded_final = round(float(me.final_score), 3)
        rounded_bonus = round(float(me.bonus), 3)
        return jsonify(final_score=str(rounded_final),
                       bonus=str(rounded_bonus),
                       num=rounded_final*10000,
                       int=str(rounded_final)[:3], decimal=str(rounded_final)[3:])
    except:  # If anything goes wrong, reauthorise
        raise
        return authorise()


@app.route('/remove/<int:user_id>')
def remove_entry(user_id):
    try:
        token = get_facebook_oauth_token()
        me = fb(token, "me")
        if str(user_id) == me["id"]:
            User.query.filter_by(id=user_id).delete()
            db.session.commit()
        return authorise()
    except:  # If anything goes wrong, reauthorise
        return authorise()


@app.errorhandler(404)
def page_not_found(e):
    print e
    return redirect(url_for('index'))


@app.errorhandler(500)
def internal_error(e):
    print e
    return redirect(url_for('index'))


@facebook.tokengetter
def get_facebook_oauth_token():
    try:
        return session.get('oauth_token')[0]
    except:
        return 0


def get_facebook_session_user_id():
    try:
        return session.get('user_id')[0]
    except:
        return 0


@app.template_filter('urlencode')
def urlencode_filter(s):
    if type(s) == 'Markup':
        s = s.unescape()
    s = s.encode('utf8')
    s = urllib.quote_plus(s)
    return Markup(s)


def authorise():
    return redirect(url_for('login'))


if __name__ == '__main__':
    db.create_all()
    app.run(debug=False, host="0.0.0.0")



