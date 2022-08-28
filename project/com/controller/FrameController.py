import os
from datetime import date, datetime

from flask import request, render_template, redirect, url_for
from werkzeug.utils import secure_filename

from project import app
from project.com.controller.LoginController import adminLoginSession
from project.com.dao.FrameDAO import FrameDAO
from project.com.vo.FrameVO import FrameVO

FRAME_UPLOAD_FOLDER = "project/static/adminResources/frame/"
app.config['FRAME_UPLOAD_FOLDER'] = FRAME_UPLOAD_FOLDER


@app.route('/admin/loadFrame')
def adminLoadFrame():
    try:
        if adminLoginSession() == 'admin':

            return render_template('admin/addFrame.html')
        else:
            return redirect('/admin/logoutSession')
    except Exception as ex:
        print(ex)


@app.route('/admin/insertFrame', methods=['POST'])
def adminInsertFrame():
    try:
        if adminLoginSession() == 'admin':
            print("adminInsertFrame")

            frameVO = FrameVO()
            frameDAO = FrameDAO()

            faceShape = request.form['faceShape']
            file = request.files['frameFilename']

            print('file::', file)

            frameFileName = secure_filename(file.filename)
            print('filename::', frameFileName)

            frameFilePath = os.path.join(app.config['FRAME_UPLOAD_FOLDER'])
            print('filepath::', frameFilePath)

            file.save(os.path.join(frameFilePath, frameFileName))

            frameVO.faceShape = faceShape

            frameVO.frameFileName = frameFileName

            frameVO.frameFilePath = frameFilePath.replace("project", "..")

            frameVO.frameUploadDate = date.today()

            frameVO.frameUploadTime = (datetime.now()).strftime("%H:%M:%S")

            frameDAO.insertFrame(frameVO)

            return redirect(url_for('adminViewFrame'))
        else:
            return redirect('/admin/logoutSession')
    except Exception as ex:
        print(ex)


@app.route('/admin/viewFrame', methods=['GET'])
def adminViewFrame():
    try:
        if adminLoginSession() == 'admin':
            frameDAO = FrameDAO()
            frameVOList = frameDAO.viewFrame()
            print("__________________", frameVOList)
            return render_template('admin/viewFrame.html', frameVOList=frameVOList)
        else:
            return redirect('/admin/logoutSession')
    except Exception as ex:
        print(ex)


@app.route('/admin/deleteFrame', methods=['GET'])
def adminDeleteFrame():
    try:
        if adminLoginSession() == 'admin':
            frameVO = FrameVO()
            frameDAO = FrameDAO()

            frameId = request.args.get('frameId')

            frameVO.frameId = frameId

            frameList = frameDAO.deleteFrame(frameVO)

            path = frameList.frameFilePath.replace("..", "project") + frameList.frameFileName

            os.remove(path)

            return redirect(url_for('adminViewFrame'))
        else:
            return redirect('/admin/logoutSession')
    except Exception as ex:
        print(ex)
