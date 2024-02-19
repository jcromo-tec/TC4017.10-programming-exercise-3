'''
Modulo para leer archivos con los datos de Hotel, Customer y Reservation.
Todos los datos están en formato JSON.

Historia
Fecha           Descripcion del cambio                      Author
17-02-2024      Version inicial                             A00260430
'''
import json
import os

from filelock import FileLock
OK_STATUS = 0
ERROR_STATUS = -9
TEMP_DATA = {}


def create_data_store(entity_name) -> tuple[int, None]:
    '''
    Función para crear un archivo de datos en formato JSON.

    La función genera un diccionario simple con todos los productos y sus
    precios.
    '''
    status = OK_STATUS

    try:
        lock = FileLock(entity_name+'.lock')
        with lock:
            with open(entity_name+'.json', 'w', encoding='UTF-8') as fd:
                json.dump(TEMP_DATA, fd)
    except OSError as error:
        print(
            '[ERROR] - An exception ocurred',
            f'while creating file for entity {entity_name}: {error}'
        )
        status = ERROR_STATUS
    finally:
        lock.release()

    return status, None


def update_data_store(entity_name, data) -> tuple[int, None]:
    '''
    Función para actualizar archivo con en formato JSON.
    '''
    status = OK_STATUS

    try:
        lock = FileLock(entity_name+'.lock')
        with lock:
            with open(entity_name+'.json', 'w', encoding='UTF-8') as fd:
                json.dump(data, fd)
    except OSError as error:
        print(
            '[ERROR] - An exception ocurred',
            f'while writing file for entity {entity_name}: {error}'
        )
        status = ERROR_STATUS
    finally:
        lock.release()

    return status, None


def load_data_store(entity_name) -> tuple[int, dict]:
    '''
    Función para actualizar archivo con en formato JSON.
    '''
    status = OK_STATUS
    data = None

    try:
        lock = FileLock(entity_name+'.lock')
        with lock:
            if not os.path.isfile(entity_name+'.json'):
                data = {}
            else:
                with open(entity_name+'.json', 'r', encoding='UTF-8') as fd:
                    data = json.load(fd)
    except OSError as error:
        print(
            '[ERROR] - An exception ocurred',
            f'while reading file for entity {entity_name}: {error}'
        )
        status = ERROR_STATUS
        data = {}
    finally:
        lock.release()

    return status, data
