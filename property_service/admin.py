from django.contrib import admin
from .models import Property


# Register your models here.
class PropertyAdmin(admin.ModelAdmin):
    using = "default"
    list_display = (
        "id",
        "agent",
        "title",
        "slug",
    )
    list_display_links = (
        "id",
        "agent",
        "title",
        "slug",
    )
    list_filter = ("agent",)
    search_fields = (
        "title",
        "description",
        "address",
        "property_type",
        "price",
    )
    list_per_page = 15

    def save_model(self, request, obj, form, change):
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        obj.delete(using=self.using)

    def get_queryset(self, request):
        return super().get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        return super().formfield_for_foreignkey(
            db_field, request, using=self.using, **kwargs
        )

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        return super().formfield_for_manytomany(
            db_field, request, using=self.using, **kwargs
        )


admin.site.register(Property, PropertyAdmin)
