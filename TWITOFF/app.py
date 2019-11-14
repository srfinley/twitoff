"""build app factory, do routes and config"""

from decouple import config
from flask import Flask, render_template, request
from .models import DB, User, Tweet
from .twitter import TWITTER, BASILICA, add_or_update_user
from .predict import predict_user
from dotenv import load_dotenv

load_dotenv()

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

    # @app.route('/usertweets/<username>')
    # def show_user_tweets(username):
    #     twitter_user=TWITTER.get_user(username)
    #     tweets=twitter_user.timeline(count=200, exclude_replies=True,
    #                                  include_rts=False, tweet_mode='extended')
    #     db_user=User(id=twitter_user.id, name=twitter_user.screen_name,
    #                  newest_tweet_id=tweets[0].id)
    #     for tweet in tweets:
    #         embedding = BASILICA.embed_sentence(tweet.full_text, model='twitter')
    #         db_tweet = Tweet(id=tweet.id, text=tweet.full_text[:500], embedding=embedding)
    #         DB.session.add(db_tweet)
    #         db_user.tweets.append(db_tweet)
    #     return render_template('username.html', username=username, tweets=tweets)

    @app.route('/user', methods=['POST'])
    @app.route('/user/<name>', methods=['GET'])
    def user(name=None, message=''):
        name = name or request.values['user_name']
        try:
            if request.method == 'POST':
                add_or_update_user(name)
                message = "User {} successfully added!".format(name)
            tweets = User.query.filter(User.name == name).one().tweets
        except Exception as e:
            message = "Error adding {}: {}".format(name, e)
            tweets = []
        return render_template('user.html', title=name, tweets=tweets, message=message)

    @app.route('/compare', methods=['POST'])
    def compare(message=''):
        user1, user2 = sorted([request.values['user1'], request.values['user2']])
        if user1 == user2:
            message = "Cannot compare users to themselves"
        else:
            prediction = predict_user(user1, user2, request.values['tweet_text'])[0]
            percent = int(round(max(predict_user(user1, user2, request.values['tweet_text'])[1][0]) * 100))
            message = '"{}" is more likely to be said by {} than {}. Confidence: {}%'.format(
                request.values['tweet_text'], user1 if prediction else user2, user2 if prediction else user1, percent)
        return render_template('prediction.html', title='Prediction', message=message)


    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title='Reset', users=[])
    return app