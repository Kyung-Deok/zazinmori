SECRET_KEY = 'django-insecure-yyz73f9%k25qawajk_ao3veawp9x7x299)l(zfqv2%vy8r)z#d'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'pjt3',
        'USER' : 'admin',
        'PASSWORD' : 'qwer1234',
        'HOST' : '35.79.77.17',
        'PORT' : '3306',
    }
}

CERT_KEY = '9B5ECDD9AF5A32F5973EAC757CB6F1256C686473954F652396AEBF9E1AEDB253'

SALT = 10
ALGORITHM = 'HS256'