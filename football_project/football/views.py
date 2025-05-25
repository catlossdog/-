from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from football.models import Article, Comment, User ,Match ,MatchRegistration
from django.shortcuts import redirect
from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import Count  # 新增导入
from .forms import MatchForm # 导入 MatchForm
from .forms import MatchForm, SignupModalForm, ArticleForm # 导入 MatchForm, SignupModalForm, ArticleForm
from django.db.models import F, Count # 确保导入 Count
from django.db import IntegrityError # 导入 IntegrityError 用于处理重复报名错误

from .forms import MatchForm, SignupModalForm # 导入 MatchForm, SignupModalForm

 


# Create your views here.

def login(request):
    if request.method == 'POST':
        # 获取用户提交的账号和密码
        # 注意：login.html 表单中账号的 name 是 "username"
        account = request.POST.get('username')
        password = request.POST.get('password') # 获取明文密码
        print("hello")

        # --- 简单的登录逻辑（不安全！） ---
        try:
            print(f"用户尝试登录: 账号={account}, 密码={password}")
            # 在 User 模型中查找账号和明文密码都匹配的用户
            # 这是一个非常不安全的操作，因为它直接比较明文密码
            user = User.objects.get(account=account, password=password)

            # 如果找到用户，说明账号密码匹配，登录成功
            print(f"用户登录成功: 账号={account}")
            request.session['logged_in_account'] = user.account

            # TODO: 对于稍复杂的需求，这里通常会建立用户会话 (session)
            # 但对于最简单的毕设演示，我们直接重定向到主页
            # 假设你的主页 URL 是 '/home/' 并且在 urls.py 中命名为 'index'
            return redirect('index') # 使用 URL name 进行重定向

        except User.DoesNotExist:
            # 如果没有找到匹配的用户，说明账号不存在或密码错误
            print(f"登录失败: 账号={account}, 密码错误或账号不存在")
            error_message = '账号或密码错误。'

            # 登录失败，重新渲染登录页面，并传递错误信息和用户输入的账号
            return render(request, 'login.html', {
                'error_message': error_message,
                'username': account # 将用户输入的账号传回模板，方便用户
            })

    else:
        # 如果是 GET 请求（第一次访问登录页），直接渲染空表单
        return render(request, 'login.html')


def register(request):
    return render(request,'register.html')
# 修改 article_detail 视图来使用 session 中的用户账号
def article_detail(request, article_id):
    logged_in_account = request.session.get('logged_in_account')
    current_user = None
    if logged_in_account:
        try:
            current_user = User.objects.get(account=logged_in_account)
        except User.DoesNotExist:
            # Session 中的用户不存在，可能是数据问题，清除 session
            del request.session['logged_in_account']
            current_user = None
            print(f"Session 中的账号 '{logged_in_account}' 在数据库中不存在！")
    # ===================================


    article = get_object_or_404(Article, pk=article_id)
    comments = article.comments.all().order_by('comment_time')

    if request.method == 'POST':
        # === 从 session 中获取评论用户 ===
        logged_in_account = request.session.get('logged_in_account')

        if not logged_in_account:
            # 如果 session 中没有账号，说明用户没有通过你的简化登录流程“登录”
            # 可以重定向到登录页，或者给个错误提示
            print("用户未登录，尝试发表评论。")
            # 这里选择重定向到登录页
            # 可选：可以在重定向时带一个消息提示用户登录
            return redirect('login') # 假设你的登录 URL name 是 'login'


        try:
            # 根据 session 中的账号找到对应的用户对象
            commenter_user = User.objects.get(account=logged_in_account)
            print(f"找到评论用户：{commenter_user.account}")

        except User.DoesNotExist:
            # session 中的账号在数据库中不存在，这通常不应该发生，可能是数据不同步
            print(f"Session 中的账号 '{logged_in_account}' 在数据库中不存在！清除 session 并重定向到登录。")
            # 清除 session 中的登录标记
            del request.session['logged_in_account']
            return redirect('login')

        # ==================================

        comment_content = request.POST.get('comment_content', '').strip()

        if not comment_content:
             return render(request, 'article_detail.html', {
                'article': article,
                'comments': comments,
                'error_message': '评论内容不能为空。'
             })

        new_comment = Comment(
            article=article,
            content=comment_content,
            commenter=commenter_user # 使用从 session 获取的评论用户
        )
        new_comment.save()

        print(f"新评论已由用户 '{commenter_user.account}' 添加到文章 ID {article_id}")

        return redirect('article_detail', article_id=article_id)

    else: # GET 请求
        return render(request, 'article_detail.html', {
            'article': article,
            'comments': comments,
            'error_message': None
        })



