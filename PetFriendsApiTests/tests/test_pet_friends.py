from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password
import os

pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """Проверка получения ключа"""
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """Проверка получения спика питомцев"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Котя', animal_type='Милота', age='1', pet_photo='images/cat1.jpg'):
    """Проверка возможности создания нового питомца с фото"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name


def test_update_pet_info(name='Котяра', animal_type='Измененный', age='3'):
        """Проверка возможности изменения данных питомца"""
        _, auth_key = pf.get_api_key(valid_email, valid_password)
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
        if len(my_pets['pets']) > 0:
            status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
            assert status == 200
            assert result['name'] == name
        else:
            raise Exception("Питомцы отсутствуют")


def test_delete_self_pet():
    """Проверка возможности удаления питомца"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Кот", "Экзот", "2", "images/cat2.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    assert status == 200
    assert pet_id not in my_pets.values()


def test_add_new_pet_without_photo(name='Кот', animal_type='Новый', age='7'):
    """Проверка возможности добавления нового питомца без фото"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name


def test_add_pet_photo(pet_photo='images/cat2.jpg'):
    """Проверка возможности добавления фото к созданному питомцу"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, api_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(api_key, 'my_pets')
    if len(my_pets['pets']) > 0:
        status, result = pf.add_pet_photo(api_key, my_pets['pets'][0]['id'], pet_photo)
        _, my_pets = pf.get_list_of_pets(api_key, 'my_pets')
        assert status == 200
        assert result['pet_photo'] == my_pets['pets'][0]['pet_photo']


def test_get_api_key_for_invalid_email(email=invalid_email, password=valid_password):
    """Проверка возможности получения ключа с некорректным адресом почты"""
    status, result = pf.get_api_key(email, password)
    assert status == 403


def test_get_api_key_for_invalid_password(email=valid_email, password=invalid_password):
    """Проверка возможности получения ключа с некорректным паролем"""
    status, result = pf.get_api_key(email, password)
    assert status == 403


def test_get_my_pets_list(filter='my_pets'):
    """Проверка получения спика питомцев с фильтром my_pets"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) == 0 or len(result['pets']) > 0


def test_add_new_pet_without_data(name='', animal_type='', age='', pet_photo='images/cat3.jpg'):
    """Проверка возможности создания питомца без заполненных данных.
    Ожидаемый код ответа 500, результат код ответа 200."""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200


def test_add_new_pet_with_invalid_age(name='Cat', animal_type='cat', age='CatКОТCAT'):
    """Проверка возможности добавления нового питомца с буквами вместо чисел в графе возраст
    Ожидаемый код ответа 500, результат код ответа 200."""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200


def test_add_new_pet_without_big_data(name='апвпвпвр5н758697674474gdhdhrufsdj;j;k;u9yly%$^$$^#^dfddre', animal_type='БольшойКот', age='8', pet_photo='images/cat4.jpg'):
    """Проверка возможности добавления нового питомца c очень большим количеством символов в имени
    Ожидаемый код ответа 500, результат код ответа 200."""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200


def test_add_pet_negative_age_number(name='Баттон', animal_type='Кот', age='-3', pet_photo='images/cat2.jpg'):
    """Проверка добавление питомца с отрицательным числом в поле возраст.
    Ожидаемый код ответа 500, результат код ответа 200."""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200


def test_add_pet_with_three_digit_age_number(name='Какойто', animal_type='Кот', age='98765', pet_photo='images/cat3.jpg'):
    """Проверка добавление питомца с числом более двух знаков в поле возраст.
    Ожидаемый код ответа 500, результат код ответа 200."""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200








