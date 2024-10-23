class LogIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        print(f"IP Address: {request.META['REMOTE_ADDR']}")
        
        response = self.get_response(request)
        return response
    
class ModifyRequestResponseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        request.META['HTTP_CUSTOM_HEADER'] = "Hello Furqan Welcome"
        print(f"Request Header: 'HTTP_CUSTOM_HEADER' added: {request.META['HTTP_CUSTOM_HEADER']}")
        
        response = self.get_response(request)
        response['X-Custom-Response-Header'] = "Processed by ModifyRequestResponseMiddleware"
        
        print(f"Response Header 'X-Custom-Response-Header' added")
        
        return response