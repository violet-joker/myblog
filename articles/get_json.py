import os
import json

def get_dirs(path):
    dirs = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
    return dirs

def get_files(path):
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    return files

def get_data(path, name):
	data = {
		"label": name,
		"key": "null",
		"children": []
	}
	dirs = get_dirs(root + '/' + path)
	files = get_files(root + '/' + path)
	for file in files:
		key = path + '/' if path else ""
		item = {
			"label": file.rstrip('.md'),
			"key": key + file
		}
		data["children"].append(item)
	for d in dirs:
		data["children"].append(get_data(path + d, d))
	return data

root = os.getcwd()
data = get_data("", "≡")
json_data = json.dumps(data, ensure_ascii=False, indent=2)
with open('list.json', 'w', encoding='utf-8') as f:
	f.write(json_data)