def submit(request):
    if request.method == 'POST':
        nickname = request.POST.get('nickname')
        account = request.POST.get('account')
        password = request.POST.get('password') # 获取用户输入的密码

        # --- 简单的注册逻辑 ---

        # 检查账号是否已存在（因为模型中 account 设置了 unique=True，但提前检查可以返回更友好的错误）
        if User.objects.filter(account=account).exists():
            # 如果账号已存在，重新渲染注册页面并传递错误信息
            return render(request, 'register.html', {
                'error_message': '该账号已被注册，请尝试其他账号。',
                'nickname': nickname, # 传递回用户输入的其他数据，方便用户
                'account': account,
                # 不返回 password，出于安全考虑（尽管是明文）
            })

        # 如果账号不存在，创建新的用户对象
        user = User(nickname=nickname, account=account, password=password) # 直接保存明文密码
        user.save() # 保存到数据库

        print(f"用户注册成功: 昵称={nickname}, 账号={account}") # 打印成功信息到控制台

        # 注册成功后，重定向到登录页面（假设登录页是根路径 '/'）
        # 确保 urls.py 中 '/' 映射到了 login 视图
        return redirect('/')

    else:
        # 如果是 GET 请求直接访问 /register/submit/，通常不应该发生，重定向回注册页
        return redirect('/register/')

def index(request):
    logged_in_account = request.session.get('logged_in_account')
    current_user = None
    if logged_in_account:
        try:
            current_user = User.objects.get(account=logged_in_account)
        except User.DoesNotExist:
            # Session 中的用户不存在，可能是数据问题，清除 session
            del request.session['logged_in_account']
            current_user = None
            print(f"Session 中的账号 '{logged_in_account}' 在数据库中不存在！")
    # ===================================
    # 3.渲染模板
    return render(request, 'index.html',{
        'current_user': current_user # 传递当前用户，可以在模板中显示欢迎信息等
    })

def discussion_list(request):
    logged_in_account = request.session.get('logged_in_account')
    current_user = None
    if logged_in_account:
        try:
            current_user = User.objects.get(account=logged_in_account)
        except User.DoesNotExist:
            # Session 中的用户不存在，可能是数据问题，清除 session
            del request.session['logged_in_account']
            current_user = None
            print(f"Session 中的账号 '{logged_in_account}' 在数据库中不存在！")
    # ===================================
    # 获取所有文章（包含预加载优化）
    articles = Article.objects.all()[:30]
    return render(request, 'Comment.html', {'articles': articles,
                'current_user': current_user })

def like_article(request):
    article_id = request.POST.get('id')
    article_id = int(article_id)
    print("文章id",article_id,type(article_id))
    
    # if not article_id.isdigit():
    #     return JsonResponse({'status': 'error', 'message': '非法参数'}, status=400)
    try:
        # 原子操作更新点赞数[8](@ref)
        # likes=F('likes') + 1是原子操作，直接在数据库中更新likes字段
        article = Article.objects.get(id=article_id)
        print("文章喜欢数",article.likes,type(article.likes))
        Article.objects.filter(id=article_id).update(likes=F('likes') + 1)
        updated_article = Article.objects.get(id=article_id)
        return JsonResponse({
            'status': 'success',
            'likes': updated_article.likes
        })
    except Article.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': '文章不存在'}, status=404)


# 赛事直播视图
def live_streams_view(request):
    logged_in_account = request.session.get('logged_in_account')
    current_user = None
    if logged_in_account:
        try:
            current_user = User.objects.get(account=logged_in_account)
        except User.DoesNotExist:
            # Session 中的用户不存在，可能是数据问题，清除 session
            del request.session['logged_in_account']
            current_user = None
            print(f"Session 中的账号 '{logged_in_account}' 在数据库中不存在！")
    # ===================================
    return render(request, 'live_streams.html',{'current_user': current_user})


# 足球文化 - 简史视图
def culture_history_view(request):
    # 静态内容直接在模板中写即可，视图不需要传递额外数据
    return render(request, 'culture_history.html')

