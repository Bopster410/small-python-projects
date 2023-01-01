import re

def extractPhoneNumber(string):
    # Creating a phone number regex object
    phoneRegex = re.compile(r'(\+7|8)(\d{3})(\d{3})(\d{2})(\d{2})')
    
    # Storing found number in mo Match object
    mo = phoneRegex.search(string)

    # If no phone numbers are found then return None
    if mo:
        return mo.group()
    else:
        return None


if __name__ == '__main__':
    print(extractPhoneNumber('Epic my number is 89992286969 yeeah'))
    print(extractPhoneNumber('Epic my number is +79992286969 yeeah'))