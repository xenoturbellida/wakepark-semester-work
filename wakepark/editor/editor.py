from flask import Blueprint, request, render_template, redirect, flash
from flask_login import login_required

from .forms import AddPostForm

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
        ph = form.photos.data
        print(ph)
    # if request.method == 'POST':
    #     # upload_files = request.files.getlist('photos')
    #
    #     print(upload_files)
    return render_template('editor/add_post.html', form=form)
