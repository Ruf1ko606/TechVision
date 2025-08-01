# core/admin.py

from django.contrib import admin
from .models import Advantage, Project, Service, ContactMessage, Testimonial, ProjectImage, ConsultationRequest # Добавь ConsultationRequest

@admin.register(Advantage)
class AdvantageAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon_class')
    search_fields = ('title',)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created_at")
    search_fields = ("name", "email", "message")
    list_filter = ("created_at",)

# Инлайн для изображений проекта
class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1 # Количество пустых форм для добавления новых изображений

# Инлайн для отзыва к проекту (OneToOne связь)
class TestimonialInline(admin.StackedInline):
    model = Testimonial
    can_delete = False # Отзыв тесно связан с проектом, не позволяем удалять его отдельно
    verbose_name = "Отзыв клиента"
    verbose_name_plural = "Отзыв клиента"

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = [TestimonialInline, ProjectImageInline] # Добавляем инлайны
    list_display = ('title', 'service', 'is_featured')
    list_filter = ('is_featured', 'service')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)} # Автоматическое заполнение slug на основе заголовка

@admin.register(ConsultationRequest)
class ConsultationRequestAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'company_name', 'service', 'created_at', 'is_processed')
    list_filter = ('is_processed', 'created_at', 'service')
    search_fields = ('full_name', 'company_name', 'email', 'phone_number')
    list_editable = ('is_processed',)
