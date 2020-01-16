EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
# Turn on less secure apps to make it work
# https://support.google.com/accounts/answer/6010255?hl=en
EMAIL_HOST_USER = '<mail>@gmail.com'
EMAIL_HOST_PASSWORD = '<password>'
