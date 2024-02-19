'''
Programa de pruebas para la Clase Reservation
'''
import sys
import unittest
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))
from hotel import Hotel
from customer import Customer
from reservation import Reservation

class TestReservations(unittest.TestCase):
    '''
    Clase para probar reservaciones usando unittest
    '''
    @classmethod
    def setUpClass(cls):
        '''
        Metodo para crear el ambiente para las pruebas
        '''
        cls._hotel = Hotel()
        cls._customer = Customer()
        cls._reservation = Reservation(cls._hotel, cls._customer)
        result, hotel_data = cls._hotel.create_hotel(
            'Pretoria Deluxe','125 Delmas Rd',10
        )
        print('Hotel creation', result, hotel_data, '\n')
        result, cls._cust_no = cls._customer.create_customer(
            'JC','Romo','ID660616185','27832629691',1966
        )
        print('Customer creation', result, cls._cust_no, '\n')

    def test_01_create_reservation(self):
        '''
        Metodo para probar creacion de reservacion
        '''
        self.assertEqual(
            self._reservation.create_reservation(
                self._cust_no,
                'Pretoria Deluxe',
                1,
                1,
                1,
                5
            ),
            ([0], None)
        )

    def test_02_create_reservation_duplicate(self):
        '''
        Metodo para probar creacion de reservacion duplicada
        '''
        self.assertEqual(
            self._reservation.create_reservation(
                self._cust_no,
                'Pretoria Deluxe',
                1,
                1,
                1,
                5
            ),
            ([-230], None)
        )

    def test_03_cancel_reservation(self):
        '''
        Metodo para probar cancelacion de reservacion
        '''
        self.assertEqual(
            self._reservation.cancel_reservation(
                self._cust_no,
                'Pretoria Deluxe',
                1,
                1,
                1,
                5
            ),
            ([0], None)
        )

    def test_04_cancel_reservation_missing(self):
        '''
        Metodo para probar cancelacion de reservacion no existente
        '''
        self.assertEqual(
            self._reservation.cancel_reservation(
                self._cust_no,
                'Pretoria Deluxe',
                1,
                1,
                1,
                5
            ),
            ([-220], None)
    )

    @classmethod
    def tearDownClass(cls):
        '''
        Metodo para limpiar la ejecucion de las pruebas
        '''
        result, _ = cls._hotel.delete_hotel('Pretoria Deluxe')
        print('\nHotel deletion', result, '\n')
        result, _ = cls._customer.delete_customer(cls._cust_no)
        print('Customer deletion', result, '\n')

if __name__ == '__main__':
    unittest.main()
