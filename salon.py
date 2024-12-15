import datetime

class User:
    def __init__(self, username, password, role, history=None):
        self.username = username
        self.password = password
        self.role = role
        self.history = history if history else []

class Service:
    def __init__(self, name, price, duration, added_at=None):
        self.name = name
        self.price = price
        self.duration = duration
        self.added_at = added_at if added_at else datetime.date.today()

    def __str__(self):
        return f"{self.name} - Цена: {self.price} руб., Длительность: {self.duration} мин., Добавлено: {self.added_at}"

class Cart:
    def __init__(self):
        self.items = []

    def add_item(self, service):
        self.items.append(service)

    def get_total(self):
        return sum(item.price for item in self.items)

    def clear(self):
        self.items = []

    def __str__(self):
      if not self.items: return "Корзина пуста"
      return "\n".join(str(item) for item in self.items)

class Client:
    def __init__(self, name, services, total_cost, visit_date, appointment_time):
        self.name = name
        self.services = services
        self.total_cost = total_cost
        self.visit_date = visit_date
        self.appointment_time = appointment_time

    def __str__(self):
        return f"Имя: {self.name}, Услуги: {', '.join(self.services)}, Стоимость: {self.total_cost} руб., Дата визита: {self.visit_date}, Время записи: {self.appointment_time}"


def authenticate(username, password, users):
    for user in users:
        if user.username == username and user.password == password:
            return user
    return None

def add_service(services, name, price, duration):
    services.append(Service(name, price, duration))
    print("Услуга добавлена.")

def delete_service(services, name):
    for i, service in enumerate(services):
        if service.name == name:
            del services[i]
            print(f"Услуга '{name}' удалена.")
            return
    print(f"Услуга '{name}' не найдена.")

def edit_service(services, name, new_price=None, new_duration=None):
    for service in services:
        if service.name == name:
            if new_price: service.price = new_price
            if new_duration: service.duration = new_duration
            print(f"Услуга '{name}' изменена.")
            return
    print(f"Услуга '{name}' не найдена.")


def display_services(services):
    if not services:
        print("Список услуг пуст.")
        return
    print("\nДоступные услуги:")
    for service in services:
        print(service)

def sort_services(services, key, reverse=False):
    return sorted(services, key=key, reverse=reverse)

def filter_services(services, key, value):
    return list(filter(lambda service: key(service) == value, services))

def add_to_cart(cart, service):
    cart.add_item(service)
    print(f"Услуга '{service.name}' добавлена в корзину.")

def checkout(user, cart, services, clients):
    if not cart.items:
        print("Корзина пуста.")
        return
    total_cost = cart.get_total()
    name = input("Введите ваше имя: ")
    visit_date = input("Введите дату визита (YYYY-MM-DD): ")
    appointment_time = input("Введите желаемое время (HH:MM): ")
    client = Client(name, [item.name for item in cart.items], total_cost, visit_date, appointment_time)
    clients.append(client)
    cart.clear()
    print(f"Заказ оформлен успешно! Общая стоимость: {total_cost} руб.")

def display_clients(clients):
    if not clients:
        print("Список клиентов пуст.")
        return
    print("\nСписок клиентов:")
    for client in clients:
        print(client)


def user_menu(user, services, clients):
    cart = Cart()
    while True:
        print("\nМеню пользователя:")
        print("1. Просмотреть услуги")
        print("2. Запись на услугу")
        print("3. Просмотреть корзину")
        print("4. Оформить заказ")
        print("5. Выйти")

        choice = input("Выберите действие: ")
        try:
            choice = int(choice)
            if choice == 1:
                display_services(services)
            elif choice == 2:
                display_services(services)
                service_num = int(input("Выберите номер услуги: ")) - 1
                if 0 <= service_num < len(services):
                    add_to_cart(cart, services[service_num])
            elif choice == 3:
                print(cart)
                print(f"Общая стоимость: {cart.get_total()} руб.")
            elif choice == 4:
                checkout(user, cart, services, clients)
            elif choice == 5:
                break
            else:
                print("Неверный выбор.")
        except ValueError:
            print("Неверный ввод.")


