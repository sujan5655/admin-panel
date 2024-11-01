from django import forms
from .models import Property
class PropertyForm(forms.ModelForm):
  class Meta:
    model=Property
    fields=('name','description','price','location','is_available')
  
    def __init__(self, *args, **kwargs):
        super(PropertyForm, self).__init__(*args, **kwargs)
        
        # Example: Make specific fields optional
        self.fields['description'].required = False