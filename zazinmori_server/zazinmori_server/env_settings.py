SECRET_KEY = 'django-insecure-yyz73f9%k25qawajk_ao3veawp9x7x299)l(zfqv2%vy8r)z#d'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'books',
        'USER' : 'root',
        'PASSWORD' : '9941',
        'HOST' : 'localhost',
        'PORT' : '3306',
    }
}

CERT_KEY = '9B5ECDD9AF5A32F5973EAC757CB6F1256C686473954F652396AEBF9E1AEDB253'

SALT = 10
ALGORITHM = 'HS256'