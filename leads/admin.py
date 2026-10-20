from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Lead, Activity, FollowUp, Customer


# =========================
# LEAD IMPORT / EXPORT RESOURCE
# =========================
class LeadResource(resources.ModelResource):

    class Meta:
        model = Lead
        fields = (
            'id',
            'name',
            'email',
            'phone',
            'company',
            'source',
            'status',
            'score',
            'assigned_to',
            'created_at',
            'updated_at',
        )
        export_order = fields
        import_id_fields = ('id',)
        skip_unchanged = True
        report_skipped = True


# =========================
# LEAD ADMIN WITH CSV IMPORT/EXPORT
# =========================
@admin.register(Lead)
class LeadAdmin(ImportExportModelAdmin):
    resource_class = LeadResource

    list_display = (
        'name',
        'email',
        'phone',
        'company',
        'source',
        'status',
        'score',
        'assigned_to',
        'created_at',
    )

    list_filter = ('status', 'source', 'assigned_to')

    search_fields = ('name', 'email', 'company', 'phone')

    list_editable = ('status', 'score')

    ordering = ('-created_at',)


# =========================
# ACTIVITY ADMIN
# =========================
@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('lead', 'activity_type', 'created_at')
    list_filter = ('activity_type', 'created_at')
    search_fields = ('lead__name', 'description')


# =========================
# FOLLOW-UP ADMIN
# =========================
@admin.register(FollowUp)
class FollowUpAdmin(admin.ModelAdmin):
    list_display = ('lead', 'scheduled_at', 'completed')
    list_filter = ('completed', 'scheduled_at')
    search_fields = ('lead__name',)


# =========================
# CUSTOMER ADMIN
# =========================
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('lead', 'converted_at')
    search_fields = ('lead__name', 'lead__email')