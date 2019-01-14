from api.auth import UserAuthHandler

handlers = [
    (r'/v1/user/auth', UserAuthHandler),
]

# Need_Token_URLs = []
