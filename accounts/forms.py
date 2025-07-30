from django.contrib.auth.forms import UserCreationForm
from .models import Customer

class CustomUserCreationForm(UserCreationForm):
    
    class Meta:
        
        model = Customer
        fields = ('phone', 'email','first_name','last_name','image')
