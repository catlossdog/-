from django.contrib import admin
from football.models import User, Article, Comment, Match, MatchRegistration

admin.site.register(User)
admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(Match)
admin.site.register(MatchRegistration)
# Register your models here.
