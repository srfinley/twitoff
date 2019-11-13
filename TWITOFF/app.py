from decouple import config
from flask import Flask, render_template, request
from .models import DB, User, Tweet
from .twitter import TWITTER, BASILICA

# app factory

def create_app():
    app = Flask(__name__)

    # add config
    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # tell database about app
    DB.init_app(app)

    @app.route('/')
    def root():
        users = User.query.all()
        return render_template('base.html', title='Home', users=users)

    @app.route('/user/<username>')
    def show_user_tweets(username):
        twitter_user=TWITTER.get_user(username)
        tweets=twitter_user.timeline(count=200, exclude_replies=True,
                                     include_rts=False, tweet_mode='extended')
        db_user=User(id=twitter_user.id, name=twitter_user.screen_name,
                     newest_tweet_id=tweets[0].id)
        for tweet in tweets:
            embedding = BASILICA.embed_sentence(tweet.full_text, model='twitter')
            db_tweet = Tweet(id=tweet.id, text=tweet.full_text[:500], embedding=embedding)
            DB.session.add(db_tweet)
            db_user.tweets.append(db_tweet)
        return render_template('username.html', username=username, tweets=tweets)

    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title='Reset', users=[])
    return app