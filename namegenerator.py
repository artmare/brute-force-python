import datetime

def generate_usernames(first_name, last_name):
	"""Генерирует возможные варианты имени пользователя на основе имени и фамилии"""
	first_name = first_name.lower()
	last_name = last_name.lower()
	usernames = [
		first_name,
		last_name,
		f"{first_name}{last_name}",
		f"{last_name}{first_name}",
		f"{first_name}.{last_name}",
		f"{last_name}.{first_name}",
		f"{first_name}_{last_name}",
		f"{last_name}_{first_name}",
		f"{first_name[0]}{last_name}",
		f"{first_name}{last_name[0]}",
		f"{first_name[0]}.{last_name}",
		f"{first_name}.{last_name[0]}",
		f"{first_name[0]}_{last_name}",
		f"{first_name}_{last_name[0]}"
	]
	# Добавляем варианты с годами (например, для дня рождения)
	current_year = datetime.datetime.now().year
	years = list(range(current_year - 70, current_year + 1))
	years_short = [str(year)[-2:] for year in years]
	year_variations = []
	for username in usernames:
		for year in years_short[-10:]:  # Последние 10 лет в коротком формате
			year_variations.append(f"{username}{year}")
	usernames.extend(year_variations)
	return usernames

print(generate_usernames("admin", "Karnaukhov"))