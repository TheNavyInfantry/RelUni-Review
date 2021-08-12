from reluni_review import db
from reluni_review.posts.forms import PostForm
from reluni_review.models import Post
from flask import render_template, redirect, url_for, flash, request, abort, Blueprint
from flask_login import current_user, login_required

posts = Blueprint('posts', __name__)


@posts.route('/review/new', methods=['GET', 'POST'])
@login_required
def new_review():
    form = PostForm()

    if form.validate_on_submit():
        post_to_create = Post(title=form.title.data,
                              content=form.content_text.data,
                              user_id=current_user.id)

        db.session.add(post_to_create)

        try:
            db.session.commit()
            # flash(f"Hey! Your post has successfully shared!", category='success')

            return redirect(url_for('main.home'))

        except:
            return redirect(url_for('main.errorhandler'))

    else:
        return render_template("share_review.html", form=form)


@posts.route('/review/delete/<int:review_id>', methods=['GET', 'POST'])
@login_required
def delete_review(review_id):
    review = Post.query.get_or_404(review_id)

    if review.user != current_user:
        abort(403)

    db.session.delete(review)
    db.session.commit()

    flash(f"Your post has been deleted!", category='success')

    return redirect(url_for('main.home'))


@posts.route('/review/update/<int:review_id>', methods=['GET', 'POST'])
@login_required
def update_review(review_id):
    review = Post.query.get_or_404(review_id)

    if review.user != current_user:  # Check user and post's owner and if not match
        abort(403)

    form = PostForm()
    if form.validate_on_submit():
        review.title = form.title.data
        review.content = form.content_text.data
        db.session.commit()

        flash(f"Your post has been updated!", category='success')
        return redirect(url_for('main.home', review_id=review.id))

    elif request.method == 'GET':
        form.title.data = review.title
        form.content_text.data = review.content

    return render_template('update_review.html', form=form)
