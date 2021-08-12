from reluni_review.models import User, Post
from flask import render_template, request, Blueprint

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    username = User.query.get('username')
    page = request.args.get('page', 1, type=int)
    reviews = Post.query.order_by(Post.time_stamp.desc()).paginate(page=page, per_page=6)  # getting latest records

    return render_template("home.html", reviews=reviews, username=username)


@main.errorhandler(404)
def error(e):
    return render_template("404.html"), 404
