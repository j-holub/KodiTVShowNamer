#!/usr/bin/env python

# Jan Holub, 2014
# Jan-Holub@gmx.net



# This script is designed to rename a bunch of files belonging to the same TVSeries to a format, so that
# XBMC/Kodi finds the matching information.



# Basic usage:
# TVSeriesRename <directory> <seriesname> [optional parameters]



# Determine the episode number:
# If you do not specify an own regular expression the script will look for the pattern epXX, X elemnt {0..9}
# You can however specify your own regEx with -r <regex> to match any pattern you will come accross



# optional arguments:

# -r / --regex:
# This will specify your own regular Expression to determine the episode number

# -y / --year:
# This will add the year to the filename

# -s / --season
# This will add the season number to the filename

# -su / --subitle
# This will look for subtitle files in the same directory (it can find srt, ass, sub, idx) and rename them adding
# the language specified with these argument. For example SeriesA.ep01.mkv and SeriesA.ep01.en.srt.
# If this argument is not given, it will still rename the subtitle file but not add a language specifiction


# Example:
# TVSeriesRename . SeriesA -y 2014 -r " - [0-2][0-9]" -s 01 - su en
# This will rename the files in the current directory to SeriesA.s01.eXX.mkv and the Subitle files to
# SeriesA.s01.eXX.en.srt if they were mkv and srt files.
# The regex will look for the pattern " - XY" with X in {0, 1, 2} and Y in {0..9}



import sys, os, re, argparse

#setup subitle endinglist
subEndings = ['srt', 'ass', 'sub', 'idx']

#Create Parser Object
parser = argparse.ArgumentParser()
parser.add_argument('directory', help="The directory in which the files are located")
parser.add_argument('tv_show_name', help="Name of the TV Show")
parser.add_argument('-r',  '--regex', type=str, help="Regular Expression to detect the episodenumber in the files")
parser.add_argument('-y',  '--year', type=str, help="Year the TV Show was released")
parser.add_argument('-s',  '--season', type=str, help="Season Number")
parser.add_argument('-su', '--subtitle', type=str, help="Subtitle Language Suffix")
arguments = parser.parse_args()

#Get the Path
path = os.path.abspath(arguments.directory)
#Check if the given path exists
if (not os.path.exists(path)):
	print "Error: No such directory '%s'" % path
	sys.exit()


#TV Show Name
print "TVShowname: %s" % arguments.tv_show_name
#Year
if(arguments.year):
	print "Year: %s" % arguments.year
#Season
if(arguments.season):
	print "Season: %s" % arguments.season



#Check if a regex was specified
if arguments.regex:
	regex = re.compile(arguments.regex)
	print "Regular expression was specified as '%s'" % arguments.regex
#Falling back to standart Regex
else:
	regex = re.compile("ep[0-9][0-9]", re.IGNORECASE)
	print "No Regular Expression was specified. Falling back to standart 'ep[0-9][0-9]' (case-insensitive)"




#Count modified files
count = 0
#Count conflicts
conflicts = 0

#Get the list of all files in the given Directory
list_of_files = [File for File in os.listdir(path) if os.path.isfile("%s/%s" % (path, File))]



#Iterate through every file and process is
for episode in list_of_files:


	#Get the ending of the file
	file_ending = episode[str.rfind(episode, '.')+1:]

	#Check for a match with the regular expression
	match = regex.search(episode)

	#if there was a match apply the changes
	if(match):
		episode_number = filter(str.isdigit, episode[match.start():match.end()])

		#if there was no number found in the string, better do not touch this file
		if not episode_number:
			continue

		#build the newname
		new_name = arguments.tv_show_name

		#XBMC/Kodi scrapers wants only e if the season is inlcuded. SeriesA.s1.e2.mkv
		#However if no season is specified epXX works

		#Add Season if specified
		if(arguments.season):
			new_name += ".s" + arguments.season
			#Add SeasonType Episode Number
			new_name += ".e" + episode_number
		#if no Season was specified, add it with "ep"
		else:
			#Add EpisodeNumber
			new_name += ".ep" + episode_number

		#Add Year if specified
		if(arguments.year):
			new_name += "." + arguments.year

		#check if it was a subtitle File if argument was given
		if(arguments.subtitle and file_ending in subEndings):
			new_name += "." + arguments.subtitle
			
		#Add File ending
		new_name += "." + file_ending

		#check for conflict
		if(os.path.isfile("%s/%s" % (path, new_name))):
			print "Conflict when trying to rename '%s' to '%s': File already exists" % (episode, new_name)
			conflicts+= 1
		else:
			#Rename the file
			os.rename("%s/%s" % (path, episode), "%s/%s" % (path, new_name))

			#Increment the counter
			count += 1
	
			print "Renamed '%s' to '%s'" % (episode, new_name)

	else:
		print "No Match found for '%s'" % episode


print "Renamed %d files" % count
print "%d conflicts" % conflicts
print "Finished"