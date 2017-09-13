from django.db import models
from django.urls import reverse
# User是一个自带的模型类，里面是用户的字段
from django.contrib.auth.models import User
import markdown
from django.utils.html import strip_tags

class Category(models.Model):#分类
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

class Tag(models.Model):#标签
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

class Post(models.Model):#文章
    title = models.CharField(max_length=64)
    body = models.TextField()
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()
    # 摘要
    excerpt = models.CharField(max_length=256,blank=True)

    # 关系
    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag,blank=True)

    author = models.ForeignKey(User)

    # 文章阅读量
    views = models.PositiveIntegerField(default=0)
    def save(self,*args,**kwargs):
        if not self.excerpt:
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
        self.excerpt = strip_tags(md.convert(self.body))[:54]
        super(Post,self).save(*args,**kwargs)
    def increase_views(self):
        self.views+=1
        self.save(update_fields=['views'])

    # 看不到的属性：comment_set

    class Meta:
        ordering = ['-created_time','-modified_time']

    def get_absolute_url(self):
        #使用reverse函数，生成一个url，例如 post / 1
        return reverse('blog:detail',kwargs={'pk':self.pk}) #

    def __str__(self):
        return self.title


