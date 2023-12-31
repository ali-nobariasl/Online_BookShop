from django.contrib import admin

from .models import Payment, Order, OrderedBook

class OrderedBookInline(admin.TabularInline):
    model = OrderedBook
    readonly_fields = ('order','payment','user','Bookitem','quantity','price','amount')
    extra = 0
    
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number','name','order_placed_to','phone','email','total','payment_method','status','is_ordered']
    inlines = [OrderedBookInline]


admin.site.register(Payment)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderedBook)