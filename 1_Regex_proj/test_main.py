import main

def test_correct_numbers():
    assert main.extractPhoneNumber('Epic my number is 89992286969 yeeah') == '89992286969'
    assert main.extractPhoneNumber('Epic my number is +79992286969 yeeah') == '+79992286969'

def test_incorrect_numbers():
    assert main.extractPhoneNumber('My number today is +7999286969') == None
    assert main.extractPhoneNumber('My number today is +8999286969') == None
