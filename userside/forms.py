from django import forms
from .models import Product
from django.shortcuts import render,redirect


class ProductForm(forms.ModelForm):
    class Meta:
        model=Product
        fields='__all__'
        widgets = {
            'productname': forms.TextInput(attrs={
                'class': 'form-control block w-full px-4 py-2 m-3 text-gray-900 bg-gray-50 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Enter product name',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control block w-full px-4 py-2 m-3 text-gray-900 bg-gray-50 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Enter description',
                'rows': 4,
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control block w-full px-4 py-2 m-3 text-gray-900 bg-gray-50 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Enter price',
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control block w-full px-4 py-2 m-3 text-gray-900 bg-gray-50 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500',
            }),
        }