from django import forms
from rango.models import Category, Page, UserProfile
from django.contrib.auth.models import User

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter Category name")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Category
        fields = ('name',)

class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="Enter the page title")
    url = forms.URLField(max_length=200, help_text="Enter the url to the page")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        if url and not url.startswith('http://'):
            url = 'http://' + url
            cleaned_data['url'] = url

            return cleaned_data

    class Meta:
        model = Page
        exclude = ('category',)


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password', 'placeholder': '******' }))
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'type':'text', 'placeholder': 'johndoe' }))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control', 'type':'email', 'placeholder': 'johndoe@xyz.com' }))
    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    website = forms.URLField(required=False, widget=forms.TextInput(attrs={'class':'form-control', 'type':'text', 'placeholder': 'http://www.xyz.com' }))
    picture = forms.ImageField(required=False)
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')
