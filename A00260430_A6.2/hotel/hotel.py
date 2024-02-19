'''
Codigo fuente de la clase Customer. Esta clase usa la clase Persistence.

La clase Customer implementa los metodos create_customer, delete_customer,
display_customer_info, modify_customer_info

Historia
Fecha           Descripcion del cambio                      Author
17-02-2024      Version inicial                             A00260430
'''
import datetime
from persistence import update_data_store, load_data_store


OK_STATUS = 0
ERROR_STATUS = -209
DUPLICATE_HOTEL = -201
HOTEL_NOT_FOUND = -202
INVALID_FIELD = -210
ROOM_NOT_FOUND = -220
ROOM_NOT_AVAILABLE = -230
RESERVATION_NOT_FOUND = -240
HOTEL_ENTITY = 'hotel'


class Hotel():
    '''
    Clase Hotel. Esta clase crea un diccionario con datos contenidos en un archivo
    con formato JSON nombrado hotel.json.

    La estructura del cliente es un diccionario con los campos
    - name (nombre)
    - cuartos (anio con arreglo por cuarto de 366 elementos binarios (falso o verdadero))


    Metodos privados
    + _validate_hotel_data - verifica que los datos sean del tipo correcto

    Metodos publicos
    + create_hotel - crea un nuevo registro del hotel.
    + delete_hotel - borra un registro existente del hotel
    + display_hotel_info - obtiene los datos de un registro existente del hotel
    + modify_hotel_info - actualiza los datos de un registro existente del hotel
    + reserve_hotel_room - reserva una habitacion en un hotel existente
    + cancel_hotel_reservation - cancela la reservacio de una habitacion en un hotel
    '''

    def __init__(self):
        # Cargando datos del archivo en formato JSON para el diccionario de hoteles
        self.loaded_data, self.hotel_dicc = load_data_store(HOTEL_ENTITY)

    def _validate_hotel_data(
            self,
            partial: bool,
            name: str,
            address: str,
            rooms: int) -> tuple[int, dict]:
        '''
        Este metodo valida los campos del hotel.

        El metodo retorna una tupla (err, field_list)
        '''
        status = 0
        field_list = {}
        if name is None or not isinstance(name, str) or name == '':
            status = INVALID_FIELD
        field_list['name'] = (
            bool(isinstance(name, str)),
            name
        )
        if address is None or not isinstance(address, str) or address == '':
            status = INVALID_FIELD
        field_list['address'] = (
            bool(isinstance(address, str)),
            address
        )
        if (rooms is None or not isinstance(rooms, int) or rooms <= 0) and not partial:
            status = INVALID_FIELD
        field_list['rooms'] = (
            bool(isinstance(rooms, int)),
            rooms
        )

        return status, field_list

    def create_hotel(
            self,
            name: str,
            address: str,
            rooms: int) -> tuple[int, None]:
        '''
        Metodo para crear un registro nuevo de hotel. La llave primaria es el nombre
        del hotel.

        El metodo retorna una tupla (err, None)
        '''
        status = OK_STATUS
        status_persist = OK_STATUS

        status, _ = self._validate_hotel_data(
            False,
            name,
            address,
            rooms
        )

        if status == OK_STATUS:
            if name in self.hotel_dicc:
                status = DUPLICATE_HOTEL
            else:
                hotel_data = {}
                present_year = str(datetime.date.today().year)
                room_list = [[(False, '')] * 366] * rooms
                hotel_data['address'] = address
                hotel_data['rooms'] = rooms
                hotel_data[present_year] = room_list
                self.hotel_dicc[name] = hotel_data
                status_persist, _ = update_data_store(HOTEL_ENTITY, self.hotel_dicc)

        return int(status + status_persist), None

    def delete_hotel(self, name: str) -> tuple[int, None]:
        '''
        Este metodo remueve un hotel en el diccionario de clientes.

        El diccionario de hotel es almacenado en el archivo customer.json

        Regresa una tupla (err, None)
        '''
        status = OK_STATUS
        status_persist = OK_STATUS

        if name in self.hotel_dicc:
            self.hotel_dicc.pop(name)
            status_persist, _ = update_data_store(HOTEL_ENTITY, self.hotel_dicc)
        else:
            status = HOTEL_NOT_FOUND

        return int(status + status_persist), None

    def display_hotel_info(self, name: str) -> tuple[int, dict]:
        '''
        Este metodo depliega los datos de un hotel en el diccionario de
        clientes.

        El diccionario de hotel es almacenado en el archivo customer.json

        Regresa una tupla (err, diccionario)
        '''
        status = OK_STATUS
        hotel_data = {}

        if name in self.hotel_dicc:
            hotel_data['name'] = name
            hotel_data['address'] = self.hotel_dicc[name]['address']
            hotel_data['rooms'] = self.hotel_dicc[name]['rooms']
        else:
            status = HOTEL_NOT_FOUND

        return status, hotel_data

    def modify_hotel_info(self, name: str, address: str) -> tuple[int, dict]:
        '''
        Este metodo depliega los datos de un hotel en el diccionario de
        clientes.

        El diccionario de hotel es almacenado en el archivo customer.json

        Regresa una tupla (err, diccionario)
        '''
        status = OK_STATUS
        status_persist = OK_STATUS
        hotel_field_list = {}
        hotel_data = {}

        status, hotel_field_list = self._validate_hotel_data(
            True,
            name,
            address,
            None
        )

        if status == OK_STATUS:
            if name in self.hotel_dicc:
                hotel_data['name'] = name
                hotel_data['rooms'] = self.hotel_dicc[name]['rooms']
                if hotel_field_list['address'][0]:
                    self.hotel_dicc[name]['address'] = address
                    hotel_data['address'] = address
                    status_persist, _ = update_data_store(
                        HOTEL_ENTITY, self.hotel_dicc
                    )
            else:
                status = HOTEL_NOT_FOUND

        return int(status + status_persist), hotel_data

    def _validate_reservation_data(
            self,
            room: int,
            year: int,
            month: int,
            day: int,
            days: int) -> tuple[int, int]:
        '''
        Metodo privado para validar los datos de la reservacion
        '''
        status = OK_STATUS
        if (room is None or not isinstance(room, int) or room < 1):
            status = INVALID_FIELD
        if (month is None or not isinstance(month, int) or month < 1 or month > 12):
            status = INVALID_FIELD
        if (day is None or not isinstance(day, int) or day < 1 or day > 31):
            status = INVALID_FIELD
        if (days is None or not isinstance(days, int) or day < 1 or days > 366):
            status = INVALID_FIELD

        date_value = datetime.datetime(year, month, day, 0, 0)
        julian_date = date_value.timetuple()

        return status, julian_date.tm_yday

    def _reserve_hotel_rooms(
            self,
            name: str,
            customer_no: str,
            room: int,
            year: int,
            date_day: int,
            days: int) -> tuple[int, None]:
        '''
        Metodo privado para reservar una habitacion. Una habitacion esta
        representada por una tupla donde el primer valor [0] indica si la
        habitacion esta ocupada para ese dia (verdadero) o no (falso). Si
        esta ocupada el segundo valor de la tupla [1] tiene el valor del
        numero de cliente.

        El metodo intentara reservar una habitacion en el dia solicitado
        del anio actual. Si puede agregara el numero de cliente en ese
        dia para esa habitacion.

        Si no puede reserver todos los dias removera las reservaciones en los
        dias que si pudo y retornara un error de habitacion no encontrada.
        '''
        status = OK_STATUS
        present_year = str(year)

        if room > self.hotel_dicc[name]['rooms']:
            status = ROOM_NOT_FOUND
            return status, None
        if present_year not in self.hotel_dicc[name]:
            status = ROOM_NOT_FOUND
            return status, None

        date_val = date_day - 1
        while (
                date_val < (date_day - 1 + days)
                and status == OK_STATUS):
            if self.hotel_dicc[name][present_year][room - 1][date_val][0]:
                status = ROOM_NOT_AVAILABLE
                break
            self.hotel_dicc[name][present_year][room - 1][date_val] = (True, customer_no)
            date_val += 1

        if status == ROOM_NOT_AVAILABLE:
            date_val -= 1
            while date_val >= (date_day - 1):
                self.hotel_dicc[name][present_year][room - 1][date_val] = (False, '')
                date_val -= 1

        return status, None

    def _unreserve_hotel_rooms(
            self,
            name: str,
            customer_no: str,
            room: int,
            year: int,
            date_day: int,
            days: int) -> tuple[int, None]:
        '''
        Metodo privado para reservar una habitacion. Una habitacion esta
        representada por una tupla donde el primer valor [0] indica si la
        habitacion esta ocupada para ese dia (verdadero) o no (falso). Si
        esta ocupada el segundo valor de la tupla [1] tiene el valor del
        numero de cliente.

        El metodo intentara reservar una habitacion en el dia solicitado
        del anio actual. Si puede agregara el numero de cliente en ese
        dia para esa habitacion.

        Si no puede reserver todos los dias removera las reservaciones en los
        dias que si pudo y retornara un error de habitacion no encontrada.
        '''
        status = OK_STATUS
        present_year = str(year)

        if room > self.hotel_dicc[name]['rooms']:
            status = ROOM_NOT_FOUND
            return status, None
        if present_year not in self.hotel_dicc[name]:
            status = ROOM_NOT_FOUND
            return status, None

        date_val = date_day - 1
        while (
                date_val < (date_day - 1 + days)
                and status == OK_STATUS):
            if not self.hotel_dicc[name][present_year][room - 1][date_val][0]:
                status = ROOM_NOT_FOUND
                break
            if self.hotel_dicc[name][present_year][room - 1][date_val][1] != customer_no:
                status = ROOM_NOT_FOUND
                break
            self.hotel_dicc[name][present_year][room - 1][date_val] = (False, '')
            date_val += 1

        if status == ROOM_NOT_FOUND:
            date_val -= 1
            while date_val >= (date_day - 1):
                self.hotel_dicc[name][present_year][room - 1][date_val] = (
                    True, customer_no
                )
                date_val -= 1

        return status, None

    def reserve_hotel_room(
            self,
            name: str,
            room: int,
            customer_no: str,
            start_month: int,
            start_day: int,
            days: int) -> tuple[int, None]:
        '''
        Metodo publico para reservar una habitacion en un hotel en el presente
        anio.
        '''
        status = OK_STATUS
        status_persist = OK_STATUS
        present_year = datetime.date.today().year

        status, julian_day = self._validate_reservation_data(
            room,
            present_year,
            start_month,
            start_day,
            days
        )

        if status == OK_STATUS:
            if name in self.hotel_dicc:
                status, _ = self._reserve_hotel_rooms(
                    name,
                    customer_no,
                    room,
                    present_year,
                    julian_day,
                    days
                )
                status_persist, _ = update_data_store(HOTEL_ENTITY, self.hotel_dicc)
            else:
                status = HOTEL_NOT_FOUND

        return int(status + status_persist), None

    def cancel_hotel_reservation(
            self,
            name: str,
            room: int,
            customer_no: str,
            start_month: int,
            start_day: int,
            days: int) -> tuple[int, None]:
        '''
        Metodo publico para cancelar la reservarcion de una habitacion en un
        hotel en el presente anio.
        '''
        status = OK_STATUS
        status_persist = OK_STATUS
        present_year = datetime.date.today().year

        status, julian_day = self._validate_reservation_data(
            room,
            present_year,
            start_month,
            start_day,
            days
        )

        if status == OK_STATUS:
            if name in self.hotel_dicc:
                status, _ = self._unreserve_hotel_rooms(
                    name,
                    customer_no,
                    room,
                    present_year,
                    julian_day,
                    days
                )
                status_persist, _ = update_data_store(HOTEL_ENTITY, self.hotel_dicc)
            else:
                status = HOTEL_NOT_FOUND

        return int(status + status_persist), None
