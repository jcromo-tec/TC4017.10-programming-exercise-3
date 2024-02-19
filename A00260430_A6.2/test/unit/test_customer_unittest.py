'''
Programa de pruebas para la Clase Customer
'''
import sys
import unittest
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))
from customer import Customer

class TestCustomer(unittest.TestCase):
    '''
    Clase para probar Customer usando unittest
    '''
    @classmethod
    def setUpClass(cls):
        '''
        Metodo para crear el ambiente para las pruebas
        '''
        cls._customer = Customer()

    def test_01_create_customer(self):
        '''
        Metodo para probar creacion de cliente
        '''
        self.assertEqual(
            self._customer.create_customer(
                'JC',
                'Romo',
                'ID660616185',
                '27832629691',
                1966),
            (0, 'ID660616185|27832629691|1966')
        )

    def test_02_create_duplicate_customer(self):
        '''
        Metodo para probar creacion de cliente duplicado
        '''
        self.assertEqual(
            self._customer.create_customer(
                'JC',
                'Romo',
                'ID660616185',
                '27832629691',
                1966),
            (-101, None)
        )

    def test_03_modify_customer(self):
        '''
        Metodo para probar modificacion del cliente
        ''' 
        self.assertEqual(
            self._customer.modify_customer_info(
                'ID660616185|27832629691|1966',
                'Juan Carlos',
                'Romo',
                'ID660616185',
                '27832629691',
                1966
            ),
            (
                0,
                {
                    'names': 'Juan Carlos',
                    'surname': 'Romo',
                    'id_doc_no': 'ID660616185',
                    'phone_no': '27832629691',
                    'year_dob': 1966
                }
            )
        )

    def test_04_display_customer(self):
        '''
        Metodo para probar desplegado del cliente
        '''
        self.assertEqual(
            self._customer.display_customer_info(
                'ID660616185|27832629691|1966'
            ),
            (
                0,
                {
                    'names': 'Juan Carlos',
                    'surname': 'Romo',
                    'id_doc_no': 'ID660616185',
                    'phone_no': '27832629691',
                    'year_dob': 1966
                }
            )
        )

    def test_05_modify_missing_customer(self):
        '''
        Metodo para probar modificacion de cliente no existente.
        '''
        self.assertEqual(
            self._customer.modify_customer_info(
                'ID660616184|27832629691|1966',
                'Juan Carlos',
                'Romo',
                'ID660616185',
                '27832629691',
                1966),
            (-102, {})
        )

    def test_06_display_missing_customer(self):
        '''
        Metodo para probar desplegado de cliente no existente.
        '''

        self.assertEqual(
            self._customer.display_customer_info(
                'ID660616184|27832629691|1966'
            ),
            (-102, {})
        )

    def test_07_delete_customer(self):
        '''
        Metodo para probar desplegado de cliente no existente.
        '''
        self.assertEqual(
                self._customer.delete_customer(
                    'ID660616185|27832629691|1966'
                ),
            (0, None)
        )

if __name__ == '__main__':
    unittest.main()
