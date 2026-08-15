class BaseException(Exception):
    def __init__(self, *args, status_code:int = 400):
        self.status_code = status_code
        super().__init__(*args)
        
    
    def __str__(self):
        return super().__str__()
    
