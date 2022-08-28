from project import db
from project.com.vo.LoginVO import LoginVO

class ImageVO(db.Model):
    __tablename__ = 'imagemaster'
    imageId = db.Column('imageId', db.Integer, primary_key=True, autoincrement=True)
    imageFileName = db.Column('imageFileName', db.String(100), nullable=False)
    imageFilePath = db.Column('imageFilePath', db.String(100), nullable=False)
    faceShape = db.Column('faceShape', db.String(100), nullable=False)
    imageUploadDate = db.Column('imageUploadDate', db.String(100), nullable=False)
    imageUploadTime = db.Column('imageUploadTime', db.String(100), nullable=False)
    image_LoginId = db.Column('image_LoginId', db.Integer, db.ForeignKey(LoginVO.loginId))

    def as_dict(self):
        return {
            'imageId': self.imageId,
            'imageFileName': self.imageFileName,
            'imageFilePath': self.imageFilePath,
            'faceShape':self.faceShape,
            'imageUploadDate':self.imageUploadDate,
            'imageUploadTime':self.imageUploadTime,
            'image_LoginId': self.image_LoginId
        }


db.create_all()
