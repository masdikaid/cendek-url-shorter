# import sys
# sys.path.append("d:\\project\\cendek-url-shorter\\backend\\webapi")
from datetime import datetime
from firebase import createShorterUrl,getAllUrlData, getUrlData, getUrlDataByUser, getVisitor, setVisitorData, setExpirationData

class UrlStore():
    def __init__(self, userid, target_url, urlid=None, isactive=True, expiration=None, create_at=None):
        self.urlid = urlid
        self.userid = userid
        self.target_url = target_url
        self.isactive = isactive
        self.expiration = expiration
        self.create_at = create_at
    
    def create(self):
        self.create_at = datetime.now()
        url_data = createShorterUrl(self.urlid, self.userid, self.toDict)
        self.urlid = url_data["urlid"]

    @staticmethod
    def get(urlid):
        urldata = getUrlData(urlid)
        return UrlStore(urldata["userid"], urldata["target_url"], urlid, urldata["isactive"], urldata["expiration"], urldata["create_at"])

    @staticmethod
    def getByUser(userid):
        urlsdata = getUrlDataByUser(userid)
        return [ UrlStore(u["userid"], u["target_url"], u["urlid"], u["isactive"], u["expiration"], u["create_at"]) for u in urlsdata ]

    @staticmethod
    def all(userid):
        urlsdata = getAllUrlData(userid)
        return [ UrlStore(u["userid"], u["target_url"], u["urlid"], u["isactive"], u["expiration"], u["create_at"]) for u in urlsdata ]    

    @property
    def visitor(self):
        return getVisitor(self.urlid)

    @visitor.setter
    def visitor(self, visitordata):
        visitor = {
            "timestamp" : datetime.now(),
            "ipaddress" : visitordata["ipaddress"],
            "device" : visitordata["device"]
        }
        setVisitorData(self.urlid, visitor)

    @expiration.setter
    def expiration(self, expirationdata):
        expiration = {
            "expiration_at" : expirationdata["expiration_at"],
            "expiration_messege" : expirationdata["messege"] 
        }
        setExpirationData(self.urlid, expiration)
        self.expiration = expiration

    @property
    def toDict(self):
        return {
            "target_url" : self.target_url,
            "isactive" : self.isactive,
            "expiration" : self.expiration,
            "create_at" : self.create_at
        }