from django.db import models


class Customer(models.Model):
    customer_full_name = models.CharField('Полное имя',max_length=50)
    contact_information = models.CharField('Контактная информация',max_length=25)
    customer_login = models.CharField('Логин',max_length=25)
    customer_password = models.IntegerField('Пароль')

    def __str__(self):
        return self.customer_full_name
    

class Application(models.Model):
    date_of_creation = models.DateField('Дата создания')
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    destination_address = models.CharField('Адрес назначения', max_length=50)
    type_tc_id = models.IntegerField()
    total_cost = models.IntegerField('Суммарная стоимость')
    date_of_accomplishment = models.DateField('Дата выполнения')
    administrator_id = models.IntegerField()
    application_status = models.CharField('Статус')

    def __str__(self):
        return f'Заявка:{self.application_status}'
    
    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

class Type_TC(models.Model):
    name_type_tc = models.CharField('Название ТС',max_length=50)
    type_tc_cost = models.IntegerField('Стоимость ТС')

    def _str_(self)-> str:
        return self.name_type_tc