from project import db
from project.com.vo.FrameVO import FrameVO


class FrameDAO:
    def insertFrame(self, frameVO):
        db.session.add(frameVO)
        db.session.commit()

    def viewFrame(self):
        frameList = FrameVO.query.all()

        return frameList

    def deleteFrame(self, frameVO):
        frameList = FrameVO.query.get(frameVO.frameId)

        db.session.delete(frameList)

        db.session.commit()

        return frameList

    def viewFrameByFaceShape(self,frameVO):
        frameVOList = FrameVO.query.filter_by(faceShape=frameVO.faceShape).all()
        return frameVOList