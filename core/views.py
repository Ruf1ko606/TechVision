from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Advantage, Project, Service, ContactMessage, ConsultationRequest
from .forms import ContactForm, ConsultationForm

def index(request):
    advantages = Advantage.objects.all()
    featured_projects = Project.objects.filter(is_featured=True).select_related('service')
    context = { 'advantages': advantages, 'featured_projects': featured_projects }
    return render(request, 'core/index.html', context)

def services_view(request):
    services = Service.objects.all()
    context = { 'services': services }
    return render(request, 'core/services.html', context)

# --- ПОЛНОСТЬЮ ОБНОВЛЕННАЯ ФУНКЦИЯ ДЕТАЛЬНОЙ СТРАНИЦЫ УСЛУГИ ---
def service_detail_view(request, slug):
    service = get_object_or_404(Service, slug=slug)

    # Логика для обработки AJAX-запроса от модального окна консультации
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Переименовываем поля из JS, чтобы они соответствовали модели
        post_data = request.POST.copy()
        post_data['full_name'] = post_data.get('fullname')
        post_data['company_name'] = post_data.get('company')
        post_data['phone_number'] = post_data.get('phone')
        
        form = ConsultationForm(post_data)
        if form.is_valid():
            # Создаем объект, но не сохраняем в базу сразу
            consultation_request = form.save(commit=False)
            # Привязываем заявку к текущей услуге
            consultation_request.service = service
            # Теперь сохраняем
            consultation_request.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)

    # Стандартная логика для отображения страницы (GET-запрос)
    related_projects = service.projects.all()
    steps_data = {
        'razrabotka-kastomnyh-veb-servisov': [
            {'icon': 'fas fa-search', 'title': 'Бизнес-аналитика и ТЗ', 'desc': 'Глубоко изучаем ваши уникальные процессы, выявляем точки роста и составляем четкое техническое задание.'},
            {'icon': 'fas fa-drafting-compass', 'title': 'Архитектура и дизайн', 'desc': 'Проектируем надежную структуру продукта, создаем интерактивные прототипы и современный UI/UX.'},
            {'icon': 'fas fa-code', 'title': 'Разработка и интеграции', 'desc': 'Пишем чистый, масштабируемый код, подключая необходимые внешние системы и API для полной функциональности.'},
            {'icon': 'fas fa-rocket', 'title': 'Запуск и поддержка', 'desc': 'Разворачиваем сервис на сервере, проводим нагрузочные тесты и берем на себя дальнейшее развитие.'}
        ],
        'sozdanie-korporativnyh-sajtov-i-portalov': [
            {'icon': 'fas fa-briefcase', 'title': 'Анализ бизнес-задач', 'desc': 'Погружаемся в специфику вашей компании, выявляем ключевые сценарии использования для сотрудников и клиентов.'},
            {'icon': 'fas fa-palette', 'title': 'Прототипы и фирменный дизайн', 'desc': 'Создаем интуитивно понятный интерфейс, который отражает ваш бренд и решает поставленные задачи.'},
            {'icon': 'fas fa-cogs', 'title': 'Разработка и наполнение', 'desc': 'Реализуем сайт на современной платформе, добавляем ключевой функционал и помогаем с наполнением.'},
            {'icon': 'fas fa-bullhorn', 'title': 'SEO, запуск и обучение', 'desc': 'Оптимизируем сайт для поисковиков, обучаем вашу команду работе с админ-панелью и сопровождаем после запуска.'}
        ],
        'razrabotka-e-commerce-platform': [
            {'icon': 'fas fa-shopping-cart', 'title': 'Анализ рынка и конкурентов', 'desc': 'Изучаем вашу нишу, выявляем лучшие практики и точки роста для создания конкурентного преимущества.'},
            {'icon': 'fas fa-map-signs', 'title': 'Проектирование пути клиента', 'desc': 'Детализируем все сценарии покупателя, от каталога и корзины до удобной и безопасной оплаты.'},
            {'icon': 'fas fa-credit-card', 'title': 'Разработка и интеграции', 'desc': 'Интегрируем платформу с платежными системами, складами, CRM и службами доставки.'},
            {'icon': 'fas fa-check-circle', 'title': 'Тестирование и запуск', 'desc': 'Тщательно проверяем весь цикл покупки, дорабатываем под реальные сценарии и поддерживаем после релиза.'}
        ],
        'integraciya-s-vneshnimi-sistemami-api': [
            {'icon': 'fas fa-network-wired', 'title': 'Аудит ИТ-ландшафта', 'desc': 'Анализируем ваши текущие системы, чтобы определить оптимальные точки и методы для интеграции.'},
            {'icon': 'fas fa-file-alt', 'title': 'Проектирование обмена', 'desc': 'Готовим детальные схемы и протоколы обмена данными, обеспечивая безопасность и надежность.'},
            {'icon': 'fas fa-plug', 'title': 'Реализация и тестирование', 'desc': 'Пишем и настраиваем коннекторы, проводим полное тестирование для гарантии стабильной работы.'},
            {'icon': 'fas fa-power-off', 'title': 'Ввод в эксплуатацию', 'desc': 'Запускаем интеграцию в "боевом" режиме и настраиваем систему мониторинга для контроля стабильности.'}
        ],
        'tehnicheskaya-podderzhka-i-razvitie-proektov': [
            {'icon': 'fas fa-shield-alt', 'title': 'Аудит и приемка проекта', 'desc': 'Проводим полный технический аудит проекта, выявляем уязвимости и составляем план улучшений.'},
            {'icon': 'fas fa-life-ring', 'title': 'Стабилизация и поддержка', 'desc': 'Оперативно решаем критичные проблемы, обеспечиваем стабильную работу и резервное копирование.'},
            {'icon': 'fas fa-chart-line', 'title': 'Плановое развитие', 'desc': 'Внедряем новый функционал по вашему запросу, обновляем компоненты и улучшаем производительность.'},
            {'icon': 'fas fa-tasks', 'title': 'Отчетность и SLA', 'desc': 'Предоставляем прозрачную отчетность о проделанной работе и гарантируем соблюдение уровня сервиса (SLA).'}
        ],
        'it-konsalting-i-audit': [
            {'icon': 'fas fa-microscope', 'title': 'Диагностика бизнес-процессов', 'desc': 'Изучаем вашу ИТ-инфраструктуру, находим узкие места, неэффективные процессы и потенциальные риски.'},
            {'icon': 'fas fa-clipboard-check', 'title': 'Проведение аудита', 'desc': 'Глубоко анализируем архитектуру, безопасность, код и процессы разработки в вашей компании.'},
            {'icon': 'fas fa-lightbulb', 'title': 'Разработка стратегии', 'desc': 'Формируем подробный отчет с практическими рекомендациями и пошаговым планом цифровой трансформации.'},
            {'icon': 'fas fa-users-cog', 'title': 'Сопровождение внедрения', 'desc': 'Помогаем реализовать предложенные решения, обучаем команду и контролируем достижение ключевых метрик.'}
        ],
        'razrabotka-mobilnyh-prilozhenij': [
            {'icon': 'fas fa-mobile-alt', 'title': 'Исследование и ТЗ', 'desc': 'Изучаем вашу аудиторию и цели, формируем карту пользовательских путей и создаем детальную спецификацию.'},
            {'icon': 'fas fa-pencil-ruler', 'title': 'Прототипирование и UX/UI', 'desc': 'Создаем дизайн, ориентированный на удобство использования, и тестируем его на фокус-группах.'},
            {'icon': 'fab fa-apple', 'title': 'Разработка для iOS/Android', 'desc': 'Пишем нативное или кроссплатформенное приложение, которое работает в тесной связке с вашими веб-сервисами.'},
            {'icon': 'fas fa-upload', 'title': 'Публикация и аналитика', 'desc': 'Готовим и публикуем приложение в App Store и Google Play, настраиваем аналитику и занимаемся поддержкой.'}
        ]
    }

    process_steps = steps_data.get(service.slug, [])
    
    context = {
        'service': service,
        'related_projects': related_projects,
        'process_steps': process_steps
    }
    return render(request, 'core/service_detail.html', context)

