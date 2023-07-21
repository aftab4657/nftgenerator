from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class LogInForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

class UploadFileForm(forms.Form):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))

class GenerateNFTsForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True, max_length=254, initial="")
    symbol = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'hidden': True}), max_length=254, initial='NA')
    description = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True, max_length=254, initial="")
    sellerfee = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control' , 'hidden': True}), required=True, max_length=254, initial="2")
    externalurl = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'hidden': True}), required=True, max_length=254, initial="NA")

    collectionname = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'hidden': True}), required=True, max_length=254, initial="NA")
    collectionfamily = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'hidden': True}), required=True, max_length=254, initial="NA")
    creatoraddress = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'hidden': True}), required=True, max_length=254, initial="NA")
    creatorshare = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'hidden': True}), required=True, max_length=254, initial="100")
    totalnfts = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True, max_length=254, initial="")
    nfts_path_input = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', '': True, 'id': 'nftsPaths_input', 'hidden': True}), required=True, max_length=254)
    nfts_path_output = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', '': True, 'id': 'nftsPaths_output', 'hidden': True}), required=True, max_length=254)
    task_id = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', '': True, 'id': 'task_id', 'hidden': True}), required=True, max_length=254)

class GenerateNFTsForm_defaul_value(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True, max_length=254, initial="AftabAnsari")
    symbol = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True, max_length=254, initial='AK')
    description = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True, max_length=254, initial="THis is description")
    sellerfee = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True, max_length=254, initial="20")
    externalurl = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True, max_length=254, initial="external url")

    collectionname = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True, max_length=254, initial="Ansari Collection")
    collectionfamily = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True, max_length=254, initial="Ansari Family")
    creatoraddress = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True, max_length=254, initial="sdfdksfsdjkfdsjkhfdshjkfds")
    creatorshare = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True, max_length=254, initial="100")
    totalnfts = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True, max_length=254, initial="20")
    nfts_path_input = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', '': True, 'id': 'nftsPaths_input',}), required=True, max_length=254)
    nfts_path_output = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', '': True, 'id': 'nftsPaths_output'}), required=True, max_length=254)
    task_id = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', '': True, 'id': 'task_id'}), required=True, max_length=254)