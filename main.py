import cmd
import json
from collections import UserDict
from datetime import datetime


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        self.phone_valid = value

    @property
    def phone_valid(self):
        return self.value

    @phone_valid.setter
    def phone_valid(self, phone):
        if len(phone) != 10 or not phone.isdigit():
            raise ValueError('Invalid phone number.')
        self.value = phone


class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)
        self.birthday_valid = value

    @property
    def birthday_valid(self):
        return self.value

    @birthday_valid.setter
    def birthday_valid(self, birthday):
        try:
            if int(birthday[-4:]) < 1930:
                raise ValueError
            else:
                self.value = birthday
        except ValueError:
            print('Birthday year can not be less than 1930.')


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = birthday

    def add_birthday(self, birthday):
        self.birthday = birthday

    def days_to_birthday(self):
        if not self.birthday:
            return 'No birthday details.'
        if isinstance(self.birthday, Birthday):
            birthday_datetime = datetime.strptime(self.birthday.value, '%d %B %Y').date()
        else:
            birthday_datetime = datetime.strptime(self.birthday, '%d %B %Y').date()

        current_year_birthday = datetime(datetime.now().year, birthday_datetime.month, birthday_datetime.day).date()
        if current_year_birthday.month >= datetime.now().month:
            difference = current_year_birthday - datetime.now().date()
            return f'Days left until birthday: {difference.days}'
        else:
            difference = datetime(current_year_birthday.year + 1, current_year_birthday.month, current_year_birthday.day).date() - datetime.now().date()
            return f'Days left until birthday: {difference.days}'

    def add_phone(self, phone):
        try:
            p = Phone(phone)
            if p.phone_valid:
                self.phones.append(p)
        except ValueError as e:
            print(e)

    def edit_phone(self, old_phone, new_phone):
        phone_found = False
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                phone_found = True
                break
        if not phone_found:
            raise ValueError('Phone was not found.')

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)

    def __str__(self):
        if not self.birthday:
            return 'Contact name: {:<10} Phones: {:<25} Birthday: {:<25} {}'.format(self.name.value, '; '.join(p.value for p in self.phones), self.days_to_birthday(), self.days_to_birthday())
        else:
            return 'Contact name: {:<10} Phones: {:<25} Birthday: {:<25} {}'.format(self.name.value, '; '.join(p.value for p in self.phones), str(self.birthday), self.days_to_birthday())


class AddressBook(UserDict):

    def add_record(self, contact):
        self.data.update({contact.name.value: contact})

    def find(self, name):
        if name in self.data:
            return self.data[name]
        else:
            print('Phone was not found.')

    def delete(self, name):
        try:
            if name in self.data:
                self.data.pop(name)
            else:
                raise KeyError
        except KeyError:
            print(f'"{name}" is not in the address book.')

    def iterator(self, n):
        if n > len(book.data):
            print(f'There are {len(book.data)} records in Address Book.')
        counter = 0
        result = ''
        for _, record in self.data.items():
            result += f'{record}\n'
            counter += 1
            if counter == n:
                yield result
                result = ''

    def search(self, query):
        results = []
        for _, record in self.data.items():
            if query.lower() in record.name.value.lower() or any(query in phone.value for phone in record.phones):
                results.append(record)
        return results

    def dump(self, file):
        self.file = file
        with open(self.file, 'w') as file:
            for _, record in self.data.items():
                record_dict = {
                    'Contact name': record.name.value,
                    'Phones': [p.value for p in record.phones],
                    'Birthday': record.birthday.value if record.birthday else 'No birthday details.'}
                json.dump(record_dict, file)
                file.write('\n')

    def load(self, file):
        self.file = file
        with open(self.file, 'r') as file:
            for line in file:
                line_reader = json.loads(line)
                print(line_reader)


book = AddressBook()

search_by_name = book.search('')
for match in search_by_name:
    print(match)


search_by_phone = book.search('')
for match in search_by_phone:
    print(match)