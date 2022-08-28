from project import db
from project.com.vo.LoginVO import LoginVO
from project.com.vo.ImageVO import ImageVO


class ImageDAO():
    def insertImage(self, imageVO):
        db.session.merge(imageVO)
        db.session.commit()

    def viewImageShapeByLoginId(self, imageVO):
        imageVOList = ImageVO.query.filter_by(
        image_LoginId=imageVO.image_LoginId).all()
        return imageVOList
