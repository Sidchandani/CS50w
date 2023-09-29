from django.contrib import admin

# Register your models here.
from .models import Product,Bid,User,Comment

class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ('product_id',)

admin.site.register(Product,ProductAdmin)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(User)


# sidd - nothing (admin)
# sid - nothing@75
# wid - nothing@75
