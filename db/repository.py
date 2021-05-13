from datetime import datetime

from peewee import *

from tables import FineDetails, CarDetails, ImgData
from tables import dbhandle


def save_fines(fines):
    for fine in fines:
        fine.save()


def get_car_details(sts_num):
    try:
        return CarDetails.select().where(CarDetails.sts_num == sts_num).get()
    except DoesNotExist:
        return None


def create_car_detail(carDetailsDto):
    CarDetails(reg_num=carDetailsDto.reg_num,
               reg_reg=carDetailsDto.reg_reg,
               sts_num=carDetailsDto.sts_num).save()


def get_img(car_id):
    pics = list()
    try:
        for fine in FineDetails.select().where(FineDetails.car_id == car_id).get():
            pics.append(ImgData.select(ImgData.data).where(ImgData.fine_id == fine.id).get())

        return pics
    except DoesNotExist:
        return None


def save_img(fine_id, img):
    ImgData(fine_id=fine_id, data=img).save()
