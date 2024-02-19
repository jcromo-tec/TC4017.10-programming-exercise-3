'''
Programa de pruebas para la Clase Hotel
'''
import sys
import unittest
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))
from hotel import Hotel

class TestCustomer(unittest.TestCase):
    '''
    Clase para probar Customer usando unittest
    '''
    @classmethod
    def setUpClass(cls):
        '''
        Metodo para crear el ambiente para las pruebas
        '''
        cls._hotel = Hotel()

    def test_01_create_hotel(self):
        '''
        Metodo para probar creacion de hotel.
        '''
        self.assertEqual(
            self._hotel.create_hotel(
                'Pretoria Deluxe',
                '125 Delmas Rd',
                10
            ),
            (0, None)
        )

    def test_02_display_hotel(self):
        '''
        Metodo para probar desplegado de hotel.
        '''
        self.assertEqual(
            self._hotel.display_hotel_info('Pretoria Deluxe'),
            (
                0,
                {
                    'name': 'Pretoria Deluxe',
                    'address': '125 Delmas Rd',
                    'rooms': 10
                }
            )
        )

    def test_03_display_hotel_missing(self):
        '''
        Metodo para probar desplegado de hotel no existente.
        '''
        self.assertEqual(
            self._hotel.display_hotel_info('Pretoria Gen Z'),
            (-202, {})
        )

    def test_04_modify_hotel(self):
        '''
        Metodo para probar modificacion de hotel.
        '''
        self.assertEqual(
            self._hotel.modify_hotel_info('Pretoria Deluxe','135 Delmas Rd'),
            (
                0,
                {
                    'name': 'Pretoria Deluxe',
                    'rooms': 10,
                    'address': '135 Delmas Rd'
                }
            )
        )

    def test_05_reserve_room(self):
        '''
        Metodo para probar reservar habitacion de hotel.
        '''
        self.assertEqual(
            self._hotel.reserve_hotel_room(
                'Pretoria Deluxe',
                1,
                'ID660616185|27832629691|1966',
                1,
                1,
                5
            ),
            (0, None)
        )

    def test_05_reserve_room_duplicate(self):
        '''
        Metodo para probar reservar habitacion de hotel duplicada.
        '''
        self.assertEqual(
            self._hotel.reserve_hotel_room(
                'Pretoria Deluxe',
                1,
                'ID660616185|27832629691|1966',
                1,
                1,
                5
            ),
            (-230, None)
        )

    def test_05_reserve_room_duplicate(self):
        '''
        Metodo para probar reservar habitacion de hotel duplicada.
        '''
        self.assertEqual(
            self._hotel.cancel_hotel_reservation(
                'Pretoria Deluxe',
                1,
                'ID660616185|27832629691|1966',
                1,
                1,
                5
            ),
            (0, None)
        )

    @classmethod
    def tearDownClass(cls):
        '''
        Metodo para limpiar la ejecucion de las pruebas
        '''
        result, _ = cls._hotel.delete_hotel('Pretoria Deluxe')
        print('\nHotel deletion', result, '\n')

if __name__ == '__main__':
    unittest.main()
