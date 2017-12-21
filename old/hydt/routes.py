from .controller.auth import (RegistrationHandler, LoginHandler,
    LogoutHandler, ChangePasswordHandler)
from .controller.home import HomeHandler
from .controller.user import (UserHandler, UserPasswordHandler,
    UserDayHandler,)
from .utils import UUID_RE


ROUTES = (
    (r'/', HomeHandler),

    (r'/register/?', RegistrationHandler),
    (r'/login/?', LoginHandler),
    (r'/logout/?', LogoutHandler),

    (r'/user/', UserHandler),
    (r'/user/password/?', UserPasswordHandler),
    (r'/user/('+ UUID_RE +')/?', UserDayHandler),
)