# 大数据
def bigdata_view(request):
    logged_in_account = request.session.get('logged_in_account')
    current_user = None
    if logged_in_account:
        try:
            current_user = User.objects.get(account=logged_in_account)
        except User.DoesNotExist:
            # Session 中的用户不存在，可能是数据问题，清除 session
            del request.session['logged_in_account']
            current_user = None
            print(f"Session 中的账号 '{logged_in_account}' 在数据库中不存在！")
    # ===================================
    return render(request, 'bigdata.html',{'current_user': current_user})


""" 新增 """

# 线上约战视图 - 列表显示和处理来自重定向的反馈
def battle_view(request):
    # 获取当前登录用户（如果存在）
    logged_in_account = request.session.get('logged_in_account')
    current_user = None
    if logged_in_account:
        try:
            current_user = User.objects.get(account=logged_in_account)
        except User.DoesNotExist:
            print(f"Session 中的账号 '{logged_in_account}' 在数据库中不存在！清除 session。")
            del request.session['logged_in_account']
            current_user = None

    feedback_message = None # 用于存储报名成功或失败的反馈信息
    feedback_status = 'info' # 'success' 或 'danger'

    # --- 处理来自重定向的反馈信息（如果URL中有查询参数） ---
    status = request.GET.get('status')
    message = request.GET.get('message')
    match_title = request.GET.get('match_title', '该活动') # 获取活动标题用于显示
    if status == 'success':
        feedback_message = f"报名成功！您已报名参加活动: {match_title}"
        feedback_status = 'success'
    elif status == 'error':
        feedback_message = f"报名失败：{message or '发生未知错误。'} ({match_title})"
        feedback_status = 'danger'
    # =======================================================


    # 获取所有约战活动，并计算每个活动的报名人数
    # 使用 annotate 方法统计 related_name='registrations' 的数量
    matches = Match.objects.annotate(current_players=Count('registrations')).order_by('-created_at') # 按创建时间倒序排列

    # 准备数据列表，包含每个活动的详细信息、当前人数、目标人数以及当前用户是否已报名
    match_list_data = []
    for match in matches:
        is_signed_up = False
        if current_user:
            # 检查当前用户是否已报名该活动
            is_signed_up = MatchRegistration.objects.filter(match=match, player=current_user).exists()

        is_creator = False
        if current_user and match.creator == current_user:
             is_creator = True

        match_list_data.append({
            'match': match, # 原始 Match 对象
            'current_players': match.current_players if match.current_players is not None else 0, # 确保不是 None
            'is_signed_up': is_signed_up, # 当前用户是否已报名
            'is_creator': is_creator, # 当前用户是否为创建者
            'is_full': (match.current_players is not None and match.current_players >= match.required_players) # 判断是否已满
        })

    # 渲染模板，传递数据、反馈消息、以及一个空的报名表单实例用于模态框
    signup_form = SignupModalForm()
    return render(request, 'battle.html', {
        'match_list_data': match_list_data,
        'feedback_message': feedback_message,
        'feedback_status': feedback_status,
        'current_user': current_user,
        'signup_form': signup_form # 将报名表单实例传递给模板
    })

# 新增创建约战视图
def create_match_view(request):
    # === 检查用户是否登录 ===
    logged_in_account = request.session.get('logged_in_account')
    if not logged_in_account:
        # 如果未登录，重定向到登录页
        print("未登录用户尝试访问创建约战页面，重定向到登录页。")
        return redirect('/') # 或者你的登录 URL name 'login'

    try:
        current_user = User.objects.get(account=logged_in_account)
    except User.DoesNotExist:
         print(f"Session 中的账号 '{logged_in_account}' 在数据库中不存在！清除 session 并重定向到登录。")
         del request.session['logged_in_account']
         return redirect('/')

    # =======================

    if request.method == 'POST':
        form = MatchForm(request.POST)
        if form.is_valid():
            # 表单数据验证通过
            match = form.save(commit=False) # 先不保存到数据库
            match.creator = current_user # 设置活动的创建者为当前登录用户
            match.save() # 保存 Match 对象

            print(f"用户 '{current_user.account}' 创建了新约战: {match.title}")

            # 创建成功，重定向到约战列表页
            return redirect('/home/battle/') # 或者你的约战列表 URL name 'battle'

        else:
             # 表单无效，重新渲染页面，显示错误
             print("创建约战表单验证失败。")

    else: # GET 请求
        form = MatchForm() # 创建一个空表单实例

    # 渲染创建约战模板
    return render(request, 'create_match.html', {
        'form': form,
        'current_user': current_user # 传递当前用户，用于模板显示
    })


