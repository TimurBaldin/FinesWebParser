from datetime import datetime

from peewee import *

__user = 'root'
__password = '1234'
__db_name = 'parser_db'

dbhandle = MySQLDatabase(
    __db_name, user=__user,
    password=__password,
    host='localhost',
    port=3307
)


class BaseTable(Model):
    class Meta:
        database = dbhandle


class CarDetails(BaseTable):
    class Meta:
        db_table = 'car_details'

    id = PrimaryKeyField(null=False)
    reg_num = CharField(max_length=10)
    reg_reg = CharField(max_length=5)
    sts_num = CharField(max_length=100)
    create_date = DateTimeField(default=datetime.now())
    update_date = DateTimeField(default=datetime.now())


class FineDetails(BaseTable):
    class Meta:
        db_table = 'fine_details'

    id = PrimaryKeyField(null=False)
    car_id = IntegerField()
    fine_description = TextField()
    create_date = DateTimeField(default=datetime.now())


class ImgData(BaseTable):
    class Meta:
        db_table = 'img_data'

    id = PrimaryKeyField(null=False)
    fine_id = IntegerField()
    data = BlobField()
