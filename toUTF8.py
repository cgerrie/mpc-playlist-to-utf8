# Charlie Gerrie July 2021

# NOTE Must be run on windows for now so it can get absolute paths right

import sys
import os

class PlaylistDirectory:
	files = []
	pwd = ""
	def __init__(self, directory):
		# (path, subdirectories, files)
		(self.pwd, _, self.files) = next(os.walk(directory)) # TODO WALK MIGHT NOT ACTUALLY RETURN A VALUE
		
		# convert to absolute paths
		for i in range(0, len(self.files)):
			#self.files[i] = pwd+os.path.sep+self.files[i]
			self.files[i] = self.pwd+"\\"+self.files[i]
		#print("TEST search_directory # of files: "+str(len(self.files)))
		
	def findSimilarFile(self, filename):
		max_similarity = 0
		most_similar = ""
		line_length = len(filename)
		# find most similar
		for file in self.files:
			# get length of shorter string
			min_length = min(line_length, len(file))
			# find number of shared characters
			shared_characters = 0
			for i in range(0, min_length):
				if filename[i] == file[i]:
					shared_characters += 1
			similarity = shared_characters
			# check if more similar
			if similarity > max_similarity:
				most_similar = file
				max_similarity = similarity
				#print("TEST FOUND MORE SIMILAR "+file+" "+str(similarity))
		#print("TEST FIND SIMILAR OUTPUT "+most_similar+" "+str(max_similarity))
		return most_similar

# __main__

# handle arguments

# arg 1 playlist file
# TODO IF NO ARGUMENTS READ PLAYLIST FROM STDIN

# arg 2 (OPTIONAL, NOT => ./) song directory
# TODO DOESN'T NEED TO BE EXPLICIT BECAUSE MPC WILL INCLUDE DIRECTORIES IN THE FILE
# TODO AT LEAST MAKE IT SUPPORT MULTIPLE DIRECTORIES

# arg 3 output file
# It's best not done through stdout, since cmd has problems with utf-8 anyway

try:
	playlist_file = sys.argv[1]
	search_directory_path = sys.argv[2]
	output_playlist_path = sys.argv[3]
except IndexError:
	print("Insufficient arguments. Usage: python toUTF8.py <input_file.mpcpl> <directory to search> <output_file.mpcpl>")
	exit

# list search directory
search_directory = PlaylistDirectory(search_directory_path)

# read playlist file
ascii_lines = []
with open(playlist_file) as input:
	for ascii_line in input:
		ascii_lines.append(ascii_line)

# check header
#print("TEST header read successfully: "+str(ascii_lines[0].strip() == "MPCPLAYLIST"))
# TODO HANDLE IF NO?!?

# fix lines
for i in range(1, len(ascii_lines)): # note starts at 1, since we skipped the header
	# parse line type
	line = ascii_lines[i]
	fields = line.split(",")

	if fields[1].strip() == "filename":
		ascii_lines[i] = fields[0]+",filename,"+search_directory.findSimilarFile(fields[2])+"\n"
	else:
		pass # skip "type" lines
	

# output
with open(output_playlist_path, "w", encoding="utf-8") as output:
	for i in range(0, len(ascii_lines)):
		print(ascii_lines[i], end="", file=output)

