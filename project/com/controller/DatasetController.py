import os
from datetime import date, datetime

from flask import request, render_template, redirect, url_for
from werkzeug.utils import secure_filename

from project import app
from project.com.controller.LoginController import adminLoginSession
from project.com.dao.DatasetDAO import DatasetDAO
from project.com.vo.DatasetVO import DatasetVO

DATASET_UPLOAD_FOLDER = 'project/static/adminResources/dataset/'

app.config['DATASET_UPLOAD_FOLDER'] = DATASET_UPLOAD_FOLDER


@app.route('/admin/loadDataset')
def adminLoadDataset():
    try:
        if adminLoginSession() == 'admin':

            return render_template('admin/addDataset.html')
        else:
            return redirect('/admin/logoutSession')
    except Exception as ex:
        print(ex)


@app.route('/admin/insertDataset', methods=['POST'])
def adminInsertDataset():
    try:
        if adminLoginSession() == 'admin':
            print("adminInsertDataset")

            datasetVO = DatasetVO()
            datasetDAO = DatasetDAO()

            file = request.files['datasetFilename']

            print('file::', file)

            datasetFileName = secure_filename(file.filename)
            print('filename::', datasetFileName)

            datasetFilePath = os.path.join(app.config['DATASET_UPLOAD_FOLDER'])
            print('filepath::', datasetFilePath)

            file.save(os.path.join(datasetFilePath, datasetFileName))

            datasetVO.datasetFileName = datasetFileName

            datasetVO.datasetFilePath = datasetFilePath.replace(
                "project", "..")

            datasetVO.datasetUploadDate = date.today()

            datasetVO.datasetUploadTime = (datetime.now()).strftime("%H:%M:%S")

            datasetDAO.insertDataset(datasetVO)

            return redirect(url_for('adminViewDataset'))
        else:
            return redirect('/admin/logoutSession')
    except Exception as ex:
        print(ex)


@app.route('/admin/viewDataset', methods=['GET'])
def adminViewDataset():
    try:
        if adminLoginSession() == 'admin':
            datasetDAO = DatasetDAO()
            datasetVOList = datasetDAO.viewDataset()
            print("__________________", datasetVOList)
            return render_template('admin/viewDataset.html', datasetVOList=datasetVOList)
        else:
            return redirect('/admin/logoutSession')
    except Exception as ex:
        print(ex)


@app.route('/admin/deleteDataset', methods=['GET'])
def adminDeleteDataset():
    try:
        if adminLoginSession() == 'admin':
            datasetVO = DatasetVO()
            datasetDAO = DatasetDAO()

            datasetId = request.args.get('datasetId')

            datasetVO.datasetId = datasetId

            datasetList = datasetDAO.deleteDataset(datasetVO)

            path = datasetList.datasetFilePath.replace(
                "..", "project") + datasetList.datasetFileName

            os.remove(path)

            return redirect(url_for('adminViewDataset'))
        else:
            return redirect('/admin/logoutSession')
    except Exception as ex:
        print(ex)
