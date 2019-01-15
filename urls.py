from api.auth import UserAuthHandler
from api.user import UserDeatilHandler, UserListHandler
from api.admin import LoginHandler, LogoutHandler

handlers = [
    (r'/admin/auth', UserAuthHandler),
    (r'/admin/login', LoginHandler),
    (r'/admin/logout', LogoutHandler),

    (r'/user/list', UserListHandler),
    (r'/user/detail', UserDeatilHandler),
]

# Need_Token_URLs = []
