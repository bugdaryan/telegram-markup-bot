from flask import url_for, redirect, request, flash
import flask_admin as admin
import flask_login as login
from flask_admin import helpers, expose
from admin import LoginForm

class MyAdminIndexView(admin.AdminIndexView):

    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated:
            return redirect(url_for('.login_view'))
        return super(MyAdminIndexView, self).index()
    
    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            if user:
                if user.is_admin:
                    login.login_user(user)
                else:
                    flash('Forbidden access', 'error')
                    return redirect(url_for('.index'))
            else:
                flash('Incorrect username or password', 'error')
        if login.current_user.is_authenticated:
            return redirect(url_for('.index'))
        self._template_args['form'] = form
        return super(MyAdminIndexView, self).index()

    @expose('/logout/')
    def logout_view(self):
        login.logout_user()
        return redirect(url_for('.index'))