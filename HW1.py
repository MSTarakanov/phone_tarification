# Подключим нужные модули
from datetime import datetime as dt, date

# Присвоим каждому типу события числовой код в виде константы, а также определим их стоимость
EVENT_TOPUP = 1                         # пополнение счета
EVENT_INC_CALL = 2                      # входящий звонок
EVENT_INC_CALL_HOME_PRICE = 0           # стоимость входящих звонков в домашней сети
EVENT_INC_CALL_ROAMING_PRICE = 8        # стоимость входящих звонков в роуминге
EVENT_OUT_CALL = 3                      # исходящий звонок
EVENT_OUT_CALL_HOME_PRICE = 2           # стоимость исходящих звонков в домашней сети
EVENT_OUT_CALL_ROAMING_PRICE = 20       # стоимость исходящих звонков в роуминге
EVENT_INC_SMS = 4                       # входящее смс
EVENT_INC_SMS_HOME_PRICE = 0            # стоимость входящих смс в домашней сети
EVENT_INC_SMS_ROAMING_PRICE = 0         # стоимость входящих смс в роуминге
EVENT_OUT_SMS = 5                       # исходящее смс
EVENT_OUT_SMS_HOME_PRICE = 1            # стоимость исходящего смс в домашней сети
EVENT_OUT_SMS_ROAMING_PRICE = 5         # стоимость исходящего смс в роуминге
EVENT_WEB_SESSION = 6                   # интернет сессия
EVENT_WEB_SESSION_ROAMING_PRICE = 5     # стоимость одного Мб в роуминге
EVENT_WEB_SESSION_HOME_PRICE = 0.2      # стоимость одного Мб в домашней сети
EVENT_EXIT_ROAMING = 7                  # выход из роуминга
EVENT_ENTER_ROAMING = 8                 # вход в роуминг

# дополнительные константы
MAX_MESSAGE_LEN = 70
MIN_CALL_TIME = 3

# константы, определяющие события, которые нужно описать
INC_CALL_HOME = 11
INC_CALL_ROAMING = 22
OUT_CALL_HOME = 33
OUT_CALL_ROAMING = 44
INC_SMS = 55
OUT_SMS_HOME = 66
OUT_SMS_ROAMING = 77
MBS_HOME = 88
MBS_ROAMING = 99
TOPUP = 100

# Добавим событий в журнал событий (список, где каждый следующий жлемент имеет дату больше или равную предыдущего,
# как в настоящем журнале)
events = [{'date': dt(2021, 3, 15, 14, 56, 40, 0),      'event_id': EVENT_TOPUP, 'sum': 500},
          {'date': dt(2021, 3, 15, 15, 30, 20, 54),     'event_id': EVENT_INC_CALL, 'phone': "+79122697995", 'time': 61},
          {'date': dt(2021, 3, 15, 15, 40, 2, 22),      'event_id': EVENT_INC_CALL, 'phone': "+79122697995", 'time': 61},
          {'date': dt(2021, 3, 15, 18, 14, 59, 0),      'event_id': EVENT_OUT_SMS, 'phone': "+79106541234", 'text': 'Ок'},
          # смс больше 70 символов
          {'date': dt(2021, 3, 15, 18, 20, 20, 999),    'event_id': EVENT_OUT_SMS, 'phone': "+79106541234", 'text': "Если вы полагаете, что труд облагораживает человека, зайдите на ближайшую стройку — посмотрите на благородных."},
          {'date': dt(2021, 3, 15, 19, 20, 40, 0),      'event_id': EVENT_INC_SMS, 'phone': "+79106541234", 'text': "Перезвони мне"},
          {'date': dt(2021, 3, 15, 22, 0, 5, 5),        'event_id': EVENT_OUT_CALL, 'phone': "+79106541234", 'time': 240},
          {'date': dt(2021, 3, 16, 7, 20, 0, 65),       'event_id': EVENT_ENTER_ROAMING},
          {'date': dt(2021, 3, 16, 8, 42, 54, 0),       'event_id': EVENT_OUT_SMS, 'phone': "+79106541234", 'text': "Перезвони мне"},
          {'date': dt(2021, 3, 16, 9, 0, 0, 0),         'event_id': EVENT_INC_CALL, 'phone': "+79261112233", 'time': 40},
          {'date': dt(2021, 3, 16, 9, 15, 20, 30),      'event_id': EVENT_INC_CALL, 'phone': "+79261112233", 'time': 40},
          {'date': dt(2021, 3, 17, 10, 11, 30, 300),    'event_id': EVENT_WEB_SESSION, 'mbs': 10},
          {'date': dt(2021, 3, 17, 12, 12, 12, 12),     'event_id': EVENT_WEB_SESSION, 'mbs': 20},
          {'date': dt(2021, 3, 17, 12, 40, 44, 44),     'event_id': EVENT_OUT_CALL, 'phone': "+79106541234", 'time': 72},
          {'date': dt(2021, 3, 17, 15, 30, 0, 0),       'event_id': EVENT_EXIT_ROAMING},
          {'date': dt(2021, 3, 18, 10, 10, 30, 22),     'event_id': EVENT_OUT_CALL, 'phone': "+79164321234", 'time': 2},
          {'date': dt(2021, 3, 18, 12, 18, 3, 2),       'event_id': EVENT_WEB_SESSION, 'mbs': 2}]


