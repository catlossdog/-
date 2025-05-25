import os
import django

# 设置 Django 项目的 settings 模块
# 这里的 'football_project.settings' 假设你的项目设置文件在 football_project/settings.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'football_project.settings')

# 加载 Django 环境
django.setup()


import random
from django.utils import timezone
from django.db import IntegrityError # 用于处理可能的重复报名错误
from django.db.models import Count # 用于验证统计人数

# 导入你的模型
from football.models import User, Match, MatchRegistration

# --- 设置要创建的数据量 ---
NUM_USERS_TO_CREATE = 20
NUM_MATCHES_TO_CREATE = 15
MAX_REGISTRATIONS_PER_MATCH = 15 # 每个活动最多有多少用户报名

# --- 存储创建的对象以便后续关联 ---
created_users = []
created_matches = []
created_registrations = []

print(f"--- 开始创建 {NUM_USERS_TO_CREATE} 个用户 ---")
for i in range(NUM_USERS_TO_CREATE):
    account = f'testuser{i+1:03d}' # 生成如 testuser001, testuser002... 的账号
    nickname = f'球迷_{i+1}'
    password = f'pass{i+1}' # *** 警告：这里是明文密码，仅用于简单毕设测试！ ***

    try:
        user = User.objects.create(account=account, nickname=nickname, password=password)
        created_users.append(user)
        # print(f"创建用户: {account}")
    except IntegrityError:
        print(f"警告: 用户账号 {account} 已存在，跳过创建。")
        try:
             # 如果已存在，尝试获取已存在的用户，以便后续使用
            user = User.objects.get(account=account)
            if user not in created_users: # 避免重复添加
                 created_users.append(user)
        except User.DoesNotExist:
            pass # 实在找不到就算了

print(f"--- 已创建/获取 {len(created_users)} 个用户 ---")

if not created_users:
    print("错误：未能创建任何用户，无法创建活动和报名！请检查 User 模型和数据库。")
else:
    print(f"--- 开始创建 {NUM_MATCHES_TO_CREATE} 个约战活动 ---")
    # 约战主题和地点列表
    match_titles = [
        "周末公园约战", "周中夜场野球", "室内五人制", "沙滩足球", "人工草场挑战赛",
        "城市联赛热身", "老友足球局", "青年队训练赛", "女生专属足球", "混合足球赛"
    ]
    match_locations = [
        "绿茵公园大球场", "学校体育场", "XXX室内足球馆", "YYY沙滩足球场", "ZZZ人工草皮",
        "市中心足球场A", "郊区球场B", "新区训练基地", "大学城体育中心", "市民健身广场"
    ]

    for i in range(NUM_MATCHES_TO_CREATE):
        title = random.choice(match_titles) + f" - {i+1}" # 标题加个序号以区分
        description = f"这是一场关于 {title} 的精彩活动详情。"
        location = random.choice(match_locations)
        # 活动时间：从现在起未来 1 到 30 天内的随机时间
        future_days = random.randint(1, 30)
        future_hours = random.randint(9, 21) # 早上9点到晚上9点之间
        future_minutes = random.choice([0, 15, 30, 45])
        match_datetime = timezone.now() + timezone.timedelta(days=future_days, hours=future_hours, minutes=future_minutes)

        creator = random.choice(created_users) # 从已创建用户中随机选一个作为创建者
        required_players = random.randint(10, 22) # 随机目标人数 (如 10 到 22 人)

        try:
            match = Match.objects.create(
                title=title,
                description=description,
                location=location,
                datetime=match_datetime,
                creator=creator,
                required_players=required_players
                
            )
            created_matches.append(match)
            # print(f"创建活动: {title} (ID: {match.id})")
        except Exception as e:
            print(f"警告: 创建活动失败 - {title}: {e}")


    print(f"--- 已创建 {len(created_matches)} 个约战活动 ---")

    if not created_matches:
         print("错误：未能创建任何活动，无法创建报名记录！")
    else:
        print(f"--- 开始创建报名记录 ---")
        for match in created_matches:
            # 为每个活动，随机选择一些用户进行报名
            num_registrations = random.randint(0, MAX_REGISTRATIONS_PER_MATCH) # 随机报名人数，不超过最大值
            # 确保选择的用户数量不超过已创建的用户总数和活动的required_players
            num_registrations = min(num_registrations, len(created_users), match.required_players + 5) # 可以稍微超过 required_players
            
            # 随机打乱用户列表，然后选择前 num_registrations 个用户
            users_to_register = random.sample(created_users, num_registrations) # 无放回抽样，确保用户不重复

            for user in users_to_register:
                try:
                    registration = MatchRegistration.objects.create(match=match, player=user)
                    created_registrations.append(registration)
                    # print(f" - {user.nickname} 报名 {match.title}")
                except IntegrityError:
                    # 如果因为 unique_together 约束报错，说明该用户已经报过名了，跳过
                    # print(f" - {user.nickname} 已报名 {match.title}，跳过。")
                    pass # 忽略重复报名错误
                except Exception as e:
                    print(f"警告: 创建报名记录失败 - 用户 {user.account} 报名活动 {match.title}: {e}")

        print(f"--- 已创建 {len(created_registrations)} 条报名记录 ---")

print("\n--- 数据插入完成 ---")
