from django import forms


class CartAddForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1,
        initial=1,
        label="تعداد",
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "تعداد مورد نظر را وارد کنید",
            }
        ),
    )


class CommentForm(forms.Form):
    text = forms.CharField(
        label="متن نظر",
        max_length=500,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "نظر خود را وارد کنید...",
            }
        ),
    )
    score = forms.IntegerField(
        min_value=1,
        max_value=5,
        label="امتیاز",
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "امتیاز ۱ تا ۵",
            }
        ),
    )
