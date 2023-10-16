from collections import UserDict
from datetime import datetime as date
import pickle as pckl
import re


class Contact():
    def __init__(self, surname):
        self.surname = surname
        self.name = ''
        self.phones = []
        self.birthday = ''
        self.email = ''

    def add_name(self, name):
        if name:
            self.name = name

    def add_phone(self, phones):
        if phones:
            for phone in phones:
                self.phones.append(phone)

    def add_email(self, email):
        if email:
            self.email = email

    def add_birthday(self, birthday):
        if birthday:
            self.birthday = birthday    

    def update_surname(self, new_surname):
            self.surname = new_surname

    def update_name(self, new_name):
        if new_name:  
            self.name = new_name

    def update_phone(self, *_):
        pass
    
    def update_birthday(self, new_birthday):
        if new_birthday:
            self.birthday = new_birthday
    
    def update_email(self, new_email):
        if new_email:
            self.email = new_email

    def read_surname(self):
        pass

    def read_birthday(self):
        pass

    def read_email(self):
        pass

    def read_phones(self):
        pass

    def delete_phone(self, value: str):
        pass

    def __repr__(self) -> str:
        return "Surname: {:<10}  Name: {:<10}  Phone: {:<15}  Email: {:<15}  Birthday: {}".format(
            self.surname,
            self.name,
            ", ".join(phone for phone in self.phones),
            self.email,
            self.birthday,
        )
    #   --------------------------------Chek parameters----------------------------
       
    #Правильность ввода номера телефона
    @property
    def phone(self):
        return self._phone

    @phone.setter
    def phone(self, phone: str):
        san_phone = re.sub(r'[-)( ]', '', phone)
        if re.match('^\\+380\d{9}$', san_phone):
            self._phone = san_phone
        else:
            raise ValueError("Phone number is not valid")
    #-------email checking_____________________________________________
    #Правильность ввода электронной почты
    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email: str):
        if re.match('^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$', email):
            self._email = email 
        else:
            raise ValueError("Email is not valid")
        

    #-------birthday checking_____________________________________________
    #правильность ввода даты
    @property
    def birthday(self):
        return self._birthday

    @birthday.setter
    def birthday(self, date):
        if re.match('^\d{2}.\d{2}.\d{4}$', date): 
            self._birthday = date 
        else:
            raise ValueError("Birthday is not valid")
    

class AddressBook(UserDict):
        
    def add_contact(self, ui , contact: Contact):
            self.data.update({contact.surname:contact})
            ui.show_green_message('This command will guide you through creating new contact:\n')
            ui.show_message(f'Surname: {contact.surname}')
            contact.add_name(ui.user_input('Name [Enter to skip]: '))
            contact.add_phone(ui.user_input('Phones space-separate [Enter to skip]: ').split())
            contact.add_birthday(ui.user_input('Birthday [Enter to skip]: '))
            contact.add_email(ui.user_input('Email [Enter to skip]: '))
        

    def read_contact(self, name: str):
        pass


    def update_contact(self, ui, contact: Contact):
        ui.show_green_message('This command will guide you through updating contact:\n')
        new_surname = ui.user_input(f'Surname: {contact.surname} [Enter to skip]: ') 
        if new_surname in self.data:
            ui.show_red_message(f'{new_surname} already exists ')
            return
        elif new_surname:
            self.data[new_surname] = contact
            del self.data[contact.surname]
            contact.update_surname(new_surname)      
        contact.update_name(ui.user_input(f'Name: {contact.name} [Enter to skip]: '))
        contact.update_phone(ui.user_input(f'Phones {contact.phones} [Enter to skip]: ').split())
        contact.update_birthday(ui.user_input(f'Birthday: {contact.birthday} [Enter to skip]: '))
        contact.update_email(ui.user_input(f'Email: {contact.email} [Enter to skip]: '))


    def delete_contact(self, name):
        if name in self.data:
            del self.data[name]


    def show_contacts(self):
        pass
    
    def log(self, action):
        time = date.strftime(date.now(), '%H:%M:%S')
        msg = f'[{time} {action}]'
        with open("logs.txt", "a") as file:
            file.write(f'{msg}\n')

    def save(self, file_name):
        with open(file_name + ".bin", "wb") as file:
            pckl.dump(self.data, file)
        self.log(f'AdressBook saved')
    
    def load(self, file_name):
        try:
            with open(file_name + ".bin", "rb") as file:
                self.data = pckl.load(file)
        except FileNotFoundError:
            ...
        self.log(f'AdressBook loaded')
        return self.data





            
      
