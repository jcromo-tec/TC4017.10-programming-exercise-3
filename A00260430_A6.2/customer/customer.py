'''
Codigo fuente de la clase Customer. Esta clase usa la clase Persistence.

La clase Customer implementa los metodos create_customer, delete_customer,
display_customer_info, modify_customer_info

Historia
Fecha           Descripcion del cambio                      Author
17-02-2024      Version inicial                             A00260430
'''
import re
from persistence import update_data_store, load_data_store


OK_STATUS = 0
ERROR_STATUS = -109
DUPLICATE_CUSTOMER = -101
CUSTOMER_NOT_FOUND = -102
INVALID_FIELD = -110
CUSTOMER_ENTITY = 'customer'


class Customer():
    '''
    Clase Customer. Esta clase crea un diccionario con datos contenidos en un archivo
    con formato JSON nombrado customer.json.

    La estructura del cliente es un diccionario con los campos
    - names (nombres)
    - surname (apellidos)
    - id_doc_no (no. documento de identificacion alfanumerico)
    - phone_no (no telefono numerico)
    - year_dob (anio de nacimiento)

    Metodos privados
    + _validate_customer_data - verifica que los datos sean del tipo correcto

    Metodos publicos
    + create_customer - crea un nuevo registro del cliente.
    + delete_customer - borra un registro existente del cliente
    + display_customer - obtiene los datos de un registro existente del cliente
    + modify_custimer - actualiza los datos de un registro existente del cliente
    '''
    def __init__(self):
        self.loaded_data, self.customer_dicc = load_data_store(CUSTOMER_ENTITY)

    def _validate_customer_data(
            self,
            partial: bool,
            names: str,
            surname: str,
            id_doc_no: str,
            phone_no: str,
            year_dob: int):
        '''
        Este metodo valida los campos del cliente.

        El metodo retorna una tupla (err, field_list)
        '''
        status = OK_STATUS
        field_list = {}
        if (
             (names is None or not isinstance(names, str) or names == '')
             and partial):
            status = INVALID_FIELD
        field_list['names'] = (
            bool(isinstance(names, str)),
            names
        )
        if (
             (surname is None or not isinstance(surname, str) or surname == '')
             and partial):
            status = INVALID_FIELD
        field_list['surname'] = (
            bool(isinstance(surname, str)),
            surname
        )
        if (
             (id_doc_no is None or not isinstance(id_doc_no, str) or id_doc_no == '')
             and not bool(re.match('^[a-zA-Z0-9]+$', id_doc_no))
             and partial):
            status = INVALID_FIELD
        field_list['id_doc_no'] = (
            bool(isinstance(id_doc_no, str)
                 and bool(re.match('^[a-zA-Z0-9]+$', id_doc_no))),
            id_doc_no
        )
        if (
             (phone_no is None or not isinstance(phone_no, str) or phone_no == '')
             and not bool(re.match('^[0-9]+$', phone_no))
             and partial):
            status = INVALID_FIELD
        field_list['phone_no'] = (
            bool(isinstance(phone_no, str)
                 and bool(re.match('^[0-9]+$', phone_no))),
            phone_no
        )
        if (
             (year_dob is None or not isinstance(year_dob, int) or year_dob <= 0)
             and partial):
            status = INVALID_FIELD
        field_list['year_dob'] = (
            bool(isinstance(year_dob, int)),
            year_dob
        )

        return status, field_list

    def create_customer(
            self,
            names: str,
            surname: str,
            id_doc_no: str,
            phone_no: str,
            year_dob: int) -> tuple[int, str]:
        '''
        Este metodo crea un cliente en el diccionario de clientes. El diccionario
        de clientes es almacenado en el archivo customer.json

        El metodo retorna una tupla (err, customer_no)
        '''
        status = OK_STATUS
        status_persist = OK_STATUS

        status, cust_field_list = self._validate_customer_data(
            False,
            names,
            surname,
            id_doc_no,
            phone_no,
            year_dob
        )
        if status == OK_STATUS:
            customer_key = id_doc_no + '|' + phone_no + '|' + str(year_dob)
            if customer_key in self.customer_dicc:
                status = DUPLICATE_CUSTOMER
                customer_key = None
            else:
                customer_data = {}
                customer_data['names'] = cust_field_list['names'][1]
                customer_data['surname'] = cust_field_list['surname'][1]
                customer_data['id_doc_no'] = cust_field_list['id_doc_no'][1]
                customer_data['phone_no'] = cust_field_list['phone_no'][1]
                customer_data['year_dob'] = cust_field_list['year_dob'][1]
                self.customer_dicc[customer_key] = customer_data
                status_persist, _ = update_data_store(CUSTOMER_ENTITY, self.customer_dicc)

        return int(status + status_persist), customer_key

    def delete_customer(self, customer_no: str):
        '''
        Este metodo remueve un cliente en el diccionario de clientes.

        El diccionario de clientes es almacenado en el archivo customer.json

        Regresa una tupla (err, None)
        '''
        status = OK_STATUS
        status_persist = OK_STATUS

        if customer_no in self.customer_dicc:
            self.customer_dicc.pop(customer_no)
            status_persist, _ = update_data_store(CUSTOMER_ENTITY, self.customer_dicc)
        else:
            status = CUSTOMER_NOT_FOUND

        return int(status + status_persist), None

    def display_customer_info(self, customer_no: str):
        '''
        Este metodo depliega los datos de un cliente en el diccionario de
        clientes.

        El diccionario de clientes es almacenado en el archivo customer.json

        Regresa una tupla (err, diccionario)
        '''
        status = OK_STATUS
        customer_data = {}

        if customer_no in self.customer_dicc:
            customer_data = self.customer_dicc[customer_no]
        else:
            status = CUSTOMER_NOT_FOUND

        return int(status), customer_data

    def modify_customer_info(
            self,
            customer_no: str,
            names: str,
            surname: str,
            id_doc_no: str,
            phone_no: str,
            year_dob: int,):
        '''
        Este metodo modifica los datos de un cliente en el diccionario de
        clientes.

        El diccionario de clientes es almacenado en el archivo customer.json

        Regresa una tupla (err, diccionario)
        '''
        status = OK_STATUS
        status_persist = OK_STATUS
        customer_data = {}

        status, cust_field_list = self._validate_customer_data(
            True,
            names,
            surname,
            id_doc_no,
            phone_no,
            year_dob
        )

        if status == OK_STATUS:
            if customer_no in self.customer_dicc:
                if cust_field_list['names'][0]:
                    customer_data['names'] = cust_field_list['names'][1]
                else:
                    customer_data['names'] = self.customer_dicc[customer_no]['names']
                if cust_field_list['surname'][0]:
                    customer_data['surname'] = cust_field_list['surname'][1]
                else:
                    customer_data['surname'] = self.customer_dicc[customer_no]['surname']
                if cust_field_list['id_doc_no'][0]:
                    customer_data['id_doc_no'] = cust_field_list['id_doc_no'][1]
                else:
                    customer_data['id_doc_no'] = \
                        self.customer_dicc[customer_no]['id_doc_no']
                if cust_field_list['phone_no'][0]:
                    customer_data['phone_no'] = cust_field_list['phone_no'][1]
                else:
                    customer_data['phone_no'] = \
                        self.customer_dicc[customer_no]['phone_no']
                if cust_field_list['year_dob'][0]:
                    customer_data['year_dob'] = cust_field_list['year_dob'][1]
                else:
                    customer_data['year_dob'] = \
                        self.customer_dicc[customer_no]['year_dob']
                self.customer_dicc[customer_no] = customer_data
                status_persist, _ = update_data_store(
                    CUSTOMER_ENTITY, self.customer_dicc
                )
            else:
                status = CUSTOMER_NOT_FOUND
        else:
            status = INVALID_FIELD

        return int(status + status_persist), customer_data
