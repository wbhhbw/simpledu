from functools import wraps
from flask_login import current_user
from simpledu.models import User
from flask import abort


def role_required(role):
    """带参数的装饰器，可以用它保护一个路由处理函数只能被特定角色用户访问

        @role_required(User.ADMIN)
        def admin():
                pass
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 未登录用户或角色不满足引发404，不用403是因为不想把路由暴露给不具有权限的用户
            if not current_user.is_authenticated or current_user.role < role:
                abort(404)
            return func(*args, **kwargs)
        return wrapper
    return decorator

# 特定角色的装饰器
staff_required = role_required(User.ROLE_STAFF)
admin_required = role_required(User.ROLE_ADMIN)
