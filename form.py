from django import forms

class Mybook(forms.Form):
	name = forms.CharField()
	author = forms.CharField()
	data = forms.CharField()
