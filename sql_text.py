from www import orm
from www.WEB import User,Blog,Comment

def test():
    yield from orm.create_pool(user='www-data',password='www-data',database='awesome')

    u=User(name='Test',email='306965405@.com',passwd='123456',image='about-blank')

    yield from u.save()

for x in test():
    pass