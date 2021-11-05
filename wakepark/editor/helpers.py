import os
from math import ceil

import psycopg2
from datetime import datetime

from flask import request
from sqlalchemy.exc import SQLAlchemyError

from ..models import Post, db, Photo

PHOTO_SIZE = 10485760  # 10 MB
UPLOAD_PHOTOS_DIR = 'photos'
POSTS_PER_PAGE = 3


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
        else:
            messages_to_flash.append(('Произошла непредвиденная ошибка при добавлении фотографий', 'error'))
    return messages_to_flash


class ParkDatabase:
    def __init__(self, db):
        self.db = db

    def get_posts(self, page: int):
        conn = psycopg2.connect(
                dbname="wakepark",
                user="postgres",
                host="localhost",
                password="tibobe78"
            )
        cur = conn.cursor()
        if cur:
            try:
                query = f"SELECT * FROM posts " \
                        f"ORDER BY pubdate " \
                        f"OFFSET {(page - 1) * POSTS_PER_PAGE} ROWS " \
                        f"FETCH NEXT {POSTS_PER_PAGE} ROWS ONLY;"
                cur.execute(query)
                res = cur.fetchall()
                if res:
                    return res
            except psycopg2.Error as err:
                print(err)
            finally:
                cur.close()
                conn.close()
        return []

    def get_total_pages(self):
        conn = psycopg2.connect(
                dbname="wakepark",
                user="postgres",
                host="localhost",
                password="tibobe78"
            )
        cur = conn.cursor()
        if cur:
            try:
                query = f"SELECT COUNT(*) FROM posts;"
                cur.execute(query)
                res = cur.fetchall()

                if res:
                    ans = ceil(res[0][0] / POSTS_PER_PAGE)
                    return ans
            except psycopg2.Error as err:
                print(err)
            finally:
                cur.close()
                conn.close()
        return -1
