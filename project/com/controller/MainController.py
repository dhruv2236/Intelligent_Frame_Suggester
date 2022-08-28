from flask import render_template

from project import app


# @app.route('/admin/viewUser')
# def adminViewUser():
#    try:
#        if adminLoginSession() == 'admin':
#            return render_template('admin/viewUser.html')
#        else:
#            return redirect('/admin/logoutSession')
#    except Exception as ex:
#        print(ex)


@app.route('/user/loadRegister')
def adminLRegister():
    return render_template('user/register.html')
