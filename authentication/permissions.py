from django.shortcuts import redirect
#  custom decorator

def Permission_roles(roles):

    def decorator(fn):
        
        def wrapper(request,*args,**kwargs):
            
            if request.user and request.user.is_authenticated and request.user.role in roles:
                return fn(request,*args,**kwargs)
            
            return redirect('login')
    
        return wrapper
    
    return decorator
