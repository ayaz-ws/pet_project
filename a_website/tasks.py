from django.template import Template, Context
from django.core.mail import send_mail
from decouple import config

from a_core.celery import app
from a_website.models import Post
from a_users.models import Profile

REPORT_TEMPLATE = """ 
                        Просмотры твоих записей в блоге: 
                        {% for post in posts %} 
                        Запись "{{ post.title }}": просмотрен {{ post.view_count }} раз(а) | 
                        {% endfor %} 
                    """


@app.task
def send_view_count_report():
    for profile in Profile.objects.filter(is_verify=True, informate_about_views="True"):
        posts = Post.objects.filter(author=profile.user)
        if not posts:
            continue
        from_email = config("EMAIL_HOST_USER")
        template = Template(REPORT_TEMPLATE)
        send_mail(
            template.render(context=Context({"posts": posts})),
            from_email,
            [profile.user.email],
            fail_silently=False,
        )
