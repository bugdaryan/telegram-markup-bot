from flask_admin import BaseView, expose
from models import Image, Label

class LabelStatisticsView(BaseView):
    def render_template(self, template, **kwargs):
        return super().render_template('admin/index.html', **kwargs)
    
    @expose('/')
    def index(self):
        total_count = Image.query.filter().count()
        labeled_count = Image.query.filter(Image.label != None).count()

        label_counts = {}
        for label in Label.query.all():
            label_counts[label.name] = Image.query.filter(Image.label == label).count()

        return self.render('label_statistics.html', labeled_count=labeled_count, total_count=total_count, label_counts=label_counts)