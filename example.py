from app.config import settings
from urllib.parse import quote

print(settings.database_username)
print(quote(settings.database_password))
print(settings.database_hostname)
print(settings.database_port)
print(settings.database_name)