# 修改查看我的约战视图
def my_matches_view(request):
    # === 检查用户是否登录 ===
    logged_in_account = request.session.get('logged_in_account')
    if not logged_in_account:
        print("未登录用户尝试访问我的约战页面，重定向到登录页。")
        return redirect('/') # 或者你的登录 URL name 'login'

    try:
        current_user = User.objects.get(account=logged_in_account)
    except User.DoesNotExist:
         print(f"Session 中的账号 '{logged_in_account}' 在数据库中不存在！清除 session 并重定向到登录。")
         del request.session['logged_in_account']
         return redirect('/')

    # =======================

    # 获取当前用户的所有报名记录，按报名时间倒序
    # related_name='match_registrations' 在 MatchRegistration 模型中定义
    my_registrations = current_user.match_registrations.all().order_by('-registered_at')

    # 渲染我的约战模板
    return render(request, 'my_matches.html', {
        'my_registrations': my_registrations,
        'current_user': current_user
    })


# 新增处理报名模态框提交的视图
def battle_signup_submit(request):
    if request.method != 'POST':
        # 只处理 POST 请求，其他方法重定向回列表页
        return redirect('/home/battle/')

    # === 检查用户是否登录 ===
    logged_in_account = request.session.get('logged_in_account')
    if not logged_in_account:
        print("未登录用户尝试提交报名，重定向到登录页。")
        # 重定向到登录页，可以在URL中带一个 next 参数指回约战列表
        return redirect(f"/?next=/home/battle/") # 假设登录页是根路径

    try:
        current_user = User.objects.get(account=logged_in_account)
    except User.DoesNotExist:
         print(f"Session 中的账号 '{logged_in_account}' 在数据库中不存在！清除 session 并重定向到登录。")
         del request.session['logged_in_account']
         return redirect('/')
    # =======================

    # 获取模态框表单数据和约战 ID
    signup_form = SignupModalForm(request.POST)
    match_id = request.POST.get('match_id') # 从隐藏字段获取约战 ID

    if not match_id:
        print("报名提交失败：缺少活动 ID。")
        return redirect(f"/home/battle/?status=error&message={'缺少活动信息'}")


    try:
        match_id = int(match_id)
        match = get_object_or_404(Match, pk=match_id)
        match_title_encoded = match.title # 在重定向URL中使用，防止中文乱码，或者简单英文标题

        # === 检查是否为活动创建者（Requirement 1）===
        if match.creator == current_user:
            print(f"用户 '{current_user.account}' 尝试报名自己创建的活动 ID {match_id}")
            return redirect(f"/home/battle/?status=error&message={'不能报名自己发布的活动'}&match_title={match_title_encoded}")

        # 检查是否已报名（重复报名）
        if MatchRegistration.objects.filter(match=match, player=current_user).exists():
             print(f"用户 '{current_user.account}' 重复报名活动 ID {match_id}")
             return redirect(f"/home/battle/?status=error&message={'您已报名过此活动'}&match_title={match_title_encoded}")

        # 检查人数是否已满 (可选，根据需求判断满员后是否还能报名)
        current_players_count = MatchRegistration.objects.filter(match=match).count()
        if current_players_count >= match.required_players:
             print(f"用户 '{current_user.account}' 尝试报名已满的活动 ID {match_id}")
             return redirect(f"/home/battle/?status=error&message={'该活动人数已满'}&match_title={match_title_encoded}")


        # === 验证模态框中的姓名和电话字段 ===
        if signup_form.is_valid():
            name = signup_form.cleaned_data['name']
            phone = signup_form.cleaned_data['phone']

            # === 创建报名记录（包含姓名和电话）===
            registration = MatchRegistration.objects.create(
                match=match,
                player=current_user,
                name=name,
                phone=phone
            )
            print(f"用户 '{current_user.account}' 成功报名活动 ID {match_id} (姓名: {name}, 电话: {phone})")

            # 重定向回约战列表页，带上成功信息
            return redirect(f"/home/battle/?status=success&match_title={match_title_encoded}")

        else:
            # 模态框表单验证失败（姓名或电话格式问题等）
            # 对于模态框提交，通常是返回 JSON 错误，或者重定向回原页面带错误信息
            # 这里简化处理，重定向回列表页并提示表单错误 (不太友好，实际应用应改进)
             errors = signup_form.errors.as_text().replace('\n', ' ').replace('*', '').strip()
             print(f"报名模态框表单验证失败: {errors}")
             return redirect(f"/home/battle/?status=error&message={'姓名或电话格式错误'} ({errors[:50]}...)" ) # 截断错误信息

    except ValueError:
         print(f"报名提交失败：无效的活动 ID '{request.POST.get('match_id')}'。")
         return redirect(f"/home/battle/?status=error&message={'无效的活动信息'}")
    except Exception as e:
        print(f"报名提交失败，发生异常: {e}")
        return redirect(f"/home/battle/?status=error&message={'发生未知错误'} ({e})")


