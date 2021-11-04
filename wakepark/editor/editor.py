import os
from datetime import datetime

from flask import Blueprint, request, render_template, redirect, flash
from flask_login import login_required
from sqlalchemy.exc import SQLAlchemyError

from .forms import AddPostForm
from ..models import Post, db, Photo

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
        pubdate = datetime.now()
        try:
            title = form.title.data
            content = form.content.data
            post = Post(title=title,
                        content=content,
                        pubdate=pubdate)
            db.session.add(post)
            # db.session.commit()
            db.session.flush()
            db.session.refresh(post)

        except SQLAlchemyError as e:
            flash('Произошла непредвиденная ошибка при добавлении поста', category='error')
            print(e)
            db.session.rollback()
            return render_template('editor/add_post.html', form=form)

        if form.photos.data:
            upload_files = request.files.getlist('photos')
            # file_path = None
            if upload_files:
                dir_path = os.path.join('editor', 'static', UPLOAD_PHOTOS_DIR)
                photo_serial_number = 0
                for file in upload_files:
                    file_extension = file.filename.rsplit('.', 1)[1]
                    file_name = f"{pubdate.strftime('%Y-%m-%d %H%M%S')} {photo_serial_number}.{file_extension}"
                    file_path = os.path.join(dir_path, file_name)
                    try:
                        file.save(file_path, buffer_size=PHOTO_SIZE)
                        file.close()
                        photo = Photo(path=file_path, post_id=post.id)
                        db.session.add(photo)
                    except SQLAlchemyError as e:
                        flash(f'Произошла непредвиденная ошибка при добавлении фото номер {photo_serial_number}',
                              category='error')
                        db.session.rollback()
                        print(e)
                    finally:
                        photo_serial_number += 1
                db.session.commit()
                print(post.photos)
            else:
                flash('Произошла непредвиденная ошибка при добавлении фотографий', category='error')
    return render_template('editor/add_post.html', form=form)
