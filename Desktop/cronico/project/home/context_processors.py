from .models import category

def custom_context(request):
    categories = category.objects.all()
    return {'custom_data': categories}