# Функция, возвращающая информацию о звонке в виде словаря
def call_info(event, roaming):
    call_info = {'calls_count': 1, 'calls_time': event['time'], 'sum': 0}  # инициализация словаря
    if event['time'] > MIN_CALL_TIME:  # разговоры меньше 3 секунд не валидируются
        if not roaming:
            if event['event_id'] == EVENT_INC_CALL:
                # округление в большую сторону происходит с помощью перевода числа в отрицательное
                # так как питон округляет в меньшую
                call_info['sum'] += -int(-event['time'] // 60) * EVENT_INC_CALL_HOME_PRICE
            elif event['event_id'] == EVENT_OUT_CALL:
                call_info['sum'] += -int(-event['time'] // 60) * EVENT_OUT_CALL_HOME_PRICE
        else:
            if event['event_id'] == EVENT_INC_CALL:
                call_info['sum'] += -int(-event['time'] // 60) * EVENT_INC_CALL_ROAMING_PRICE
            elif event['event_id'] == EVENT_OUT_CALL:
                call_info['sum'] += -int(-event['time'] // 60) * EVENT_OUT_CALL_ROAMING_PRICE
    return call_info


# Функция, возвращающая информацию о смс в виде словаря
def sms_info(event, roaming):
    sms_info = {'sms_count': 1, 'sum': 0}
    if not roaming:
        if event['event_id'] == EVENT_INC_SMS:
            # округление в большую сторону происходит с помощью перевода числа в отрицательное
            # так как питон округляет в меньшую
            sms_info['sum'] += -int(-len(event['text']) // MAX_MESSAGE_LEN) * EVENT_INC_SMS_HOME_PRICE
        elif event['event_id'] == EVENT_OUT_SMS:
            sms_info['sum'] += -int(-len(event['text']) // MAX_MESSAGE_LEN) * EVENT_OUT_SMS_HOME_PRICE
    else:
        if event['event_id'] == EVENT_INC_SMS:
            sms_info['sum'] += -int(-len(event['text']) // MAX_MESSAGE_LEN) * EVENT_INC_SMS_ROAMING_PRICE
        elif event['event_id'] == EVENT_OUT_SMS:
            sms_info['sum'] += -int(-len(event['text']) // MAX_MESSAGE_LEN) * EVENT_OUT_SMS_ROAMING_PRICE
    return sms_info


# Функция, которая создает новый ключ со значением словаря, содержащего суммированную информацию о ключе-событии
# или суммирует информацию, если такой ключ события уже имеется
# параметры:
# info - словарь словарей (ключ - событие, значение - словарь информации),
# adding_info - словарь информации, который нужно добавить,
# kind_info - ключ-событие (строка)
def add_info(info, adding_info, kind_info):
    if kind_info not in info:
        info[kind_info] = adding_info
    else:
        for key in info[kind_info]:
            info[kind_info][key] += adding_info[key]


# Функция, которая обрабатывает лист всех событий и возвращает словарь словарей со всей нужной для вывода информации
def account_info(date_from, date_to, events):
    info = {}           # словарь словарей всех событий, которые нужно вывести пользователю
    roaming = False     # по умолчанию пользователь находится не в роуминге
    for event in events:
        # определение константы для более читабельного кода (находится ли дата в заданном диапазоне)
        DATE_IS_RELEVANT = event['date'].date() >= date_from and event['date'].date() <= date_to
        if event['event_id'] == EVENT_EXIT_ROAMING:
            roaming = False
        elif event['event_id'] == EVENT_ENTER_ROAMING:
            roaming = True
        # каждому событию, которое нужно описать соответсвует свой индентификатор (например, inc_call_home)
        if DATE_IS_RELEVANT:
            if event['event_id'] == EVENT_INC_CALL and DATE_IS_RELEVANT and not roaming:
                add_info(info, call_info(event, roaming), INC_CALL_HOME)
            elif event['event_id'] == EVENT_INC_CALL and DATE_IS_RELEVANT and roaming:
                add_info(info, call_info(event, roaming), INC_CALL_ROAMING)
            elif event['event_id'] == EVENT_OUT_CALL and DATE_IS_RELEVANT and not roaming:
                add_info(info, call_info(event, roaming), OUT_CALL_HOME)
            elif event['event_id'] == EVENT_OUT_CALL and DATE_IS_RELEVANT and roaming:
                add_info(info, call_info(event, roaming), OUT_CALL_ROAMING)
            elif event['event_id'] == EVENT_OUT_SMS and DATE_IS_RELEVANT and roaming:
                add_info(info, sms_info(event, roaming), OUT_SMS_ROAMING)
            elif event['event_id'] == EVENT_OUT_SMS and DATE_IS_RELEVANT and not roaming:
                add_info(info, sms_info(event, roaming), OUT_SMS_HOME)
            elif event['event_id'] == EVENT_INC_SMS and DATE_IS_RELEVANT:
                add_info(info, sms_info(event, roaming), INC_SMS)
            elif event['event_id'] == EVENT_WEB_SESSION and DATE_IS_RELEVANT and roaming:
                add_info(info, {'mbs': event['mbs'], 'sum': event['mbs'] * EVENT_WEB_SESSION_ROAMING_PRICE}, MBS_ROAMING)
            elif event['event_id'] == EVENT_WEB_SESSION and DATE_IS_RELEVANT and not roaming:
                add_info(info, {'mbs': event['mbs'], 'sum': event['mbs'] * EVENT_WEB_SESSION_HOME_PRICE}, MBS_HOME)
            elif event['event_id'] == EVENT_TOPUP and DATE_IS_RELEVANT:
                add_info(info, {'sum': event['sum']}, TOPUP)
    return info


# Функция, которая подсчитывает все расходы
def calculate_expenses(info):
    expenses = 0
    for key in info:
        # складываем все сумммы, исключая пополнения
        if info[key].get('sum') and key != TOPUP:
            expenses += info[key]['sum']
    return expenses


# Функция, которая выводит обработанную информацию на экран
def print_info(date_from, date_to, events):
    info = account_info(date_from, date_to, events)
    if info.get(TOPUP):
        print('Общая сумма пополнения: ' + str(info[TOPUP]['sum']) + ' руб')
    # если хоть какое-то событие, связанное с расходами (даже нулевыми, исключения: вход и выход в/из роуминг)
    # произошло, то выводится детализация
    if info:
        print('Общие расходы: ' + str(calculate_expenses(info)) + ' руб')
        print('Детализация расходов:')
    if info.get(INC_CALL_HOME):
        print('Входящие звонки (домашняя сеть): ' + str(info[INC_CALL_HOME]['calls_count']) +
              ', общая продолжительность: ' + str(-int(-info[INC_CALL_HOME]['calls_time'] // 60)) +
              ' мин, списано: ' + str(info[INC_CALL_HOME]['sum']) + ' руб')
    if info.get(INC_CALL_ROAMING):
        print('Входящие звонки (роуминг): ' + str(info[INC_CALL_ROAMING]['calls_count']) +
              ', общая продолжительность: ' + str(-int(-info[INC_CALL_ROAMING]['calls_time'] // 60)) +
              ' мин, списано: ' + str(info[INC_CALL_ROAMING]['sum']) + ' руб')
    if info.get(OUT_CALL_HOME):
        print('Исходящие звонки (домашняя сеть): ' + str(info[OUT_CALL_HOME]['calls_count']) +
              ', общая продолжительность: ' + str(-int(-info[OUT_CALL_HOME]['calls_time'] // 60)) +
              ' мин, списано: ' + str(info[OUT_CALL_HOME]['sum']) + ' руб')
    if info.get(OUT_CALL_ROAMING):
        print('Исходящие звонки (роуминг): ' + str(info[OUT_CALL_ROAMING]['calls_count']) +
              ', общая продолжительность: ' + str(-int(-info[OUT_CALL_ROAMING]['calls_time'] // 60)) +
              ' мин, списано: ' + str(info[OUT_CALL_ROAMING]['sum']) + ' руб')
    if info.get(INC_SMS):
        print('Входящие СМС: ' + str(info[INC_SMS]['sms_count']) + ', списано: ' +
              str(info[INC_SMS]['sum']) + ' руб')
    if info.get(OUT_SMS_HOME):
        print('Исходящие СМС (домашняя сеть): ' + str(info[OUT_SMS_HOME]['sms_count']) + ', списано: ' +
              str(info[OUT_SMS_HOME]['sum']) + ' руб')
    if info.get(OUT_SMS_ROAMING):
        print('Исходящие СМС (роуминг): ' + str(info[OUT_SMS_ROAMING]['sms_count']) + ', списано: ' +
              str(info[OUT_SMS_ROAMING]['sum']) + ' руб')
    if info.get(MBS_HOME):
        print('Мобильный интернет (домашняя сеть): ' + str(info[MBS_HOME]['mbs']) + ' Мб, списано: ' +
              str(info[MBS_HOME]['sum']) + ' руб')
    if info.get(MBS_ROAMING):
        print('Мобильный интернет (роуминг): ' + str(info[MBS_ROAMING]['mbs']) + ' Мб, списано: ' +
              str(info[MBS_ROAMING]['sum']) + ' руб')
    # если события в журнале по заданной дате не найдены
    if not info:
        print('Данные не найдены')


# Функция валидации дат, при успешном валидировании врзвращает тюпл из двух дат:
def input_date_with_validation():
    date_from = None
    date_to = None
    while not date_from:
        input_date_from = input('Введите начальную дату (ДД.ММ.ГГГГ): ')
        if input_date_from == 'exit':
            exit(1)
        # конструкция try-except позволяет правильно обработать введенное значение
        try:
            # если дата введена в верном форматеЦ
            date_from = dt.strptime(input_date_from, '%d.%m.%Y').date()
        except:
            # если поймано исключение/ошибка
            print('Некорректная дата')
    while not date_to or date_from > date_to:
        input_date_to = input('Введите конечную дату (ДД.ММ.ГГГГ): ')
        if input_date_to == 'exit':
            exit(1)
        try:
            date_to = dt.strptime(input_date_to, '%d.%m.%Y').date()
            # конструкция ассерт позволяет вызвать исключение, когда начальная дата больше конечной
            assert(date_from <= date_to)
        except:
            print('Некорректная дата')
    return date_from, date_to


# ключ сортировки
def sort_by_date(input_note):
    return input_note['date']


# основная функция, с опросом пользователя до тех пор, пока он не введет "exit"
def main():
    events.sort(key=sort_by_date)  # на всякий случай отсортируем список
    while (1):
        print('Для выхода из программы введите "exit"')
        date_from, date_to = input_date_with_validation()
        print_info(date_from, date_to, events)


main()
