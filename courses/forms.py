# encoding: utf-8
"""
@author: Sunmouren
@contact: sunxuechao1024@gmail.com
@time: 2019/2/8 22:12
@desc: 
"""
from django import forms


class SearchForm(forms.Form):
    query = forms.CharField()
