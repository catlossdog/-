# generate_data.py
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'football_project.settings')
import django
django.setup()

from django.contrib.auth.hashers import make_password
from faker import Faker
from football.models import User, Article, Comment

fake = Faker('zh_CN')

def create_base_data():
    # 批量创建用户
    users = [
        User(
            account=f'user_{i}',
            password=make_password(f'Test@123{i}'),  # PBKDF2加密[5](@ref)
            nickname=fake.name()
        )
        for i in range(1, 101)  # 生成100个用户
    ]
    User.objects.bulk_create(users, batch_size=50)
    
    # 批量创建文章（每个用户3篇）
    articles = []
    for user in User.objects.all():
        for _ in range(3):
            articles.append(Article(
                author=user,
                topic=fake.sentence(nb_words=6),
                content=fake.text(max_nb_chars=500),
                likes=fake.random_int(min=0, max=1000)
            ))
    Article.objects.bulk_create(articles, batch_size=100)
    
    # 批量创建评论（每篇文章5条）
    comments = []
    for article in Article.objects.all():
        for _ in range(5):
            commenter = User.objects.order_by('?').first()  # 随机选择评论者
            comments.append(Comment(
                article=article,
                commenter=commenter,
                content=fake.paragraph(nb_sentences=3)
            ))
    Comment.objects.bulk_create(comments, batch_size=200)

if __name__ == "__main__":
    create_base_data()
    print("成功生成：用户×100 文章×300 评论×1500")