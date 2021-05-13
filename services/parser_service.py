from datetime import datetime

from classes import BrowserType, CarDetailsDto
from parser_executor import parser
from db.repository import create_car_detail, get_car_details, get_img


def check_update_date(car_detail):
    return datetime.now().day - car_detail.update_date.day < 1


def get_pics(car_detail):
    get_img(car_detail.id)


def service(cars_list: list) -> list:
    for car in cars_list:
        car_detail = get_car_details(car.sts_num)
        if car_detail is None:
            print("car_detail is not found")
            create_car_detail(car)
        elif check_update_date(car_detail):
            if get_pics(car_detail) is not None:
                car.set_img_data(get_pics(car_detail))

        if car.get_id() is None:
            car.set_id(get_car_details(car.sts_num).id)

    return parser(BrowserType.SELENOID, cars_list)


if __name__ == '__main__':
    fines = list([
        CarDetailsDto('у849ск', '777', '7741423901'),
        CarDetailsDto('а843нм', '799', '9909333875'),
        CarDetailsDto('у714хе', '777', '7750877017'),
        CarDetailsDto('К483НО', '77', '7703964071')
    ]
    )
    lists = service(fines)

    for l in lists:
        print(l)
