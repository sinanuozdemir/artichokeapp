import random
from django import forms
from dashboard.models import User, Website
import stripe
import sendgrid
import string

sg = sendgrid.SendGridClient('sinan.u.ozdemir', 'tier5beta')
stripe.api_key = "sk_test_elQ4skcmjHt34fVtK0YX7f5q"


class AuthenticationForm(forms.Form):
    """
    Login form
    """
    email = forms.EmailField(widget=forms.widgets.TextInput(attrs={'type' : 'email', 'placeholder': 'Enter email', 'name': 'email'}))
    password = forms.CharField(widget=forms.widgets.PasswordInput(attrs={'type' : 'password', 'placeholder': 'Enter password', 'name': 'password'}))

    class Meta:
        fields = ['email', 'password']
        
class RegistrationForm(forms.ModelForm):
    """
    Form for registering a new account.
    """
    email = forms.EmailField(required=True, widget=forms.widgets.TextInput(attrs={'id' : 'email', 'placeholder': 'Email', 'name': 'email', 'required':''}))
    CHOICES = (('1', 'First',), ('2', 'Second',))
    name =  forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'id' : 'name', 'placeholder': 'Name', 'name': 'name', 'required':''}))
    phone =  forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'id' : 'phone', 'placeholder': 'Phone Number', 'name': 'phone', 'required':''}))
    password =  forms.CharField(required=True, widget=forms.widgets.PasswordInput(attrs={'id' : 'pw', 'placeholder': 'Password', 'name': 'pw', 'required':''}))
    website =  forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'type': 'url', 'id': 'website', 'name' : 'website', 'placeholder': 'Website', 'required':''}), label = "Website")
    sex_CHOICES=[('male','Male'),
         ('female','Female')]
    gender = forms.ChoiceField(choices=sex_CHOICES, widget=forms.RadioSelect(attrs={'name': 'gender', 'id': 'genderOne'}))
    person_CHOICES=[('personal','Personal'),
         ('company','Company')]
    type_of_entity = forms.ChoiceField(choices=person_CHOICES, widget=forms.RadioSelect(attrs={'name': 'type_of_entity', 'id': 'RadioOne'}))
    class Meta:
        model = User
        fields = ['email', 'password', 'website', 'name', 'gender', 'type_of_entity']

    def clean(self):
        """
        Verifies that the values entered into the password fields match

        NOTE: Errors here will appear in ``non_field_errors()`` because it applies to more than one field.
        """
        cleaned_data = super(RegistrationForm, self).clean()
        return self.cleaned_data

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.type_of_entity = self.cleaned_data['type_of_entity']
        user.gender = self.cleaned_data['gender']
        user.twitter_available_for_stats = 10000
        message = sendgrid.Mail()
        message.set_from('yourfriends@legionanalytics.com')
        message.add_to(self.cleaned_data['email'])
        message.set_subject('Welcome to Legion Analytics!')
        message.set_html('Body')
        message.set_text('Body')
        message.add_filter('templates', 'enable', '1')
        message.add_filter('templates', 'template_id', 'a8d45317-2468-4819-bcc3-61e8e8107e18')
        status, msg = sg.send(message)
        customer = stripe.Customer.create(
            description = self.cleaned_data['email'],
            plan = 'Free Plan')
        user.stripe_id = customer.id
        if commit:
            user.save()
        w = Website(address=self.cleaned_data['website'], user = user)
        w.save()
        return user

  
class RegistrationFormTier5(forms.ModelForm):
    """
    Form for registering a new account.
    """
    email = forms.EmailField(required=True, widget=forms.widgets.EmailInput(attrs={'id' : 'email', 'class':'inF', 'placeholder': 'Email', 'name': 'email', 'required':''}))
    phone =  forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'id' : 'phone',  'class':'inF', 'pattern':'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})', 'placeholder': 'Phone Number', 'name': 'phone', 'required':''}))
    name =  forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'id' : 'name', 'class':'inF', 'placeholder': 'Name', 'name': 'name', 'required':''}))
    password =  forms.CharField(required=True, widget=forms.widgets.PasswordInput(attrs={'id' : 'pw', 'class':'inF', 'placeholder': 'Password', 'name': 'pw', 'required':''}))
    website =  forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'type': 'url', 'id': 'website', 'class':'inF', 'name' : 'website', 'placeholder': 'Website', 'required':''}), label = "Website")
    company_name =  forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'id' : 'company_name', 'placeholder': 'Company', 'class':'inF', 'name': 'company_name', 'required':''}))
    class Meta:
        model = User
        fields = ['email', 'password', 'website', 'name', 'company_name']

    def clean(self):
        """
        Verifies that the values entered into the password fields match

        NOTE: Errors here will appear in ``non_field_errors()`` because it applies to more than one field.
        """
        cleaned_data = super(RegistrationFormTier5, self).clean()
        return self.cleaned_data

    def save(self, commit=True):
        user = super(RegistrationFormTier5, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.company_name = self.cleaned_data['company_name']
        user.phone = self.cleaned_data['phone']
        chars = string.ascii_letters
        random_code = ''.join(random.choice(chars) for i in range(7))
        user.referral_token = random_code
        user.twitter_available_for_stats = 10000
        message = sendgrid.Mail()
        message.set_from('yourfriends@legionanalytics.com')
        message.add_to(self.cleaned_data['email'])
        message.set_subject('Welcome to Legion Analytics!')
        message.set_html('Body')
        message.set_text('Body')
        message.add_filter('templates', 'enable', '1')
        message.add_filter('templates', 'template_id', 'a8d45317-2468-4819-bcc3-61e8e8107e18')
        status, msg = sg.send(message)
        customer = stripe.Customer.create(
            description = self.cleaned_data['email'],
            plan = 'Free Plan')
        user.stripe_id = customer.id
        if commit:
            user.save()
        w = Website(address=self.cleaned_data['website'], user = user)
        w.save()
        return user