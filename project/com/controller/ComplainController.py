import os
from datetime import datetime

from flask import render_template, request, session, redirect, url_for
from werkzeug.utils import secure_filename

from project import app
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from project.com.dao.ComplainDAO import ComplainDAO
from project.com.vo.ComplainVO import ComplainVO


@app.route('/admin/viewComplain')
def adminViewComplain():
    try:
        if adminLoginSession() == "admin":
            complainVO = ComplainVO()
            complainDAO = ComplainDAO()
            complainVO.complainStatus = "pending"
            complainVOList = complainDAO.adminViewComplain(complainVO)

            return render_template('admin/viewComplain.html', complainVOList=complainVOList)
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/admin/loadComplainReply', methods=['GET'])
def adminLoadComplainReply():
    try:
        if adminLoginSession() == "admin":
            complainId = request.args.get('complainId')
            return render_template('admin/addComplainReply.html', complainId=complainId)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/insertComplainReply', methods=['POST'])
def adminInsertComplainReply():
    try:
        if adminLoginSession() == "admin":
            complainDAO = ComplainDAO()
            complainVO = ComplainVO()

            complainId = request.form['complainId']
            replySubject = request.form['replySubject']
            replyMessage = request.form['replyMessage']

            replyDate = str(datetime.date(datetime.now()))
            replyTime = str(datetime.time(datetime.now()))
            complainStatus = 'Replied'
            complainTo_LoginId = session['session_loginId']
            file = request.files['file']
            replyFileName = secure_filename(file.filename)

            UPLOAD_FOLDER = 'project/static/adminResources/replyAttachment/'
            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

            replyFilePath = os.path.join(app.config['UPLOAD_FOLDER'])

            file.save(os.path.join(replyFilePath, replyFileName))

            complainVO.complainId = complainId
            complainVO.replySubject = replySubject
            complainVO.replyMessage = replyMessage
            complainVO.replyFileName = replyFileName
            complainVO.replyFilePath = replyFilePath.replace('project', '..')
            complainVO.replyDate = replyDate
            complainVO.replyTime = replyTime
            complainVO.complainTo_LoginId = complainTo_LoginId
            complainVO.complainStatus = complainStatus

            complainDAO.adminInsertComplainReply(complainVO)

            return redirect(url_for('adminViewComplain'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/loadComplain')
def userLoadComplain():
    try:
        if adminLoginSession() == "user":
            return render_template('user/addComplain.html')
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/insertComplain', methods=['POST'])
def userInsertComplain():
    try:
        if adminLoginSession() == "user":
            complainVO = ComplainVO()
            complainDAO = ComplainDAO()

            complainSubject = request.form['complainSubject']
            complainDescription = request.form['complainDescription']

            UPLOAD_FOLDER = 'project/static/adminResources/complainAttach/'

            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

            file = request.files['file']
            print(file)

            complainFileName = secure_filename(file.filename)
            print(complainFileName)

            complainFilePath = os.path.join(app.config['UPLOAD_FOLDER'])
            print(complainFilePath)

            file.save(os.path.join(complainFilePath, complainFileName))

            complainDate = str(datetime.date(datetime.now()))
            complainTime = str(datetime.time(datetime.now()))
            complainFrom_LoginId = session['session_loginId']

            complainVO.complainSubject = complainSubject
            complainVO.complainDescription = complainDescription
            complainVO.complainFileName = complainFileName
            complainVO.complainFilePath = complainFilePath.replace(
                "project", "..")

            complainVO.complainDate = complainDate
            complainVO.complainTime = complainTime
            complainVO.complainFrom_LoginId = complainFrom_LoginId
            complainVO.complainStatus = "pending"

            complainDAO.userInsertComplain(complainVO)

            return redirect(url_for('userViewComplain'))

        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/viewComplain', methods=['GET'])
def userViewComplain():
    try:
        if adminLoginSession() == "user":
            complainVO = ComplainVO()
            complainDAO = ComplainDAO()

            complainVO.complainFrom_LoginId = session['session_loginId']

            complainVOList = complainDAO.userViewComplain(complainVO)

            return render_template('user/viewComplain.html', complainVOList=complainVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/deleteComplain', methods=['GET'])
def userDeleteComplain():
    try:
        if adminLoginSession() == "user":
            complainVO = ComplainVO()
            complainDAO = ComplainDAO()

            complainId = request.args.get('complainId')

            complainVO.complainId = complainId

            complainList = complainDAO.userDeleteComplain(complainVO)

            complainFileName = complainList.complainFileName
            complainFilePath = complainList.complainFilePath

            fullPath = complainFilePath.replace(
                '..', 'project') + complainFileName

            os.remove(fullPath)

            if complainList.complainStatus == 'Replied':
                replyFileName = complainList.replyFileName
                replyFilePath = complainList.replyFilePath

                fullPath = replyFilePath.replace(
                    '..', 'project') + replyFileName

                os.remove(fullPath)

            return redirect(url_for('userViewComplain'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/viewComplainReply')
def userViewComplainReply():
    try:
        if adminLoginSession() == "user":
            complainDAO = ComplainDAO()
            complainVO = ComplainVO()

            complainId = request.args.get('complainId')

            complainVO.complainId = complainId

            complainVOList = complainDAO.userViewComplainReply(complainVO)

            return render_template('user/viewComplainReply.html', complainVOList=complainVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)
