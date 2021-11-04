import os
from datetime import datetime

from flask import request
from sqlalchemy.exc import SQLAlchemyError

from ..models import Post, db, Photo

PHOTO_SIZE = 1048576  # 1 MB
UPLOAD_PHOTOS_DIR = 'photos'


def add_post_to_db(form):
    messages_to_flash = []

    pubdate = datetime.now()
    try:
        title = form.title.data
        content = form.content.data
        post = Post(title=title,
                    content=content,
                    pubdate=pubdate)
        db.session.add(post)
        db.session.flush()
        db.session.refresh(post)
    except SQLAlchemyError as e:
        messages_to_flash.append(('Произошла непредвиденная ошибка при добавлении поста', 'error'))
        print(e)
        db.session.rollback()
        return messages_to_flash

    if form.photos.data:
        upload_files = request.files.getlist('photos')
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
                    messages_to_flash.append(
                        (f'Произошла непредвиденная ошибка при добавлении фото номер {photo_serial_number}',
                         'error')
                    )
                    db.session.rollback()
                    print(e)
                finally:
                    photo_serial_number += 1
            db.session.commit()
            print(post.photos)
        else:
            messages_to_flash.append(('Произошла непредвиденная ошибка при добавлении фотографий', 'error'))
    return messages_to_flash
