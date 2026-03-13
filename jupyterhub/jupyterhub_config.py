c.JupyterHub.ip = '0.0.0.0'
c.JupyterHub.port = 8000
c.JupyterHub.hub_ip = '0.0.0.0'
c.JupyterHub.spawner_class = 'simple'
c.Authenticator.allowed_users = {'admin'}
c.Authenticator.admin_users = {'admin'}
c.PAMAuthenticator.open_sessions = False
c.JupyterHub.log_level = 'INFO'
