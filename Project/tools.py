def sanitize_roll_number(roll):
	"""Function to check if the entered string is a valid roll number.
	"""
	validYears = ['12', '13', '14', '15']
	validDeps = ["01", "02", "03", "04", "05", "06", "07", "08", "21", "22", "23"]
	if len(roll) == 9 and roll.isdigit():
		if roll[:2] in validYears:
			if roll[4:6] in validDeps:
				return True
	return False


def sanitize_phone_number(phone):
	"""Function to check if the entered string is a valid phone number.
	"""
	if len(phone) != 10 or not phone.isdigit():
		return False

	return True