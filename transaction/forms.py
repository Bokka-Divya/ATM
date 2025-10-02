from django import forms
class LoginForm(forms.ModelForm):
	'''account_number=forms.IntegerField()
	pin_number=forms.IntegerField()'''
	pin = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ['account_number', 'pin']
