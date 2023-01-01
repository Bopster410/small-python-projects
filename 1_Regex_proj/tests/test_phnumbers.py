import phnumbers

def test_correct_numbers_simple():
    assert phnumbers.extractPhoneNumber('Epic my number is 89992286969 yeeah') == '89992286969'
    assert phnumbers.extractPhoneNumber('Epic my number is +79992286969 yeeah') == '+79992286969'

def test_correct_numbers_complex():
    assert phnumbers.extractPhoneNumber('Epic my number is 8(999)228-69-69 yeeah') == '8(999)228-69-69'
    assert phnumbers.extractPhoneNumber('Epic my number is 8 (999) 228-69-69 yeeah') == '8 (999) 228-69-69'
    assert phnumbers.extractPhoneNumber('Epic my number is +7(999)228-69-69 yeeah') == '+7(999)228-69-69'
    assert phnumbers.extractPhoneNumber('Epic my number is +7 (999) 228-69-69 yeeah') == '+7 (999) 228-69-69'

def test_incorrect_numbers_simple():
    assert phnumbers.extractPhoneNumber('My number today is +7999286969') == None
    assert phnumbers.extractPhoneNumber('My number today is +8999286969') == None

def test_all_numbers():
    assert phnumbers.extractPhoneNumber('Epic my number is +7 (999) 228-69-69 yeeah and also 89993337766 or even +7 (12) 342-11-33', all=True) == [('8', '999', '333', '77', '66'), ('+7', '(999)', '228', '69', '69')]