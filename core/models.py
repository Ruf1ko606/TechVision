# core/models.py

from django.db import models
from django.urls import reverse

class Advantage(models.Model):
    title = models.CharField(max_length=100, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание")
    icon_class = models.CharField(max_length=50, blank=True, null=True, verbose_name="Класс иконки")

    class Meta:
        verbose_name = "Преимущество"
        verbose_name_plural = "Преимущества"

    def __str__(self):
        return self.title

class Service(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название услуги")
    short_description = models.TextField(verbose_name="Краткое описание")
    full_description = models.TextField(verbose_name="Полное описание", blank=True)
    image = models.ImageField(upload_to='services/', verbose_name="Изображение услуги")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="URL-адрес (slug)", null=True, blank=True)
    
    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

    def __str__(self):
        return self.title
        
    def get_absolute_url(self):
        return reverse('service_detail', kwargs={'slug': self.slug})

# РАСШИРЕННАЯ МОДЕЛЬ ПРОЕКТА
class Project(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название проекта")
    short_description = models.TextField(verbose_name="Краткое описание (для карточки)")
    image = models.ImageField(upload_to='projects/', verbose_name="Главное изображение")
    is_featured = models.BooleanField(default=False, verbose_name="Показывать на главной")
    service = models.ForeignKey(
        Service, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='projects', 
        verbose_name="Связанная услуга"
    )
    
    # ИЗМЕНЕНИЯ ЗДЕСЬ: Добавили null=True, blank=True ко всем новым полям
    slug = models.SlugField(max_length=220, unique=True, verbose_name="URL-адрес (slug)", null=True, blank=True)
    challenge = models.TextField(verbose_name="Задача клиента (The Challenge)", null=True, blank=True)
    solution = models.TextField(verbose_name="Наше решение (The Solution)", null=True, blank=True)
    outcome = models.TextField(verbose_name="Результат (The Outcome)", null=True, blank=True)
    
    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"

    def __str__(self):
        return self.title
        
    def get_absolute_url(self):
        # Добавляем проверку, чтобы сайт не падал, если slug еще не задан
        if self.slug:
            return reverse('project_detail', kwargs={'slug': self.slug})
        return "#"

# НОВАЯ МОДЕЛЬ ДЛЯ ОТЗЫВОВ К ПРОЕКТАМ
class Testimonial(models.Model):
    project = models.OneToOneField('Project', on_delete=models.CASCADE, related_name='testimonial', verbose_name="Проект")
    author_name = models.CharField(max_length=100, verbose_name="Имя автора отзыва")
    author_position = models.CharField(max_length=100, verbose_name="Должность, компания")
    text = models.TextField(verbose_name="Текст отзыва")
    
    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return f"Отзыв от {self.author_name} к проекту {self.project.title}"

# НОВАЯ МОДЕЛЬ ДЛЯ ГАЛЕРЕИ ИЗОБРАЖЕНИЙ ПРОЕКТА
class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='gallery_images', verbose_name="Проект")
    image = models.ImageField(upload_to='projects/gallery/', verbose_name="Изображение")
    caption = models.CharField(max_length=200, blank=True, verbose_name="Подпись к изображению")

    class Meta:
        verbose_name = "Изображение галереи"
        verbose_name_plural = "Изображения галереи"

class ContactMessage(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    email = models.EmailField(verbose_name="E-mail")
    message = models.TextField(verbose_name="Сообщение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата обращения")

    class Meta:
        verbose_name = "Сообщение с формы обратной связи"
        verbose_name_plural = "Сообщения с формы обратной связи"

    def __str__(self):
        return f"{self.name} ({self.email}) - {self.created_at}"
    
# Скопируй и добавь этот класс в конец файла core/models.py

class ConsultationRequest(models.Model):
    # Поля, которые заполняет пользователь
    full_name = models.CharField(max_length=200, verbose_name="Имя и Отчество")
    company_name = models.CharField(max_length=200, verbose_name="Название компании")
    phone_number = models.CharField(max_length=20, verbose_name="Номер телефона")
    email = models.EmailField(verbose_name="Email")
    
    # Сюда мы АВТОМАТИЧЕСКИ запишем, с какой услуги пришла заявка
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Запрошенная услуга")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата заявки")
    is_processed = models.BooleanField(default=False, verbose_name="Заявка обработана")

    class Meta:
        verbose_name = "Заявка на консультацию"
        verbose_name_plural = "Заявки на консультацию"
        ordering = ['-created_at']

    def __str__(self):
        service_title = self.service.title if self.service else 'Не указана'
        return f"Заявка от {self.full_name} ({self.company_name}) по услуге '{service_title}'"

