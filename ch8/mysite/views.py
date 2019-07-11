from django.shortcuts import render
from django.core.mail import send_mail
from mysite import models, forms
from ch8 import settings

# Create your views here.
def index(request, pid=None, del_pass=None):
    posts = models.Post.objects.filter(enabled=True).order_by('-pub_time')[:30]
    moods = models.Mood.objects.all()
    try:
        user_id = request.GET['user_id']
        user_pass = request.GET['user_pass']
        user_mood = request.GET['mood']
        user_post = request.GET['user_post']
    except:
        user_id = None
        message = '如要張貼訊息，則每一個欄位都要填呦！'
    
    if del_pass and pid:
        try:
            post = models.Post.objects.get(id=pid)
        except:
            post = None
        
        if post:
            if post.del_pass == del_pass:
                post.delete()
                message = '資料刪除成功'
            else:
                message = '密碼錯誤'
    elif user_id != None:
        mood = models.Mood.objects.get(status=user_mood)
        post = models.Post.objects.create(mood=mood, nickname=user_id, del_pass=user_pass, message=user_post)
        post.save()
        message = '成功儲存！請記得你的編輯密碼[{}]！，訊息須經審查後才會顯示。'.format(user_pass)

    return render(request, 'index.html', locals())


def listing(request):
    posts = models.Post.objects.filter(enabled=True).order_by('-pub_time')[:150]
    moods = models.Mood.objects.all()
    
    return render(request, 'listing.html', locals())

def posting(request):
    moods = models.Mood.objects.all()
    try:
        user_id = request.GET['user_id']
        user_pass = request.GET['user_pass']
        user_mood = request.GET['mood']
        user_post = request.GET['user_post']
    except:
        user_id = None
        message = '如要張貼訊息，則每一個欄位都要填呦！'

    if user_id != None:
        mood = models.Mood.objects.get(status=user_mood)
        post = models.Post.objects.create(mood=mood, nickname=user_id, del_pass=user_pass, message=user_post)
        post.save()
        message = '成功儲存！請記得你的編輯密碼[{}]！，訊息須經審查後才會顯示。'.format(user_pass)

    return render(request, 'posting.html', locals())


def contact(request):
    if request.method == 'POST':
        form = forms.ContactForm(request.POST)
        if form.is_valid():
            message = '感謝您的來信。'
            user_name = form.cleaned_data['user_name']
            user_city = form.cleaned_data['user_city']
            user_school = form.cleaned_data['user_school']
            user_email = form.cleaned_data['user_email']
            user_message = form.cleaned_data['user_message']

            send_title = "來自【來自不吐不快】網站的網友意見"
            send_body = f'網友姓名：{user_name}\n 居住城市：{user_city}\n 是否在學：{user_school}\n 反應意見：如下{user_message}'
            send_mail(
                    send_title,
                    send_body,
                    settings.EMAIL_HOST_USER,
                    [user_email],
                    fail_silently=False,
                    )
        else:
            message = '請檢查您輸入的資訊是否正確！'
    else:
        form = forms.ContactForm()

    return render(request, 'contact.html', locals())