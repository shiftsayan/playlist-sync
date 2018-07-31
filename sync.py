#########################
# Imports
#########################

from ams import ams
import refresh

#########################
# Scripts
#########################

f = open("playlists.txt", 'r')

for line in f.readlines():
    ams(line.strip())
