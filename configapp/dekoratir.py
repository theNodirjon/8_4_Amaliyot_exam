from functools import wraps
from django.http import JsonResponse


# Bu dekorator — avtorizatsiya tekshiradi
def registr_amalga_oshgan(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        # Agar foydalanuvchi login qilmagan bo‘lsa (AnonymUser bo‘lsa)
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Avtorizatsiya talab qilinadi!'}, status=401)

        # Aks holda funksiyani ishlatishga ruxsat beriladi
        return func(request, *args, **kwargs)

    return wrapper
