from django import forms
from .models import Product, HashTag

class ProductForm(forms.ModelForm):
    hashtags_str = forms.CharField(required=False)
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
    class Meta:
        model = Product
        fields = ['title', 'description', 'image', 'hashtags_str']
        
    def save(self, commit=True):
        product = super().save(commit=False)
        
        if self.user:
            product.user = self.user
            
        if commit:
            product.save()
        
        hashtags_input = self.cleaned_data.get('hashtags_str','')
        hashtag_list = [h for h in hashtags_input.replace(',',' ').split() if h]
        new_hashtags = []
        for ht in hashtag_list:
            ht_obj, created = HasgTag.objects.get_or_create(name=ht)
            new_hashtags.appenmd(ht_obj)
            
        product.hashtags.set(new_hashtags)
        
        if not commit:
            product.save()
            
        return product