def admin_menu(user, services, clients):
    while True:
        print("\nМеню администратора:")
        print("1. Просмотреть услуги")
        print("2. Добавить услугу")
        print("3. Удалить услугу")
        print("4. Редактировать услугу")
        print("5. Фильтровать услуги")
        print("6. Сортировать услуги")
        print("7. Просмотреть список клиентов")
        print("8. Выйти")

        choice = input("Выберите действие: ")
        try:
            choice = int(choice)
            if choice == 1:
                display_services(services)
            elif choice == 2:
                name = input("Название услуги: ")
                price = int(input("Цена: "))
                duration = int(input("Длительность: "))
                add_service(services, name, price, duration)
            elif choice == 3:
                name = input("Название услуги для удаления: ")
                delete_service(services, name)
            elif choice == 4:
                name = input("Название услуги для редактирования: ")
                new_price = input("Новая цена (пустое поле для пропуска): ")
                new_duration = input("Новая длительность (пустое поле для пропуска): ")
                edit_service(services, name, int(new_price) if new_price else None, int(new_duration) if new_duration else None)

            elif choice == 5:
                filter_key = input("Фильтр по (price, duration, name, added_at): ")
                filter_value = input("Значение фильтра: ")
                try:
                  if filter_key == "price" or filter_key == "duration":
                    filtered = filter_services(services, lambda s: getattr(s, filter_key), int(filter_value))
                  elif filter_key == "name" or filter_key == "added_at":
                    filtered = filter_services(services, lambda s: getattr(s, filter_key), filter_value)
                  else: raise ValueError
                  display_services(filtered)
                except ValueError: print("Неверный ключ или значение для фильтрации")

            elif choice == 6:
                sort_key = input("Сортировать по (price, duration, name, added_at): ")
                reverse = input("Обратный порядок (yes/no): ").lower() == "yes"
                try:
                  if sort_key == "price" or sort_key == "duration":
                    sorted_services = sort_services(services, lambda s: getattr(s, sort_key), reverse)
                  elif sort_key == "name" or sort_key == "added_at":
                    sorted_services = sort_services(services, lambda s: getattr(s, sort_key), reverse)
                  else: raise ValueError
                  display_services(sorted_services)
                except ValueError: print("Неверный ключ для сортировки")

            elif choice == 7:
                display_clients(clients)
            elif choice == 8:
                break
            else:
                print("Неверный выбор.")
        except ValueError:
            print("Неверный ввод.")



def main():
    users = [
        User('user', 'user', 'user'),
        User('admin', 'admin', 'admin'),
    ]
    services = [
    {'name': 'Стрижка мужская', 'price': 500, 'duration': 25},
    {'name': 'Стрижка женская каре', 'price': 800, 'duration': 45},
    {'name': 'Стрижка женская модельная', 'price': 1500, 'duration': 60},
    {'name': 'Окрашивание Эир-тач', 'price': 2000, 'duration': 60},
    {'name': 'Маникюр', 'price': 1000, 'duration': 45},
    {'name': 'Маникюр с покрытием гель лак', 'price': 3500, 'duration': 60},
    {'name': 'Педикюр', 'price': 1200, 'duration': 60},
    {'name': 'Педикюр с покрытием гель лак', 'price': 2500, 'duration': 60},
    ]
    clients = []

    while True:
        username = input("Логин: ")
        password = input("Пароль: ")
        user = authenticate(username, password, users)
        if user:
            if user.role == 'admin':
                admin_menu(user, services, clients)
            elif user.role == 'user':
                user_menu(user, services, clients)
            print("Вы вышли из системы.")
        else:
            print("Неверный логин или пароль.")

if __name__ == "__main__":
    main()
