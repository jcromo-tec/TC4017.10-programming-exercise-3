'''
Codigo fuente de la clase Reservation. Esta clase usa las clases Hotel y
Customer, así como la clase Persistence

La clase reservacion implementa dos metodos, create_reservation y
cancel_reservation

Historia
Fecha           Descripcion del cambio                      Author
17-02-2024      Versión inicial                             A00260430
'''
from hotel import Hotel
from customer import Customer


OK_STATUS = 0

DUPLICATE_CUSTOMER = -101
CUSTOMER_NOT_FOUND = -102
CUSTOMER_ERROR_STATUS = -109
CUSTOMER_INVALID_FIELD = -110
DUPLICATE_HOTEL = -201
HOTEL_NOT_FOUND = -202
HOTEL_INVALID_FIELD = -210
HOTEL_ERROR_STATUS = -209
ROOM_NOT_FOUND = -220
ROOM_NOT_AVAILABLE = -230
RESERVATION_NOT_FOUND = -240


class Reservation():
    '''
    Clase Reservation implementa dos metodos publicos:
    - create_reservation
    - cancel_reservation
    '''

    def __init__(self, hotel: Hotel, customer: Customer):
        self.hotel = hotel
        self.customer = customer

    def create_reservation(
            self,
            customer_no: str,
            hotel_name: str,
            room: int,
            start_month: int,
            start_day: int,
            days: int) -> tuple[list[int], None]:
        '''
        metodo para crear una reservacion usando una estructura con los datos
        del cliente y una estructura con los datos del hotel.

        Regresa una tupla (err, None)
        '''
        status = [OK_STATUS]

        status_h, _ = self.hotel.display_hotel_info(hotel_name)
        status_c, _ = self.customer.display_customer_info(customer_no)

        if (status_h + status_c) == OK_STATUS:
            status, _ = self.hotel.reserve_hotel_room(
                hotel_name,
                room,
                customer_no,
                start_month,
                start_day,
                days
            )
            status = [status]
        else:
            status = [status_h, status_c]

        return status, None

    def cancel_reservation(
            self,
            customer_no: str,
            hotel_name: str,
            room: int,
            start_month: int,
            start_day: int,
            days: int) -> tuple[list[int], None]:
        '''
        metodo para crear una reservacio usando una estructura con los datos
        del cliente y una estructura con los datos del hotel.

        Regresa una tupla (err, None)
        '''
        status = [OK_STATUS]

        status_h, _ = self.hotel.display_hotel_info(hotel_name)
        status_c, _ = self.customer.display_customer_info(customer_no)

        if (status_h + status_c) == OK_STATUS:
            status, _ = self.hotel.cancel_hotel_reservation(
                hotel_name,
                room,
                customer_no,
                start_month,
                start_day,
                days
            )
            status = [status]
        else:
            status = [status_h, status_c]

        return status, None

    def error_message(self, status: int) -> str:
        '''
        Metodo para traducir errores.
        '''
        return {
            OK_STATUS: 'OK',
            DUPLICATE_CUSTOMER: 'Duplicate customer found.',
            CUSTOMER_NOT_FOUND: 'Customer not found.',
            CUSTOMER_ERROR_STATUS: 'Error processing customer request.',
            CUSTOMER_INVALID_FIELD: 'Invalid field values.',
            DUPLICATE_HOTEL: 'Duplicate hotel found.',
            HOTEL_NOT_FOUND: 'Hotel not found.',
            HOTEL_INVALID_FIELD: 'Invalid field values.',
            HOTEL_ERROR_STATUS: 'Error processing hotel request.',
            ROOM_NOT_FOUND: 'Room not found',
            ROOM_NOT_AVAILABLE: 'Room not available.',
            RESERVATION_NOT_FOUND: 'Reservation not found.'
        }.get(status)
