from datetime import datetime
from firebase import createShorterUrl,getAllUrlData, getUrlData, getUrlDataByUser, getVisitor, setVisitorData, updateUrlData, deleteUrlData, checkUrlExists

class UrlStore():
    def __init__(self, target_url=[], urlid=None, userid=None, delete_at=True, expiration=None, create_at=None, hit=None):
        self.urlid = urlid
        self.userid = userid
        self.target_url = self.convertTargetUrl(target_url)
        self.delete_at = delete_at
        self.expiration = self.convertExpiration(expiration)
        self.create_at = create_at 
        self.hit = hit
    
    def convertTargetUrl(self, target_url):
        if not len(target_url) == 0 :
            return [{"title":url["title"] if "title" in url else None, "url":url["url"], "desc":url["desc"] if "desc" in url else None, "thumb":url["thumb"] if "thumb" in url else None} for url in target_url ]
        else :
            raise ValueError("target url must have minimum one url")

    def setTargetUrl(self, target_url):
        self.target_url = self.convertTargetUrl(target_url)

    def create(self):
        self.create_at = datetime.now()
        url_data = createShorterUrl(self.urlid, self.userid, self.toDict)
        self.urlid = url_data["urlid"]

    def update(self):
        updateUrlData(self.urlid, self.toDict)

    def delete(self):
        deleteUrlData(self.urlid)
        return None

    @staticmethod
    def get(urlid):
        urldata = getUrlData(urlid)
        return UrlStore(urldata["target_url"], urlid, urldata["userid"], urldata["delete_at"], urldata["expiration"], urldata["create_at"], len(urldata["visitor"]) if "visitor" in urldata else None)

    @staticmethod
    def getByUser(userid):
        urlsdata = getUrlDataByUser(userid)
        return [ UrlStore(u["target_url"], u["urlid"], u["userid"], u["delete_at"], u["expiration"], u["create_at"], len(u["visitor"]) if "visitor" in u else None) for u in urlsdata ]

    @staticmethod
    def all(userid):
        urlsdata = getAllUrlData(userid)
        return [ UrlStore(u["target_url"], u["urlid"], u["userid"], u["delete_at"], u["expiration"], u["create_at"], len(u["visitor"]) if "visitor" in u else None) for u in urlsdata ]    

    @property
    def visitor(self):
        return getVisitor(self.urlid)

    def convertExpiration(self, expirationdata):
        if type(expirationdata) == dict :
            return {
                "expiration_at" : expirationdata["expiration_at"],
                "expiration_messege" : expirationdata["expiration_messege"] 
            }
        else :
            return None

    def setExpiration(self, expirationdata):
        self.convertExpiration(expirationdata)

    @property
    def toDict(self):
        return {
            "target_url" : self.target_url,
            "delete_at" : self.delete_at,
            "expiration" : self.expiration,
            "create_at" : self.create_at
        }

    @staticmethod
    def check(urlid):
        return checkUrlExists(urlid)