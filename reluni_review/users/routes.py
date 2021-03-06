from reluni_review import db
from reluni_review.users.forms import RegisterForm, LoginForm, RequestResetForm, ResetPasswordForm
from reluni_review.models import User, Post
from flask import render_template, redirect, url_for, flash, request, session, Blueprint
from flask_login import login_user, logout_user, login_required, current_user
from reluni_review.users.utils import send_reset_email

users = Blueprint('users', __name__)


@users.route('/user/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password.data)

        db.session.add(user_to_create)
        db.session.commit()

        login_user(user_to_create) #Automatically logs the user in

        flash(f"Hey {user_to_create.username}! Your account has successfully created and logged into the website!",
              category='success')

        return redirect(url_for('main.home'))

    if form.errors != {}:  # To make sure that there aren't errors from validations
        for error_message in form.errors.values():
            flash(f'{error_message}', category='danger')  # This category has a connection to base.html

    return render_template("register.html", form=form)


@users.route('/user/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        """
        1) Checks if the user is exists,
        2) Checks if the user and password are exists
        """
        attempted_user = User.query.filter_by(email_address=form.email_address.data).first()

        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):

            login_user(attempted_user)

            session.permanent = True

            session.modified = True

            flash(f"You have successfully logged in as {attempted_user.username}", category='success')

            return redirect(url_for('main.home'))

        else:
            flash(f"Username and Password do NOT match! Please try again!", category='danger')

    return render_template("login.html", form=form)


@users.route('/user/logout')
@login_required
def logout():
    logout_user()

    flash("You have successfully logged out!", category='warning')

    return redirect(url_for('main.home'))


@users.route('/user/review/<string:username>', methods=['GET', 'POST'])
@login_required
def user_review(username):
    page = request.args.get('page', 1, type=int)

    user = User.query.filter_by(username=username).first_or_404()

    reviews = Post.query.filter_by(user=user) \
        .order_by(Post.time_stamp.desc()) \
        .paginate(page=page, per_page=6)

    return render_template("user_review.html", reviews=reviews, user=user)


@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RequestResetForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email_address=form.email_address.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password!', category='info')
        return redirect(url_for('login'))

    return render_template('reset_request.html', form=form)

@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    user = User.verify_reset_token(token)

    if user is None:
        flash('That is an invalid or expired token!', category='warning')
        return redirect(url_for('reset_request'))

    form = ResetPasswordForm()

    if form.validate_on_submit():
        user_reset_password = User(password=form.password.data)

        db.session.commit()

        # login_user(user_reset_password)

        flash(f"Hey {user_reset_password.username}! Your password has successfully updated!",
              category='success')

        return redirect(url_for('users.login'))

    return render_template('reset_token.html', form=form)