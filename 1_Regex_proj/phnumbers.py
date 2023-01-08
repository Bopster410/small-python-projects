import re, pyperclip

def extract_phone_number(string, all=False):
    # Creating a phone number regex objects
    phone_regex_simple = re.compile(r'(\+7|8)(\d{3})(\d{3})(\d{2})(\d{2})')
    phone_regex_complex = re.compile(r'(\+7|8)\s?\((\d{3})\)\s?(\d{3})-(\d{2})-(\d{2})')
    
    # If user wants to find all phone numbers in the string
    if all:
        # Storing found number in tuples
        simple_phnumbers = phone_regex_simple.findall(string)
        complex_phnumbers = phone_regex_complex.findall(string)

        # If no phone numbers are found then return None
        if simple_phnumbers or complex_phnumbers:
            return simple_phnumbers + complex_phnumbers
        else:
            return None

    else:
        # Storing found number in mo_* Match objects
        mo_simple = phone_regex_simple.search(string)
        mo_complex = phone_regex_complex.search(string)

        # If no phone numbers are found then return None
        if mo_simple:
            return mo_simple.group()
        elif mo_complex:
            return mo_complex.group()
        else:
            return None

def censor_phone_number(string):
    # Creating a phone number regex objects
    phone_regex_simple = re.compile(r'(\+7|8)(\d{3})(\d{3})(\d{2})(\d{2})')
    phone_regex_complex = re.compile(r'(\+7|8)\s?\((\d{3})\)\s?(\d{3})-(\d{2})-(\d{2})')

    return phone_regex_complex.sub(r'\1 (***) ***-**-**', phone_regex_simple.sub(r'\1**********', string))

def phone_numbers_clipboard():
    # Find all phone numbers in the string from clipboard
    string = str(pyperclip.paste())
    phone_numbers = set('8' + ''.join(number[1:]) for number in extract_phone_number(string, all=True))
    pyperclip.copy('\n'.join(phone_numbers))

if __name__ == '__main__':
    print(extract_phone_number('Epic my number is +7 (999) 228-69-69 yeeah and 89992286969 also!'))
    phone_numbers_clipboard()