# football/forms.py
from django import forms
from .models import Match # 导入 Match 模型
from django.forms.widgets import DateTimeInput # 导入日期时间输入框 widget
from django.forms.widgets import TextInput # 导入文本输入框 widget
from django.forms.widgets import Textarea # 导入文本域 widget
from .models import Article # 导入 Article 模型

# ... (RegistrationForm 如果存在，保持不变) ...

# 新增创建约战的表单
class MatchForm(forms.ModelForm):
    # 可选：定制 datetime 字段的输入方式，但默认的 DateTimeInput 也可以用
    # datetime = forms.DateTimeField(
    #     label='活动开始时间',
    #     widget=DateTimeInput(attrs={'type': 'datetime-local'}) # 使用 HTML5 datetime-local 输入框
    # )

    class Meta:
        model = Match
        # fields = '__all__' # 如果你想包含所有字段，但 creator 我们在视图中设置
        # fields = ['title', 'description', 'location', 'datetime', 'required_players', 'creator'] # 如果要在表单里选择创建者
        fields = ['title', 'description', 'location', 'datetime', 'required_players'] # 我们在视图中自动设置创建者

        labels = { # 设置字段的中文标签
            'title': '活动标题',
            'description': '活动详情',
            'location': '活动地点',
            'datetime': '活动时间',
            'required_players': '目标人数',
            # 'creator': '创建者', # 如果不在 fields 里，这里也不需要
        }

        widgets = { # 可选：为字段指定 HTML widget 和属性
            'datetime': DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}), # 使用 datetime-local 类型和 Bootstrap 类
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}), # 文本域行数和 Bootstrap 类
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'required_players': forms.NumberInput(attrs={'class': 'form-control', 'min': 2}), # 限定最小人数为 2
        }

# 新增报名模态框的 Form
class SignupModalForm(forms.Form):
    # 这个 Form 只用于接收姓名和电话，不直接对应模型
    name = forms.CharField(label='姓名', max_length=100, widget=TextInput(attrs={'class': 'form-control', 'placeholder': '请输入您的姓名'}))
    phone = forms.CharField(label='电话号码', max_length=20, widget=TextInput(attrs={'class': 'form-control', 'placeholder': '请输入您的电话号码'}))
    # 约战 ID 不在 Form 里，我们通过视图直接获取

# 新增发表帖子的表单
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        # fields = '__all__' # 如果你想包含所有字段，但 author 和 pub_time 我们在视图中设置
        fields = ['topic', 'content'] # 只包含需要用户输入的字段

        labels = { # 设置字段的中文标签
            'topic': '帖子标题',
            'content': '帖子内容',
            # 'author': '作者', # 如果不在 fields 里，这里也不需要
        }

        widgets = { # 可选：为字段指定 HTML widget 和属性
            'topic': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入帖子标题'}),
            'content': Textarea(attrs={'rows': 10, 'class': 'form-control', 'placeholder': '请输入帖子内容'}),
        }