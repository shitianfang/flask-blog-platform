from faker import Faker
import click
from main.start import app,db
from main.models import Post


fake=Faker('zh_CN')


#使用 python -m flask make-post
@app.cli.command()
def make_post():
    for i in range(50):
        db.session.add(Post(
            title=fake.text(max_nb_chars=16, ext_word_list=None),
            body=fake.text(max_nb_chars=200, ext_word_list=None),
            recommend=True,
            blog_id=6
            ))
        db.session.commit()

