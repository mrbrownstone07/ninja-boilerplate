from django.http import JsonResponse

def lockout(request, credentials, *args, **kwargs):
    """This is called for django-axes response when a user account is locked!"""
    return JsonResponse({"message": "Locked out due to too many login failures! Contact with administrator."}, status=403)