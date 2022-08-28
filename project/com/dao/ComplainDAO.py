from  project import db
from project.com.vo.ComplainVO import ComplainVO
from project.com.vo.LoginVO import LoginVO


class ComplainDAO():
    def adminInsertComplainReply(self, complainVO):
        db.session.merge(complainVO)
        db.session.commit()

    def adminViewComplain(self, complainVO):
        complainList = db.session.query(ComplainVO, LoginVO) \
            .filter_by(complainStatus=complainVO.complainStatus) \
            .join(LoginVO, ComplainVO.complainFrom_LoginId == LoginVO.loginId).all()
        return complainList

    def userDeleteComplain(self, complainVO):
        complainList = ComplainVO.query.get(complainVO.complainId)
        db.session.delete(complainList)
        db.session.commit()

        return complainList

    def userInsertComplain(self, complainVO):
        db.session.add(complainVO)
        db.session.commit()
        db.session.close()

    def userViewComplain(self, complainVO):
        complainList = ComplainVO.query.filter_by(complainFrom_LoginId=complainVO.complainFrom_LoginId).all()
        return complainList

    def userViewComplainReply(self, complainVO):
        complainList = ComplainVO.query.filter_by(complainId=complainVO.complainId).all()
        return complainList

    def totalComplain(self):
        complainList = ComplainVO.query.all()
        return complainList
