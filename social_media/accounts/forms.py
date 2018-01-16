from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

# get_user_model returns the user model that is currently active in this model

class UserCreateForm(UserCreationForm):

    class Meta():
        #  these fields comes with the get_user_model
        fields = ('username','email','password1','password2')
        model = get_user_model

    # add labels my modifying __init__
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kargs)
        self.fields['username'].label = 'Display Name'
        self.fields['email'].label = 'Email Address'
