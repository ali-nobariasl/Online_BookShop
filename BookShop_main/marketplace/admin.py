from django.contrib import admin


from .models import Cart


class CartModel(admin.ModelAdmin):
    list_display = ('user','bookitem','quantity','updated_at')


admin.site.register(Cart,CartModel)
