from pydantic.main import BaseModel
from enum import Enum


class CarDetailsDto:

    def __init__(self, reg_num, reg_reg, sts_num, count=3):
        self.reg_num = reg_num
        self.reg_reg = reg_reg
        self.sts_num = sts_num
        self.__count = count
        self.__active = True
        self.__msg = None
        self.__id=None


    def get_count(self):
        return self.__count

    def decrement(self):
        self.__count = self.__count - 1

    def get_active_status(self):
        return self.__active

    def set_active_status(self, new_status):
        self.__active = new_status

    def set_img_data(self, msg):
        self.__msg = msg

    def get_img_data(self):
        return self.__msg

    def set_id(self,id):
        self.__id=id

    def get_id(self):
        return self.__id

    def __repr__(self):
        return str(self.__dict__)


class Settings(BaseModel):
    useLocalDriver = False
    countOfProcess = 1
    timeout = 15


class BrowserType(Enum):
    FIREFOX = "FIREFOX"
    SELENOID = "SELENOID"

