from flask import Blueprint, render_template, redirect, flash
from flask_login import login_required


from .forms import AddPostForm
from .helpers import add_post_to_db

editor = Blueprint('editor', __name__, template_folder='templates', static_folder='static')

### TODO: add the method
is_editor = True
###


@editor.route('/add_post', methods=['GET', 'POST'])
@login_required
def add_post():
    if not is_editor:
        flash('Эта страница недоступна')
        return redirect('index.html')

    form = AddPostForm()
    if form.validate_on_submit():
        messages_to_flash = add_post_to_db(form)
        for message in messages_to_flash:
            flash(message[0], category=message[1])

    return render_template('editor/add_post.html', form=form)
