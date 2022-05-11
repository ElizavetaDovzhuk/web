def check_password(password):
    q = 0
    bucvy = ['йцу', 'цук', 'уке', 'кен', 'енг', 'нгш', 'гшщ', 'шщз', 'щзх', 'зхъ', 'фыв', 'ыва',
             'вап',
             'апр', 'про', 'рол', 'олд', 'лдж', 'джэ', 'ячс', 'чсм', 'сми', 'мит', 'ить', 'тьб',
             'ьбю',
             'qwe', 'wer', 'ert', 'rty', 'tyu', 'yui', 'uio', 'iop', 'asd', 'sdf', 'dfg', 'fgh',
             'ghj',
             'hjk', 'jkl', 'zxc', 'xcv', 'cvb', 'vbn', 'bnm', 'жэё']
    stroka1 = 'qwertyuyiopasdfghjklzxcvbnm'
    stroka2 = 'QWERTYUIOPASDFGHJKLZXCVBNM'
    stroka3 = 'йцукенгшщзххххххххъфывапролджэячсмитьбю'
    stroka4 = 'ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЛЖЭЯЧСМИТЬБЮ'
    q1 = 0
    q2 = 0
    s1 = 0
    s2 = 0
    s3 = 0
    s4 = 0
    if len(password) > 8:
        for i in password:
            if i in stroka1:
                s1 = 1
            if i in stroka2:
                s2 = 1
            if i in stroka3:
                s3 = 1
            if i in stroka4:
                s4 = 1
        if s1 == 1 and s2 == 1 or s3 == 1 and s4 == 1:
            for i in bucvy:
                if i in password.lower():
                    q = 1
                    break
            if q == 0:
                for i in password:
                    if i.isalpha():
                        q1 = 1
                    if i.isdigit():
                        q2 = 1
                if q1 == 1 and q2 == 1:
                    try:
                        return 'ok'
                    except Exception:
                        pass
                if q1 == 0 or q2 == 0:
                    try:
                        raise Exception('SequenceError')
                    except Exception:
                        pass
            if q == 1:
                try:
                    raise Exception('DigitError')
                except Exception:
                    pass
        if s1 == 0 or s2 == 0 and s3 == 0 or s4 == 0:
            try:
                raise Exception('LetterError')
            except Exception:
                pass
    if len(password) <= 8:
        try:
            raise Exception('LengthError')
        except Exception:
            pass

try:
    print(check_password("G7FgTU0bwТuio"))
except Exception as error:
    print(error.__class__.__name__)