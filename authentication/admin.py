from django.contrib import admin
from . models import(
    User, 
    Agent,
    Profile, 
    Function, 
    Assignment,
    Rate,
    Station,
    Usage,
    Buy_Mode
)
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class UserModelAdmin(BaseUserAdmin):
  # The fields to be used in displaying the User model.
  # These override the definitions on the base UserModelAdmin
  # that reference specific fields on auth.User.
  list_display = ('id', 'email', 'names', 'phone_number', 'is_admin', 'staff')
  list_filter = ('is_admin', 'staff',)
  fieldsets = (
      ('User Credentials', {'fields': ('email', 'password')}),
      ('Personal info', {'fields': ('names', 'phone_number')}),
      ('Permissions', {'fields': ('is_admin', 'is_active')}),
  )
  # add_fieldsets is not a standard ModelAdmin attribute. UserModelAdmin
  # overrides get_fieldsets to use this attribute when creating a user.
  add_fieldsets = (
      (None, {
          'classes': ('wide',),
          'fields': ('email', 'names', 'phone_number', 'password1', 'password2', 'staff'),
      }),
  )
  search_fields = ('email',)
  ordering = ('email', 'id')
  filter_horizontal = ()

# Register your models here.
admin.site.register(User, UserModelAdmin)
admin.site.register(Agent)
admin.site.register(Profile)
admin.site.register(Function)
admin.site.register(Assignment)
admin.site.register(Rate)
admin.site.register(Station)
admin.site.register(Usage)
admin.site.register(Buy_Mode)

