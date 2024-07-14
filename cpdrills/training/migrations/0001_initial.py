# Generated by Django 4.0.1 on 2022-01-08 04:41

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OnlineJudge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('code', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=256)),
                ('rating', models.IntegerField()),
                ('link', models.TextField()),
                ('ordering_code', models.PositiveSmallIntegerField(default=3000)),
            ],
        ),
        migrations.CreateModel(
            name='ProblemTopic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('problem_topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subcategoryOf', to='training.problemtopic')),
                ('problems', models.ManyToManyField(to='training.Problem')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='ProblemStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('solve_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('solve_duration', models.FloatField(default=-1)),
                ('speed_attempt', models.BooleanField(default=False)),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='training.problem')),
                ('userprofile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.userprofile')),
            ],
            options={
                'ordering': ['solve_time'],
            },
        ),
        migrations.AddField(
            model_name='problem',
            name='solvers',
            field=models.ManyToManyField(through='training.ProblemStatus', to='accounts.UserProfile'),
        ),
        migrations.AddField(
            model_name='problem',
            name='source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='training.onlinejudge'),
        ),
    ]