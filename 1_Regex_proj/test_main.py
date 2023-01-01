import main

def test_correct_numbers_simple():
    assert main.extractPhoneNumber('Epic my number is 89992286969 yeeah') == '89992286969'
    assert main.extractPhoneNumber('Epic my number is +79992286969 yeeah') == '+79992286969'

def test_correct_numbers_complex():
    assert main.extractPhoneNumber('Epic my number is 8(999)228-69-69 yeeah') == '8(999)228-69-69'
    assert main.extractPhoneNumber('Epic my number is 8 (999) 228-69-69 yeeah') == '8 (999) 228-69-69'
    assert main.extractPhoneNumber('Epic my number is +7(999)228-69-69 yeeah') == '+7(999)228-69-69'
    assert main.extractPhoneNumber('Epic my number is +7 (999) 228-69-69 yeeah') == '+7 (999) 228-69-69'

def test_incorrect_numbers_simple():
    assert main.extractPhoneNumber('My number today is +7999286969') == None
    assert main.extractPhoneNumber('My number today is +8999286969') == None
