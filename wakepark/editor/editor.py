from flask import Blueprint, request, render_template, redirect, flash
from flask_login import login_required

from .forms import AddPostForm

editor = Blueprint('editor', __name__, template_folder='templates', static_folder='static')


### TODO: add the method
is_editor = True
###
PHOTO_SIZE = 1048576  # 1 MB
UPLOAD_PHOTOS_DIR = 'photos'


@editor.route('/add_post', methods=['GET', 'POST'])
@login_required
def add_post():
    if not is_editor:
        flash('Эта страница недоступна')
        return redirect('index.html')

    form = AddPostForm()
    if form.validate_on_submit():
        if form.photos.data:
            upload_files = request.files.getlist('photos')
            file_path = None
            if upload_files:
                dir_path = os.path.join('editor', 'static', UPLOAD_PHOTOS_DIR)
                for file in upload_files:
                    file.save(os.path.join(dir_path, file.filename), buffer_size=PHOTO_SIZE)
                    file.close()
    return render_template('editor/add_post.html', form=form)
