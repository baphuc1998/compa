# Generated by Django 2.2.5 on 2019-09-19 07:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('GFood', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.IntegerField(null=True)),
                ('create_at', models.DateTimeField(auto_now=True, null=True)),
                ('status', models.CharField(max_length=15, null=True)),
                ('address', models.CharField(max_length=100, null=True)),
                ('is_deleted', models.BooleanField(default=False, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='cart_of_user', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('total', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('detail', models.CharField(max_length=100)),
                ('is_deleted', models.BooleanField(default=False)),
                ('create_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('detail', models.CharField(max_length=100)),
                ('price', models.IntegerField()),
                ('image', models.TextField()),
                ('is_deleted', models.BooleanField(default=False)),
                ('create_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(default='In stock', max_length=50, null=True)),
                ('category', models.ManyToManyField(null=True, related_name='product_in_category', to='GFood.Category')),
            ],
        ),
        migrations.AddField(
            model_name='customuser',
            name='account_stripe',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='address',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='id_stripe',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='image',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='phone',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='token_fcm',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.CharField(max_length=30)),
                ('is_deleted', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('star', models.IntegerField(null=True)),
                ('comment', models.CharField(max_length=100, null=True)),
                ('status', models.BooleanField(default=False)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='review_of_product', to='GFood.Product')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='review_of_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('detail', models.CharField(max_length=100)),
                ('image', models.TextField()),
                ('is_active', models.BooleanField(default=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('create_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='res_of_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='restaurant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_in_res', to='GFood.Restaurant'),
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(null=True)),
                ('price', models.IntegerField(null=True)),
                ('create_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(default='waiting', max_length=15, null=True)),
                ('bill', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='item_in_bill', to='GFood.Bill')),
                ('cart', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='item_in_cart', to='GFood.Cart')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='item_in_product', to='GFood.Product')),
            ],
        ),
        migrations.AddField(
            model_name='bill',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bill_of_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