# 修改查看我报名的约战详情视图 (my_match_detail_view)，使其创建者也能访问
def my_match_detail_view(request, match_id):
     # === 检查用户是否登录 ===
    logged_in_account = request.session.get('logged_in_account')
    if not logged_in_account:
        print("未登录用户尝试访问我的约战详情页面，重定向到登录页。")
        return redirect('/') # 或者你的登录 URL name 'login'

    try:
        current_user = User.objects.get(account=logged_in_account)
    except User.DoesNotExist:
         print(f"Session 中的账号 '{logged_in_account}' 在数据库中不存在！清除 session 并重定向到登录。")
         del request.session['logged_in_account']
         return redirect('/')
    # =======================

    # 获取约战活动对象
    match = get_object_or_404(Match, pk=match_id)

    # === 修改权限检查：允许报名者 或 创建者 访问 ===
    is_registered = MatchRegistration.objects.filter(match=match, player=current_user).exists()
    is_creator = (match.creator == current_user)

    if not is_registered and not is_creator:
        print(f"用户 '{current_user.account}' 未报名也非创建者，尝试访问活动 ID {match_id} 的详情，拒绝访问。")
        # 重定向到我的约战列表或我发布的约战列表，并提示无权查看
        # 可以检查用户是否是创建者，如果是，重定向到我发布的列表；否则重定向到我报名的列表
        if Match.objects.filter(pk=match_id, creator=current_user).exists(): # 再次确认是否是创建者
             return redirect('/home/battle/my_matches/created/?status=error&message=您无权查看此约战详情') # 重定向到我发布的约战列表
        else:
             return redirect('/home/battle/my_matches/?status=error&message=您无权查看此约战详情') # 重定向到我报名的约战列表


    # === 获取该约战活动的所有报名记录，并预加载 player 信息 ===
    all_registrations = match.registrations.all().select_related('player').order_by('registered_at')


    # 渲染约战详情模板
    return render(request, 'my_match_detail.html', {
        'match': match, # 约战活动对象
        'all_registrations': all_registrations, # 所有报名记录列表
        'current_user': current_user, # 当前用户
        'is_creator': is_creator # 传递是否是创建者到模板，以便显示删除按钮
    })




# 新增查看我发布的约战视图
def my_created_matches_view(request):
    # === 检查用户是否登录 ===
    logged_in_account = request.session.get('logged_in_account')
    if not logged_in_account:
        print("未登录用户尝试访问我发布的约战页面，重定向到登录页。")
        return redirect('/') # 或者你的登录 URL name 'login'

    try:
        current_user = User.objects.get(account=logged_in_account)
    except User.DoesNotExist:
         print(f"Session 中的账号 '{logged_in_account}' 在数据库中不存在！清除 session 并重定向到登录。")
         del request.session['logged_in_account']
         return redirect('/')

    # =======================

    # 获取当前用户创建的所有约战活动，并计算每个活动的报名人数
    my_created_matches = Match.objects.filter(creator=current_user).annotate(
        current_players=Count('registrations') # 计算报名人数
        ).order_by('-created_at') # 按创建时间倒序

    # 渲染我发布的约战模板
    return render(request, 'my_created_matches.html', {
        'my_created_matches': my_created_matches,
        'current_user': current_user
    })


