from app_ballon.dto import DTOInput, DTOOutput


def baloon_calculate(dto_input: DTOInput, size_ballon: int) -> DTOOutput:
    p_ox_d = DTOInput.pressure_oxygen
    p_ar_d = DTOInput.pressure_argon
    p_ni_d = DTOInput.pressure_nirtogen
    #Дописать формулу сюда формулу расчета по константе + усложнить расчет газа как следует
    #Сделать второе API по принципу приложения app_ballon
