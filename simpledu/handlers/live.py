from flask import Blueprint, render_template
from simpledu.models import Live

live = Blueprint('live', __name__, url_prefix='/live')

@live.route('/')
def index():
	live1 = Live.query.get_or_404(2)
	return render_template('live/index.html', live=live1)