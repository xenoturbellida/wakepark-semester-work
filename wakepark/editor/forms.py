from flask_wtf import FlaskForm
from wtforms import MultipleFileField, StringField, SubmitField, TextAreaField
from wtforms.validators import Optional, ValidationError, DataRequired


class Extension:
    def __init__(self, message=None):
        self.allowed_extensions = ['jpg', 'png']
        if not message:
            message = 'Расширение фотографий должно быть .jpg или .png'
        self.message = message

    def __call__(self, form, field):
        for file in field.data:
            ext = file.rsplit('.', 1)[1]
            if ext not in self.allowed_extensions:
                raise ValidationError(self.message)


extension = Extension


class AddPostForm(FlaskForm):
    title = StringField(u'Заголовок', validators=[DataRequired()])
    content = TextAreaField()
    photos = MultipleFileField(u'Приложите фото', validators=[Optional(), extension()])
    submit = SubmitField(u'Опубликовать')