# 新增删除约战视图
def delete_match_view(request, match_id):
     # 只允许 POST 请求删除
    if request.method != 'POST':
        print("非 POST 请求尝试访问删除约战 URL，重定向。")
        return redirect('/home/battle/my_matches/created/') # 重定向到我发布的约战列表


    # === 检查用户是否登录 ===
    logged_in_account = request.session.get('logged_in_account')
    if not logged_in_account:
        print("未登录用户尝试删除约战，重定向到登录页。")
        return redirect('/') # 或者你的登录 URL name 'login'

    try:
        current_user = User.objects.get(account=logged_in_account)
    except User.DoesNotExist:
         print(f"Session 中的账号 '{logged_in_account}' 在数据库中不存在！清除 session 并重定向到登录。")
         del request.session['logged_in_account']
         return redirect('/')

    # =======================

    # 获取约战活动对象
    match = get_object_or_404(Match, pk=match_id)

    # === 检查当前用户是否为约战的创建者 ===
    if match.creator != current_user:
        print(f"用户 '{current_user.account}' 尝试删除非自己创建的活动 ID {match_id}，拒绝访问。")
        # 重定向回我发布的约战列表并提示无权删除
        return redirect('/home/battle/my_matches/created/?status=error&message=您无权删除此约战')

    # === 执行删除操作 ===
    match_title = match.title # 在删除前获取标题用于反馈信息
    try:
        match.delete()
        print(f"用户 '{current_user.account}' 成功删除了约战活动 ID {match_id}: {match_title}")
        # 删除成功，重定向回我发布的约战列表并带上成功信息
        return redirect(f"/home/battle/my_matches/created/?status=success&message=已成功删除约战活动: {match_title}")

    except Exception as e:
        print(f"用户 '{current_user.account}' 删除约战活动 ID {match_id} 失败: {e}")
        # 删除失败，重定向回我发布的约战列表并带上失败信息
        return redirect(f"/home/battle/my_matches/created/?status=error&message=删除约战失败: {e}")

'''新内容'''
# 新增足球文化介绍详情视图
def culture_detail_view(request):
    # 这个视图只渲染模板，不涉及数据库查询（因为内容硬编码在模板里）
    # 可以传递 current_user 给模板，用于头部导航显示
    logged_in_account = request.session.get('logged_in_account')
    current_user = None
    if logged_in_account:
        try:
            current_user = User.objects.get(account=logged_in_account)
        except User.DoesNotExist:
             print(f"Session 中的账号 '{logged_in_account}' 在数据库中不存在！清除 session。")
             del request.session['logged_in_account']
             current_user = None

    return render(request, 'culture_detail.html', {
        'current_user': current_user # 传递当前用户
    })


# 新增发表帖子视图
def create_article_view(request):
    # === 检查用户是否登录 ===
    logged_in_account = request.session.get('logged_in_account')
    if not logged_in_account:
        # 如果未登录，重定向到登录页
        print("未登录用户尝试访问发表帖子页面，重定向到登录页。")
        return redirect('/') # 或者你的登录 URL name 'login'

    try:
        current_user = User.objects.get(account=logged_in_account)
    except User.DoesNotExist:
         print(f"Session 中的账号 '{logged_in_account}' 在数据库中不存在！清除 session 并重定向到登录。")
         del request.session['logged_in_account']
         return redirect('/')

    # =======================

    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            # 表单数据验证通过
            article = form.save(commit=False) # 先不保存到数据库
            article.author = current_user # 设置帖子的作者为当前登录用户
            # pub_time 会在 save 时自动设置 auto_now_add=True
            article.likes = 0 # 新发帖子点赞数默认为 0

            article.save() # 保存 Article 对象

            print(f"用户 '{current_user.account}' 发表了新帖子: {article.topic}")

            # 发表成功，重定向到帖子详情页或讨论列表页
            # 重定向到刚刚创建的帖子详情页
            return redirect('/home/discuss/%d/' % article.id) # 或者你的文章详情 URL name 'article_detail' 和参数
            # 重定向回讨论列表页
            # return redirect('/home/discuss/') # 或者你的讨论列表 URL name 'discussion_list'

        else:
             # 表单无效，重新渲染页面，显示错误
             print("发表帖子表单验证失败。")

    else: # GET 请求
        form = ArticleForm() # 创建一个空表单实例

    # 渲染发表帖子模板
    return render(request, 'create_article.html', {
        'form': form,
        'current_user': current_user # 传递当前用户，用于模板显示
    })



