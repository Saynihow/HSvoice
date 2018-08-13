# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2018-08-11 13:55
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(upload_to='images', verbose_name='圖片')),
                ('title', models.TextField(default='image', max_length=50, verbose_name='卡片名稱')),
                ('description', models.TextField(verbose_name='說說這張卡片帶給你甚麼')),
                ('manavalue', models.CharField(default=0, max_length=10, verbose_name='水晶值')),
                ('attackvalue', models.CharField(blank=True, max_length=10, verbose_name='攻擊值')),
                ('bloodvalue', models.CharField(blank=True, max_length=10, verbose_name='血量')),
                ('version', models.CharField(choices=[('經典', '經典'), ('基本', '基本'), ('安戈洛歷險記', '安戈洛歷險記'), ('冰封王座', '冰封王座'), ('狗頭人與地下城', '狗頭人與地下城'), ('黑巫森林', ' 黑巫森林'), ('哥哥打地地', '哥哥打地地 '), ('銀白聯賽', '銀白聯賽 '), ('古神碎碎念', '古神碎碎念'), ('加基森風雲', ' 加基森風雲'), ('納克薩瑪斯', '納克薩瑪斯'), ('勇闖黑石山', ' 勇闖黑石山'), ('探險者協會', '探險者協會'), ('夜夜卡拉贊', '夜夜卡拉贊'), ('競技場', '競技場'), ('爆爆計畫', '爆爆計畫')], max_length=30, verbose_name='卡片版本')),
                ('race', models.CharField(blank=True, choices=[('龍類', '龍類'), ('魚人', '魚人'), ('野獸', '野獸'), ('海盜', '海盜'), ('惡魔', '惡魔'), ('圖騰', '圖騰'), ('機械', '機械'), ('元素', '元素'), ('全部', '全部')], max_length=10, verbose_name='種族')),
                ('profession', models.CharField(choices=[('中立', '中立'), ('獵人', '獵人'), ('法師', '法師'), ('聖騎', '聖騎'), ('牧師', '牧師'), ('盜賊', '盜賊'), ('薩滿', '薩滿'), ('術士', '術士'), ('戰士', '戰士'), ('德魯伊', '德魯伊')], max_length=10, verbose_name='職業')),
                ('publish', models.DateTimeField(default=django.utils.timezone.now, verbose_name='上傳時間')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hs_images', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-publish',),
            },
        ),
        migrations.CreateModel(
            name='Voice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_type', models.CharField(choices=[('登場', '登場'), ('進攻', '進攻'), ('死亡', '死亡')], max_length=10, verbose_name='語音類型')),
                ('audio_file', models.FileField(upload_to='voice', verbose_name='語音檔案')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('publish', models.DateTimeField(default=django.utils.timezone.now, verbose_name='上傳時間')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hearthstone.Image', verbose_name='連結圖片')),
            ],
        ),
    ]