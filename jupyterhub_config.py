# Конфигурация JupyterHub для запуска в Docker
import os

# Слушать на всех интерфейсах (для доступа с хоста)
c.JupyterHub.bind_url = "http://0.0.0.0:8000"

# Аутентификация: DummyAuthenticator (для тестирования)
c.JupyterHub.authenticator_class = "dummy"
c.DummyAuthenticator.password = os.environ.get("DUMMY_AUTH_PASSWORD", "admin")

# Админ и разрешённые пользователи
c.Authenticator.admin_users = {"admin"}
c.Authenticator.allowed_users = {"admin"}

# Токен для configurable-http-proxy (из .env)
c.ConfigurableHTTPProxy.auth_token = os.environ.get("CONFIGPROXY_AUTH_TOKEN", "")

# Файл секрета для cookie-сессий (JupyterHub создаст при первом запуске)
c.JupyterHub.cookie_secret_file = "/srv/jupyterhub/jupyterhub_cookie_secret"
# JUPYTERHUB_CRYPT_KEY задаётся в .env для шифрования auth_state

# Spawner: запуск JupyterLab по умолчанию
c.Spawner.default_url = "/lab"
c.Spawner.cmd = ["jupyter-labhub"]
