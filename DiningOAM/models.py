# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup)
    permission = models.ForeignKey('AuthPermission')

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType')
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser)
    group = models.ForeignKey(AuthGroup)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser)
    permission = models.ForeignKey(AuthPermission)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', blank=True, null=True)
    user = models.ForeignKey(AuthUser)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class TblBanner(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    banner_url = models.CharField(max_length=300)
    link_url = models.CharField(max_length=300)
    show_order = models.IntegerField(blank=True, null=True)
    in_use = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tbl_banner'


class TblBill(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    user_id = models.CharField(max_length=36)
    user_location = models.CharField(max_length=300, blank=True, null=True)
    bill_totalling = models.IntegerField()
    add_time = models.DateTimeField()
    pay_time = models.DateTimeField(blank=True, null=True)
    bill_state = models.IntegerField()
    bill_content = models.CharField(max_length=300, blank=True, null=True)
    ensure_send_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_bill'


class TblBillMeal(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    bill_id = models.CharField(max_length=36)
    meal_in_house_id = models.CharField(max_length=36)
    buy_count = models.IntegerField()
    add_time = models.DateTimeField()
    meal_name = models.CharField(max_length=300)
    meal_url = models.CharField(max_length=300)
    meal_price = models.FloatField()

    class Meta:
        managed = False
        db_table = 'tbl_bill_meal'


class TblHouse(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    name = models.CharField(max_length=300)
    latitude = models.FloatField()
    longitude = models.FloatField()
    location = models.CharField(max_length=300)
    add_time = models.DateTimeField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_house'


class TblJudgeMeal(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    bill_id = models.CharField(max_length=36)
    meal_in_house = models.CharField(max_length=36)
    user_id = models.CharField(max_length=36)
    user_name = models.CharField(max_length=300, blank=True, null=True)
    judge_meal = models.IntegerField()
    judge_speed = models.IntegerField()
    judge_service = models.IntegerField()
    add_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tbl_judge_meal'


class TblLocation(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    location = models.CharField(max_length=300)
    add_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tbl_location'


class TblMeal(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    catogory_id = models.CharField(max_length=36)
    name = models.CharField(max_length=100)
    avatar_url = models.CharField(max_length=300)
    detail_url = models.CharField(max_length=300)
    detail_content = models.CharField(max_length=900)
    sold_count = models.IntegerField()
    judge_count = models.IntegerField()
    add_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tbl_meal'


class TblMealCategory(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    name = models.CharField(max_length=100)
    change_time = models.DateTimeField(blank=True, null=True)
    show_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tbl_meal_category'


class TblMealInHouse(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    meal_id = models.CharField(max_length=36)
    house_id = models.CharField(max_length=36)
    category_id = models.CharField(max_length=36)
    name = models.CharField(max_length=100)
    avatar_url = models.CharField(max_length=300)
    detail_url = models.CharField(max_length=300)
    detail_content = models.CharField(max_length=900)
    sold_count = models.IntegerField()
    judge_count = models.IntegerField()
    meal_price = models.FloatField()
    last_count = models.IntegerField()
    add_time = models.DateTimeField()
    category_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tbl_meal_in_house'


class TblUser(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    username = models.CharField(max_length=300)
    sex = models.IntegerField(blank=True, null=True)
    birthday = models.DateField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    add_time = models.DateTimeField(blank=True, null=True)
    user_location = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_user'


class TblUserMoney(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    money = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tbl_user_money'


class TblUserMoneyChange(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    user_id = models.CharField(max_length=36)
    left_money = models.IntegerField()
    action_content = models.CharField(max_length=300)

    class Meta:
        managed = False
        db_table = 'tbl_user_money_change'
