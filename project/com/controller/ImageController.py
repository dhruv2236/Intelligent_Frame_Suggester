import os
from datetime import datetime
from PIL import Image
from flask import request, render_template, redirect, url_for,session
from werkzeug.utils import secure_filename

from project import app
from project.com.controller.LoginController import adminLoginSession
from project.static.adminResources.FrameFinder import Face_Landmark
from project.com.vo.ImageVO import ImageVO
from project.com.dao.ImageDAO import ImageDAO

from project.com.vo.FrameVO import FrameVO
from project.com.dao.FrameDAO import FrameDAO

IMAGE_UPLOAD_FOLDER = "project/static/adminResources/uploadimage/"
app.config['IMAGE_UPLOAD_FOLDER'] = IMAGE_UPLOAD_FOLDER


@app.route('/user/loadImage')
def userLoadImage():
    try:
        if adminLoginSession() == 'user':

            return render_template('user/addImage.html')
        else:
            return redirect('/admin/logoutSession')
    except Exception as ex:
        print(ex)

@app.route('/user/insertImage',methods=['POST'])
def userInsertImage():
    try:
        if adminLoginSession() == 'user':
            imageVO = ImageVO()
            imageDAO = ImageDAO()

            file = request.files['file']

            imageFileName = secure_filename(file.filename)
            print('filename::', imageFileName)

            imageFilePath = os.path.join(app.config['IMAGE_UPLOAD_FOLDER'])
            print('filepath::', imageFilePath)

            file.save(os.path.join(imageFilePath, imageFileName))

            file_upload = Image.open(os.path.join(imageFilePath, imageFileName))
    
            out_list = Face_Landmark.drawFaceSketch(file_upload)

            print('out_list>>>>>>',out_list)

            uploadDate = str(datetime.now().date())
            uploadTime = datetime.now().strftime('%H:%M:%S')
            imageVO.imageFileName = imageFileName
            imageVO.imageFilePath = imageFilePath.replace('project','..')
            imageVO.faceShape = out_list['Shape']
            imageVO.imageUploadDate = uploadDate
            imageVO.imageUploadTime = uploadTime
            imageVO.image_LoginId = session['session_loginId']

            imageDAO.insertImage(imageVO)

            return redirect(url_for('userViewImage'))
        else:
            return redirect('/admin/logoutSession')
    except Exception as ex:
        print(ex)
        
@app.route('/user/viewImage')
def userViewImage():
    try:
        if adminLoginSession() == 'user':
            imageVO = ImageVO()
            imageDAO = ImageDAO()

            frameVO = FrameVO()
            frameDAO = FrameDAO()

            loginId = session['session_loginId']
            imageVO.image_LoginId = loginId
            imageVOList = imageDAO.viewImageShapeByLoginId(imageVO)
            faceShape = imageVOList[0].faceShape
            print('faceShape>>>>>',faceShape)

            frameVO.faceShape = faceShape
            frameVOList = frameDAO.viewFrameByFaceShape(frameVO)
            print('frameVOList>>>>>>>>>>>',frameVOList)

            return render_template('user/viewImage.html',frameVOList=frameVOList)
        else:
            return redirect('/admin/logoutSession')
    except Exception as ex:
        print(ex)

