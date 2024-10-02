from blood_bank.tests.faker import faker

def generate_national_id():
    return ''.join(faker.random_choices(elements=('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'), length=14))