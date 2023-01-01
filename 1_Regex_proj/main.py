import re

def extractPhoneNumber(string):
    # Creating a phone number regex objects
    phoneRegexSimple = re.compile(r'(\+7|8)(\d{3})(\d{3})(\d{2})(\d{2})')
    phoneRegexComplex = re.compile(r'(\+7|8)(\s?\(\d{3}\)\s?)(\d{3})-(\d{2})-(\d{2})')
    
    # Storing found number in mo_* Match objects
    mo_simple = phoneRegexSimple.search(string)
    mo_complex = phoneRegexComplex.search(string)

    # If no phone numbers are found then return None
    if mo_simple:
        return mo_simple.group()
    elif mo_complex:
        return mo_complex.group()
    else:
        return None


if __name__ == '__main__':
    print(extractPhoneNumber('Epic my number is 89992286969 yeeah'))
    print(extractPhoneNumber('Epic my number is +7 (999) 228-69-69 yeeah'))