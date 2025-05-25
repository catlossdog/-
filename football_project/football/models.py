from django.db import models

# Create your models here.

class User(models.Model):
    account = models.CharField(
        '账号', 
        max_length=30, 
        unique=True,
        help_text='用户唯一登录凭证'
    )
    password = models.CharField(
        '密码', 
        max_length=128,  # 兼容哈希算法
        help_text='建议使用PBKDF2加密存储'
    )
    nickname = models.CharField(
        '昵称', 
        max_length=50, 
        default='新用户',
        blank=True
    )

class Article(models.Model):
    author = models.ForeignKey(  # 修改字段名和关联对象
        User, 
        to_field='account',  # 关联用户账号
        on_delete=models.CASCADE,
        verbose_name='作者'
    )
    topic = models.CharField('主题', max_length=100)
    content = models.TextField('内容')
    likes = models.PositiveIntegerField('点赞数', default=0)
    pub_time = models.DateTimeField('发表时间', auto_now_add=True)


class Comment(models.Model):
    article = models.ForeignKey(
        Article, 
        on_delete=models.CASCADE,
        related_name='comments'  # 新增反向查询名称[1](@ref)
    )
    content = models.TextField('评论内容')
    commenter = models.ForeignKey(  # 新增评论者关联[4](@ref)
        User,
        to_field='account',
        on_delete=models.CASCADE,
        verbose_name='评论者'
    )
    comment_time = models.DateTimeField('评论时间', auto_now_add=True)


# Match 模型 - 包含活动基本信息和目标人数
class Match(models.Model):
    title = models.CharField('活动标题', max_length=100)
    description = models.TextField('活动详情')
    location = models.CharField('活动地点', max_length=200)
    datetime = models.DateTimeField('活动开始时间')
    creator = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name='创建者'
    )
    required_players = models.PositiveIntegerField('目标人数') # <--- 实现“目标人数”
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    def __str__(self):
        return self.title

# MatchRegistration 模型 - 记录用户和活动的报名关系
class MatchRegistration(models.Model):
    match = models.ForeignKey(
        Match,
        on_delete=models.CASCADE,
        related_name='registrations', # 从 Match 对象反向获取报名记录用这个名字
        verbose_name='约战活动'
    )
    player = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='match_registrations', # 从 User 对象反向获取报名记录用这个名字
        verbose_name='报名用户'
    )
    # === 新增报名时的姓名和电话字段 ===
    name = models.CharField('姓名', max_length=100, default='匿名用户') # 添加 default
    phone = models.CharField('电话号码', max_length=20, default='无电话') # 添加 default
    # ==============================
    registered_at = models.DateTimeField('报名时间', auto_now_add=True)

    class Meta:
        unique_together = ('match', 'player') # 确保一个用户只能报名同一个活动一次

    def __str__(self):
        # 修正 __str__ 方法，包含姓名和活动标题
        return f"{self.name} ({self.player.nickname}) 报名了 {self.match.title}"

