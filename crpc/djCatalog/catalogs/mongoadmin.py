# -*- coding: utf-8 -*-
from mongonaut.sites import MongoAdmin
from catalogs.models import Brand
from catalogs.models import Dept
from catalogs.models import Tag

class CustomizeAdmin(MongoAdmin):
    # Searches on the title field. Displayed in the DocumentListView.
    search_fields = ('title',)

    # provide following fields for view in the DocumentListView
    list_fields = ('title',)
    
    def has_add_permission(self, request):
        """ Can add this object """
#        return request.user.is_authenticated and request.user.is_active and request.user.is_staff)
        return True

    def has_delete_permission(self, request):
        """ Can delete this object """
#        return request.user.is_authenticated and request.user.is_active and request.user.is_admin()
        return True

    def has_edit_permission(self, request):
        """ Can edit this object """
#        return request.user.is_authenticated and request.user.is_active and request.user.is_staff)
        return True

    def has_view_permission(self, request):
        """ Can view this object """
#        return request.user.is_authenticated and request.user.is_active
        return True

class BrandAdmin(CustomizeAdmin):
    list_fields = ('title', 'title_edit', 'title_checked', 'alias', 'keywords', 'url',  'url_checked', 'level', 'blurb', 'done', 'is_delete')
    search_fields = ('title',)

class DeptAdmin(CustomizeAdmin):
    list_fields = ('title',)
    search_fields = ('title',)

class TagAdmin(CustomizeAdmin):
    list_fields = ('title', 'dept',)
    search_fields = ('title',)


# Instantiate the MongoAdmin class
# Then attach the mongoadmin to the model
Brand.mongoadmin = BrandAdmin()
Dept.mongoadmin = DeptAdmin()
Tag.mongoadmin = TagAdmin()