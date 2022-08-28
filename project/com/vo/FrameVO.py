from project import db


class FrameVO(db.Model):
    __tablename__ = 'framemaster'
    frameId = db.Column('frameId', db.Integer, primary_key=True, autoincrement=True)
    frameFileName = db.Column('frameFileName', db.String(200), nullable=False)
    frameFilePath = db.Column('frameFilePath', db.String(200), nullable=False)
    frameUploadDate = db.Column('frameUploadDate', db.String(200), nullable=False)
    frameUploadTime = db.Column('frameUploadTime', db.String(200), nullable=False)
    faceShape = db.Column('faceShape', db.String(200), nullable=False)

    def as_dict(self):
        return {
            'frameId': self.frameId,
            'frameFileName': self.frameFileName,
            'frameFilePath': self.frameFilePath,
            'frameUploadDate': self.frameUploadDate,
            'frameUploadTime': self.frameUploadTime,
            'faceShape': self.faceShape
        }


db.create_all()
