from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
import os.path


class Image(models.Model):
    img = models.ImageField(upload_to='images', verbose_name="圖片")    # 图片文件,上传至images文件夹
    title = models.TextField(max_length=50, default='image', verbose_name='卡片名稱')    # 由於title會出現在後台編輯名稱即(__str__) 而之前未輸入的title不能空白 我預設為 image
    author = models.ForeignKey(User,
                               related_name='hs_images')
    description = models.TextField(verbose_name='說說這張卡片帶給你甚麼')            # 图片描述, 长文本类型
    manavalue = models.CharField(max_length=10, default=0, verbose_name='水晶值')
    attackvalue = models.CharField(max_length=10, blank=True, verbose_name='攻擊值')
    bloodvalue = models.CharField(max_length=10, blank=True, verbose_name='血量')
    GENERATED_OF_VERSION_CHOICES = (
        ('經典', '經典'),      #第一个参数是真正的model参数，#第二个参数则是方便人们理解阅读
        ('基本', '基本'),
        ('安戈洛歷險記', '安戈洛歷險記'),
        ('冰封王座', '冰封王座'),
        ('狗頭人與地下城','狗頭人與地下城'),
        ('黑巫森林',' 黑巫森林'),
        ('哥哥打地地','哥哥打地地 '),
        ('銀白聯賽', '銀白聯賽 '),
        ('古神碎碎念', '古神碎碎念'),
        ('加基森風雲', ' 加基森風雲'),
        ('納克薩瑪斯', '納克薩瑪斯'),
        ('勇闖黑石山', ' 勇闖黑石山'),
        ('探險者協會', '探險者協會'),
        ('夜夜卡拉贊', '夜夜卡拉贊'),
        ('競技場', '競技場'),
        ('爆爆計畫','爆爆計畫'),
    )
    version = models.CharField(max_length=30, choices=GENERATED_OF_VERSION_CHOICES, verbose_name='卡片版本')
    RACE_CHOICES = (
        ('龍類','龍類'),
        ('魚人', '魚人'),
        ('野獸', '野獸'),
        ('海盜', '海盜'),
        ('惡魔', '惡魔'),
        ('圖騰', '圖騰'),
        ('機械', '機械'),
        ('元素', '元素'),
        ('全部','全部'),
    )
    race = models.CharField(max_length=10, choices=RACE_CHOICES, blank=True, verbose_name='種族')
    PROFESSION_CHOICES = (
        ('中立', '中立'),
        ('獵人', '獵人'),
        ('法師', '法師'),
        ('聖騎', '聖騎'),
        ('牧師', '牧師'),
        ('盜賊', '盜賊'),
        ('薩滿', '薩滿'),
        ('術士', '術士'),
        ('戰士', '戰士'),
        ('德魯伊', '德魯伊'),
    )
    profession = models.CharField(max_length=10, choices=PROFESSION_CHOICES, verbose_name='職業')
    publish = models.DateTimeField(default=timezone.now, verbose_name='上傳時間')
    created = models.DateTimeField(auto_now_add=True)  # 创建时间,自动添加当前时间
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('hearthstone:index_detail',                 #連結到url name
                       args=[self.publish.year,
                             self.publish.strftime('%m'),
                             self.publish.strftime('%d'),
                             self.title])

class Voice(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE, verbose_name='連結圖片')  #many-to-one 一張image會有多種voice
    FILE_TYPE_CHOICES = (
        ('登場', '登場'),
        ('進攻', '進攻'),
        ('死亡', '死亡'),
    )
    file_type = models.CharField(max_length=10, choices=FILE_TYPE_CHOICES, verbose_name='語音類型')
    audio_file = models.FileField(upload_to='voice', verbose_name='語音檔案')
    author = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    publish = models.DateTimeField(default=timezone.now, verbose_name='上傳時間')
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.image.title + '-' + self.file_type