def privacy_policy(request):
    return render(request, 'core/privacy_policy.html')

def user_agreement(request):
    return render(request, 'core/user_agreement.html')

def about_view(request):
    advantages = Advantage.objects.all()
    context = { 'advantages': advantages }
    return render(request, 'core/about.html', context)

def contacts_view(request):
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            if is_ajax:
                return JsonResponse({'success': True})
            return render(request, 'core/contacts.html', {'form': ContactForm(), 'success_message': 'Ваше сообщение отправлено!'})
        else:
            if is_ajax:
                return JsonResponse({'success': False, 'errors': form.errors.as_json()}, status=400)
            return render(request, 'core/contacts.html', {'form': form})
    return render(request, 'core/contacts.html', {'form': ContactForm()})

def portfolio_view(request):
    selected_service_slug = request.GET.get('service')
    projects = Project.objects.all().select_related('service')
    if selected_service_slug:
        projects = projects.filter(service__slug=selected_service_slug)
    services = Service.objects.all()
    context = {
        'projects': projects,
        'services': services,
        'selected_service_slug': selected_service_slug
    }
    return render(request, 'core/portfolio.html', context)

def project_detail_view(request, slug):
    project = get_object_or_404(
        Project.objects.prefetch_related('gallery_images').select_related('testimonial', 'service'), 
        slug=slug
    )
    context = {'project': project}
    return render(request, 'core/project_detail.html', context)

