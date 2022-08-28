from project import db


class DatasetVO(db.Model):
    __tablename__ = 'datasetmaster'
    datasetId = db.Column('datasetId', db.Integer, primary_key=True, autoincrement=True)
    datasetFileName = db.Column('datasetFileName', db.String(200), nullable=False)
    datasetFilePath = db.Column('datasetFilePath', db.String(200), nullable=False)
    datasetUploadDate = db.Column('datasetUploadDate', db.String(200), nullable=False)
    datasetUploadTime = db.Column('datasetUploadTime', db.String(200), nullable=False)

    def as_dict(self):
        return {
            'datasetId': self.datasetId,
            'datasetFileName': self.datasetFileName,
            'datasetFilePath': self.datasetFilePath,
            'datasetUploadDate': self.datasetUploadDate,
            'datasetUploadTime': self.datasetUploadTime
        }


db.create_all()
