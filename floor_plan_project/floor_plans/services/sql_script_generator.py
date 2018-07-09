from datetime import datetime
from floor_plan_project.floor_plans.services import utils
import os
from os.path import dirname


class SQLBuilder:

    @classmethod
    def get_attrs(cls, obj, closed=True):
        res = ''
        for attr in obj:
            if closed:
                res += "\'" + attr + "\', "
            else:
                res += attr + ', '
        return res[:-2]

    @classmethod
    def generate_insert_statement(cls, table_name, parameters, values):
        return 'insert into {t}({p}) values ({v}); \n'.format(t=table_name,
                                                           p=cls.get_attrs(parameters, False),
                                                           v=cls.get_attrs(values))

    @classmethod
    def generate_insert_images_statements(cls, gen_function, values):
        statements = []
        current_time = str(datetime.now())
        for val in values:
            statements.append(gen_function('floor_plans_imagerecord',
                                           ('origin_url', 'uploaded_at'),
                                           (str(val), current_time)))

        return statements

    @classmethod
    def write(cls, file_path, statements):
        with open(file_path, 'w') as f:
            for s in statements:
                f.write(s)


csv_path = '/home/rick/Projects/lun/image_urls.csv'
file_path = os.path.join(dirname(dirname(__file__)), 'load_images.sql')
urls = utils.extract_urls_from_csv(csv_path, 11, 10000)

SQLBuilder.write(file_path, SQLBuilder.generate_insert_images_statements(SQLBuilder.generate_insert_statement, urls))
