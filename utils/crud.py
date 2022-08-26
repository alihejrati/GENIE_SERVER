import os
import re
import sql
import pathlib
import numbers
from django.db import transaction, connection

Code = {
    'undefined': '**CODE:undefined**'
}

def get_qs_from_inp(inp, obj_type):
    if isinstance(inp, numbers.Number):
        qs = obj_type.objects.filter(pk=inp)
    elif isinstance(inp, list) or isinstance(inp, tuple):
        qs = obj_type.objects.filter(pk__in=inp)
    else:
        qs = inp
    return qs

def _runsql(f):
    with connection.cursor() as c:
        file_data = f.readlines()
        statement = ''
        delimiter = ';\n'
        for line in file_data:
            if re.findall('DELIMITER', line): # found delimiter
                if re.findall('^\s*DELIMITER\s+(\S+)\s*$', line):
                    delimiter = re.findall('^\s*DELIMITER\s+(\S+)\s*$', line)[0] + '\n'
                    continue
                else:
                    raise SyntaxError('Your usage of DELIMITER is not correct, go and fix it!')
            statement += line # add lines while not met lines with current delimiter
            if line.endswith(delimiter):
                if delimiter != ';\n':
                    statement = statement.replace(';', '; --').replace(delimiter, ';') # found delimiter, add dash symbols (or any symbols you want) for converting MySQL statements with multiply delimiters in SQL statement
                c.execute(statement) # execute current statement
                statement = '' # begin collect next statement

#############################DBMS##############################

def callproc(proc_name, proc_list):
    try:
        res = None
        with connection.cursor() as cursor:
            cursor.callproc(str(proc_name), list(proc_list))
            res = cursor.fetchall()
        return res
    except Exception as e:
        return e

def shell(sql, obj_type=None):
    try:
        if obj_type is None:
            res = None
            with connection.cursor() as cursor:
                cursor.execute(str(sql))
                res = cursor.fetchall()
            return res
        else:
            return obj_type.objects.raw(str(sql))
    except Exception as e:
        return e

def script(sqlpath):
    try:
        sqlpath = sqlpath.replace('.sql', '').replace('.', '')
        sqlpath = os.path.join(
            str(pathlib.Path(sql.__file__).parent.resolve()),
            sqlpath
        )
        
        with open(f'{sqlpath}.sql', 'r') as f:
            try:
                sqlfile = f.read()
                sql_temp_file = sqlfile.lower()

                sql_temp_file = '\n'.join([line.split('--')[0] for line in sql_temp_file.split('\n')])
                # return sql_temp_file, 'DELIMITER'.lower() in sql_temp_file
                
                if 'DELIMITER'.lower() in sql_temp_file:
                    return _runsql(open(f'{sqlpath}.sql', 'r'))
                else:
                    return shell(sqlfile)
            except Exception as e:
                return e
    except Exception as err:
        return err

##############################CRUD#############################

def create(obj_type, spec, flag_v=False):
    try:
        new_obj = obj_type()
        new_obj_dict = {}

        for raw_key in new_obj._meta.fields:
            key = str(raw_key).split('.')[-1]
            value = spec.get(key, Code['undefined'])
            key_type = str(type(raw_key)).replace("'", '').replace('>', '').split('.')[-1]

            if key_type == 'ForeignKey':
                key = key + '_id'

            if value != Code['undefined']:
                setattr(new_obj, key, value)
                new_obj_dict[key] = (value, key_type)

        new_obj_save_output = new_obj.save()

        if flag_v:
            return new_obj, new_obj_dict, new_obj_save_output
        else:
            return new_obj
    except Exception as e:
        return e

def read():
    pass

def update(inp, obj_type, spec, flag_v):
    try:
        new_obj = obj_type()
        update_dict = {}
        new_obj_dict = {}
        qs = get_qs_from_inp(inp, obj_type)

        for raw_key in new_obj._meta.fields:
            key = str(raw_key).split('.')[-1]
            value = spec.get(key, Code['undefined'])
            key_type = str(type(raw_key)).replace("'", '').replace('>', '').split('.')[-1]

            if key_type == 'ForeignKey':
                key = key + '_id'
            
            if key_type == 'OneToOneField':
                key = key + '_id'

            if value != Code['undefined']:
                update_dict[key] = value
                new_obj_dict[key] = (value, key_type)

        new_obj_update_output = qs.update(**update_dict)

        if flag_v:
            return new_obj_dict, new_obj_update_output
        else:
            return new_obj_update_output
    except Exception as e:
        return e

def delete(inp, obj_type):
    try:
        qs = get_qs_from_inp(inp, obj_type)
        return qs.delete()
    except Exception as e:
        return e

############################Example############################

# res = crud.create(Collection, spec)
# res = crud.update(1035, Collection, spec)
# res = crud.update((1037, ..., 1035), Collection, spec)
# res = crud.update(Collection.objects.filter(id__range=(1020, 1035)), Collection, spec)
# res = crud.delete(1035), Collection)
# res = crud.delete((1037, ..., 1035), Collection)
# res = crud.delete(Collection.objects.filter(id__range=(1020, 1035)), Collection)
# res = crud.script('storefront/test.sql')
# res = crud.callproc('GetAllProducts6', [])

# res = {}
# with crud.transaction.atomic():

#     res[0] = crud.create(Order, spec={
#         'payment_status': 'C',
#         'customer': 4
#     })

#     res[1] = crud.create(OrderItem, spec={
#         'order': res[0].id,
#         'product': -12,
#         'quantity': 6,
#         'unit_price': 65.34
#     })