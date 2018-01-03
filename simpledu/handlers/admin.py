from flask import Blueprint, render_template
from simpledu.decorators import admin_required
from flask import request, current_app
from simpledu.models import Course


admin = Blueprint('admin', __name__, url_prefix='/admin')


# 注意此处url:/ 代表url: /admin
@admin.route('/')
@admin_required
def index():
    return render_template('admin/index.html')


@admin.route('/courses')
@admin_required
def courses():
    page = request.args.get('page', default=1, type=int)
    pagination = Course.query.paginate(
        page=page,
        per_page=current_app.config['ADMIN_PER_PAGE'],
        error_out=False
    )
    return render_template('admin/courses.html', pagination=pagination)
