from django.contrib.auth.models import User


def bulk_create_users():
    user_list = [
        User(username=f'user_{i}', email=f'user_{i}@example.com')
        for i in range(1, 50)
    ]
    print(user_list)
    # User.objects.bulk_create(user_list)

# 缺少执行入口
if __name__ == "__main__":
    import os, django
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "football_project.settings")
    django.setup()
    
    bulk_create_users() 
