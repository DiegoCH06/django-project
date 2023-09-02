class Auth:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        token = self.session.get('token')
        refresh = self.session.get('refresh')
        if not token or not refresh:
            self.clean()
            self.save_auth()
        else:
            self.token = token
            self.refresh = refresh

    def add_tokens(self, token, refresh):
        self.token = token
        self.refresh = refresh
        self.save_auth()

    def clean(self):
        self.token = None
        self.refresh = None

    def save_auth(self):
        self.session['token'] = self.token
        self.session['refresh'] = self.refresh
        self.session.modified = True