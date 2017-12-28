from flask import Blueprint


admin = Blueprint('admin', __name__, url_prefix='/admin')

# 注意此处url:/ 代表url: /admin
@admin.route('/')
def admin_index():
    return 'admin'