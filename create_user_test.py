import sender_stand_request
import data
from data import user_body


def get_user_body(first_name):
    current_body = data.user_body.copy()
    current_body['firstName'] = first_name
    return current_body

def test_create_user_2_letter_in_first_name_get_success_response():
    user_body = get_user_body('Aa')
    user_response = sender_stand_request.post_new_user(user_body)

    assert user_response.status_code == 201
    assert user_response.json()['authToken'] != ''

    users_table_response = sender_stand_request.get_users_table()

    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
               + user_body["address"] + ",,," + user_response.json()["authToken"]

    assert users_table_response.text.count(str_user) == 1

#Pruebas positivas: Preparación
def positive_assert(first_name):
    user_body = get_user_body(first_name)
    user_response = sender_stand_request.post_new_user(user_body)

    assert user_response.status_code == 201
    assert user_response.json()['authToken'] != ''

    user_table_response = sender_stand_request.get_users_table()

    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
               + user_body["address"] + ",,," + user_response.json()["authToken"]

    assert user_table_response.text.count(str_user) == 1

# Prueba 1. El parámetro "firstName" contiene dos caracteres
def test_create_user_2_letter_in_first_name_get_success_response2():
    positive_assert('Aa')

# Prueba 2. El número permitido de caracteres (15)
def test_create_user_15_letter_in_first_name_get_success_response():
    positive_assert('Aaaaaaaaaaaaaaa')

#Pruebas negativas: Preparación
def negative_assert_symbol(first_name):
    user_body = get_user_body(first_name)
    user_response = sender_stand_request.post_new_user(user_body)

    assert user_response.status_code == 400
    assert user_response.json()['code'] == 400
    assert user_response.json()['message'] == 'Has introducido un nombre de usuario no válido. El nombre solo puede ' \
                                            'contener letras del alfabeto latino, la longitud debe ser de 2 a 15 ' \
                                            'caracteres.'

# Prueba 3. El número de caracteres que es menor a la cantidad permitida (1)
def test_create_user_1_letter_in_first_name_get_error_response():
    negative_assert_symbol('A')

# Prueba 4. El número de caracteres que es mayor a la cantidad permitida (16)
def test_create_user_16_letter_in_first_name_get_error_response():
    negative_assert_symbol('Aaaaaaaaaaaaaaaa')

# Prueba 5. No se permiten espacios
def test_create_user_has_space_in_first_name_get_error_response():
    negative_assert_symbol('A Aaa')

# Prueba 6. No se permiten caracteres especiales
def test_create_user_has_special_symbol_in_first_name_get_error_response():
    negative_assert_symbol("\"№%@\",") #Las barras invertidas (\\) antes de las comillas dobles permiten que el intérprete las trate como parte del string en lugar de como su delimitador

# Prueba 7. No se permiten números
def test_create_user_has_number_in_first_name_get_error_response():
    negative_assert_symbol('123')

#Pruebas 8 y 9: Preparación
def negative_assert_no_first_name(user_body):
    response = sender_stand_request.post_new_user(user_body)

    assert response.status_code == 400
    assert response.json()['code'] == 400
    assert response.json()['message'] == 'No se han aprobado todos los parámetros requeridos' #plataforma: 'No se enviaron todos los parámetros necesarios'

#Prueba 8. Error. La solicitud no contiene el parámetro "firstName"
def test_create_user_no_first_name_get_error_response():
    user_body = data.user_body.copy()
    user_body.pop('firstName')
    negative_assert_no_first_name(user_body)

#Prueba 9. Error. El parámetro "firstName" contiene un string vacío
def test_create_user_empty_first_name_get_error_response():
    user_body = get_user_body('')
    negative_assert_no_first_name(user_body)

#Prueba 10. Se ha pasado otro tipo de parámetro "firstName": número
def test_create_user_number_type_first_name_get_error_response():
    user_body = get_user_body(12)
    response = sender_stand_request.post_new_user(user_body)

    assert response.status_code == 400 #La solicitud devolverá el código de error 500 (aunque, según la lista de comprobación, debería ser 400), pero no te preocupes por eso por ahora.


