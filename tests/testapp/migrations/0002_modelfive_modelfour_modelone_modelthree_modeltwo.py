# Generated by Django 3.2 on 2023-03-06 12:37

from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0004_alter_taggeditem_content_type_alter_taggeditem_tag'),
        ('testapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModelThree',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ModelTwo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_three', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='model_two', to='testapp.modelthree')),
                ('tags', taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ModelOne',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_two', models.ManyToManyField(blank=True, related_name='model_one', to='testapp.ModelTwo')),
                ('tags', taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ModelFour',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_three', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='model_four', to='testapp.modelthree')),
                ('tags', taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ModelFive',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_two', models.ManyToManyField(blank=True, related_name='model_five', to='testapp.ModelThree')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
