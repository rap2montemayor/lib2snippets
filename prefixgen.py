import os

prefixes = dict()
for root, dirs, files in os.walk('.'):
	for file in files:
		if ".cpp" not in file: continue
		prefixes[file[:-4]] = ""

if "prefixes" in os.listdir():
	with open("prefixes", encoding='utf-8') as prefixfile:
		for line in prefixfile:
			if line == "\n" or line[0] == "#" or ":" not in line:
				continue
			snippet, prefix = line.strip("\n").split(':')
			snippet, prefix = snippet.strip(), prefix.strip()
			if snippet in prefixes:
				prefixes[snippet] = prefix

with open("prefixes", mode='w', encoding='utf-8') as prefixfile:
	header = """# Syntax:
# {Filename name (without extension)} : {prefix}
# Prefix names must be supplied manually
# Lines starting with # are ignored
# Take note that regenerating this file will remove 
# all comments except for this header\n"""
	print(header, file=prefixfile)
	for snippet in sorted(prefixes):
		print(snippet, prefixes[snippet], sep=" : ", file=prefixfile)