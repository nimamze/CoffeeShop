from django import forms


class CartAddForm(forms.Form):
	quantity = forms.IntegerField(min_value=1, max_value=9)

class CommentFrom(forms.Form):
	text = forms.CharField(widget=forms.Textarea)
	score = forms.IntegerField(min_value=0, max_value=5)