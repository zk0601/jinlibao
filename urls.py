from api.auth import UserAuthHandler
from api.user import UserDeatilHandler, UserListHandler

handlers = [
    (r'/admin/auth', UserAuthHandler),
    (r'/user/list', UserListHandler),
    (r'/user/detail', UserDeatilHandler)
]

# Need_Token_URLs = []
