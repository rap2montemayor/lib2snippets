# Yes it's fugly
import os

def print_snippet(directory, filename, prefix, out):
	print(f"\t\"{ filename.split('.')[0] }\": {{", file=out)
	print(f"\t\t\"prefix\": \"{prefix}\",", file=out)
	print("\t\t\"body\": [", file=out)
	file = os.path.join(directory, filename + ".cpp")
	with open(file, encoding='utf-8') as snippet:
		for line in snippet:
			line = line.replace("    ", "\\t").strip("\n")
			print(f"\t\t\t\"{line}\",", file=out)
	print("\t\t]", file=out)
	print("\t},\n", file=out)


def skipline(line):
	return line == "\n" or line[0] == "#"


def splitline(line):
	line = line.strip("\n")
	snippet, prefix = line.strip("\n").split(':')
	snippet, prefix = snippet.strip(), prefix.strip()
	return snippet, prefix


def iscppfile(file):
	return ".cpp" in file


def hascppfile(directory):
	for file in os.listdir(directory):
		if ".cpp" in file:
			return True
	return False


def getprefixes():
	prefixes = dict()
	with open("prefixes", encoding='utf-8') as prefixfile:
		for line in prefixfile:
			if skipline(line): continue
			snippet, prefix = splitline(line)
			prefixes[snippet] = prefix
	return prefixes


def goodprefixfile(snippets):
	with open("prefixes", encoding='utf-8') as prefixfile:
		for idx, line in enumerate(prefixfile, start=1):
			if skipline(line): continue
			if ":" not in line:
				print(f"\":\" expected in line {idx}")
				return False

			snippet, prefix = splitline(line)
			if snippet in snippets:
				print(f"Line {idx} is a duplicate entry.")
				return False
			if prefix == "":
				print(f"Line {idx} is blank.")
				return False

			snippets.add(snippet)
	return True


def hasmissingentry(snippets):
	for root, dirs, files in os.walk('.'):
		for file in files:
			if not iscppfile(file): continue
			if file[:-4] not in snippets:
				print(f"{file[:-4]} is missing")
				return True


def checks():
	if "prefixes" not in os.listdir():
		print("prefixes file missing")
		return False
	snippets = set()
	if not goodprefixfile(snippets) or hasmissingentry(snippets):
		return False
	return True

if __name__ == "__main__":
	if not checks():
		exit()

	prefix = getprefixes()
	with open("cpp.json", mode="w", encoding="utf-8") as out:
		print("{", file=out)
		for root, dirs, files in os.walk('.'):
			if not hascppfile(root): continue

			print(f"// {root.split(os.sep)[-1].upper()}", file=out)
			for file in files:
				if not iscppfile(file): continue
				filename = file[:-4]
				print_snippet(root, filename, prefix[filename], out)
		print("}", file=out)