#coding:utf-8
from django import forms


class User(forms.Form):
    username = forms.CharField(max_length=6,error_messages={'required':'用户名不能为空'})
    password = forms.CharField(widget=forms.PasswordInput(),max_length=15,error_messages={'required':'密码不能为空'})






