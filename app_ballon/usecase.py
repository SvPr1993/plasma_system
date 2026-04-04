from decouple import config

from app_ballon.dto import DTOInput, DTOOutput

OXYGEN_BALLON = config("OXYGEN_BALLON")
ARGON_BALLON = config("ARGON_BALLON")
NITROGEN_BALLON = config("NITROGEN_BALLON")


def baloon_calculate(dto_input, size_ballon) -> DTOOutput:
    ''' Эта функция является аркестратором вычислений '''
    volume_liters = dto_input.volume_liters
    pressure_bar = dto_input.pressure_bar
    temperature_Celsius = dto_input.temperature_Celsius

    mass_kg_oxygen = pressure_oxygen(volume_liters, pressure_bar, temperature_Celsius)
    mass_kg_argon = pressure_argon(volume_liters, pressure_bar, temperature_Celsius)
    mass_kg_nitrogen = pressure_nitrogen(volume_liters, pressure_bar, temperature_Celsius)

    oxygen_bull = False
    argon_bull = False
    nitrogen_bull = False
    result_bull = False

    if mass_kg_oxygen <= float(OXYGEN_BALLON):
        print("Работы запрешены")
    else:
        print("Все хорошо")
        oxygen_bull = True

    if mass_kg_argon <= float(ARGON_BALLON):
        print("Работы запрешены")
    else:
        print("Все хорошо")
        argon_bull = True

    if mass_kg_nitrogen <= float(NITROGEN_BALLON):
        print("Работы запрешены")
    else:
        print("Все хорошо")
        nitrogen_bull = True

    if oxygen_bull is True and argon_bull is True and nitrogen_bull is True:
        result_bull = True
    return result_bull


# Данные volume_liters, pressure_bar, temperature_сelsius приходят из API сейчас указаны данные при идеальных условиях

################## КИСЛОРОД

def pressure_oxygen(volume_liters, pressure_bar, temperature_Celsius):
    # Константы
    R = 8.314  # газовая постоянная
    M = 0.032  # молярная масса кислорода (кг/моль)

    # Переводим в нужные единицы
    volume_cubic_meters = volume_liters / 1000  # литры в кубометры
    pressure_pascals = pressure_bar * 100000  # бары в Паскали
    temperature_kelvins = temperature_Celsius + 273.15  # Цельсий в Кельвины

    # Формула: масса = (P * V * M) / (R * T)
    mass_kg_oxygen = (pressure_pascals * volume_cubic_meters * M) / (R * temperature_kelvins)

    return mass_kg_oxygen


################## АРГОН

def pressure_argon(volume_liters, pressure_bar, temperature_Celsius):
    # Константы
    R = 8.314  # газовая постоянная (Дж/(моль·К))
    M = 0.039948  # молярная масса аргона (кг/моль) - 39.948 г/моль

    # Переводим в нужные единицы
    volume_cubic_meters = volume_liters / 1000  # литры в кубометры
    pressure_pascals = pressure_bar * 100000  # бары в Паскали
    temperature_kelvins = temperature_Celsius + 273.15  # Цельсий в Кельвины

    # Формула: масса = (P * V * M) / (R * T)
    mass_kg_argon = (pressure_pascals * volume_cubic_meters * M) / (R * temperature_kelvins)

    return mass_kg_argon


################## АЗОТ

def pressure_nitrogen(volume_liters, pressure_bar, temperature_Celsius):
    # Константы
    R = 8.314  # газовая постоянная (Дж/(моль·К))
    M = 0.028014  # молярная масса азота N₂ (кг/моль) - 28.014 г/моль

    # Переводим в нужные единицы
    volume_cubic_meters = volume_liters / 1000  # литры в кубометры
    pressure_pascals = pressure_bar * 100000  # бары в Паскали
    temperature_kelvins = temperature_Celsius + 273.15  # Цельсий в Кельвины

    # Формула: масса = (P * V * M) / (R * T)
    mass_kg_nitrogen = (pressure_pascals * volume_cubic_meters * M) / (R * temperature_kelvins)

    return mass_kg_nitrogen


# Нужно возвращать результат в виде json - какие параметры передались после работы функций
# +Прокинуть константы через decouple по принципу приложения IpInfo13
# +Привести формулы в порядок, убрать принты и и так далее