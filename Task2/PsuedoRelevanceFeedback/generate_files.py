import os


def create_project_dir(directory):
	if not os.path.exists(directory):
		# print('Creating the directory' + directory)
		os.makedirs(directory)


def create_file(filename):
	if not os.path.isfile(filename):
		with open(filename, 'w') as f:
			f.write('')
			f.close()


def append_to_file(filename, data):
	with open(file=filename, mode="a", encoding="utf-8", errors="UnicodeDecodeError") as f:
		f.write(data)
		f.close()


# with open(filename,'a') as f:
# f.write(str(data.encode('UTF-8')))

def delete_file(filename):
	if os.path.isfile(filename):
		os.remove(filename)


def delete_directory(directory_name):
	if os.path.exists(directory_name):
		for entry in os.scandir(directory_name):
			if os.path.isfile(entry):
				delete_file(entry)
			else:
				delete_directory(entry)
		os.rmdir(directory_name)


