import re
import os
from shutil import copyfile

# Change these as appropriate
src = '/Volumes/Kindle/documents/My Clippings.txt'
dst = '/Users/User/clippings.txt'

copyfile(src, dst)

# The clippings file
filename = "clippings.txt"
# Output directory
dirname = "kindle_clippings"

# Each clipping always consists of 5 lines:
# - title line
# - clipping info/metadata
# - a blank line
# - clipping text
# - a divider made up of equals signs

# Check the file exists
if not os.path.isfile(filename):
    print("ERROR: cannot find " + filename)
    print("Please make sure it is in the same folder as this script.")
    raise IOError


def remove_chars(s):
    """
    Remove special characters from the string
    :param s: input string
    """
    # Replace colons with a hyphen so "A: B" becomes "A - B"
    s = re.sub(' *: *', ' - ', s)
    # Remove question marks or ampersands
    s = s.replace('?', '').replace('&', 'and')
    # Replace ( ) with a hyphen so "this (text)" becomes "this - text"
    s = re.sub(r'\((.+?)\)', r'- \1', s)
    # Delete filename chars tht are not alphanumeric or ; , _ -
    s = re.sub(r'[^a-zA-Z\d\s;,_-]+', '', s)
    # Trim off anything that isn't a word at the start & end
    s = re.sub(r'^\W+|\W+$', '', s)
    return s


# Create the output directory if it doesn't exist
if not os.path.exists(dirname):
    os.makedirs(dirname)

# The set of titles already processed
output_files = set()
title = ''

# Open clippings textfile and read data in lines
f = open(filename)

for highlight in f.read().split("=========="):
    lines = highlight.split('\n')[1:]

    # Don't try to write if we have no body
    if len(lines) < 3 or lines[3] == '':
        continue

    # Set title and trim hex
    title = lines[0]
    if title[0] == '\ufeff':
        title = title[1:]

    # Remove characters and create path
    outfile_name = remove_chars(title) + '.txt'
    path = dirname + '/' + outfile_name

    # If we haven't seen title yet, set mode to write. Else, set to append.
    if outfile_name not in (list(output_files) + os.listdir(dirname)):
        mode = 'w'
        output_files.add(outfile_name)
    else:
        # If the title exists, read it as text so that we won't append duplicates
        mode = 'a'
        with open(path, 'r') as textfile:
            current_text = textfile.read()

    clipping_text = lines[3]

    with open(path, mode) as outfile:
        # Write out the the clippings text if it's not already there
        if clipping_text not in current_text:
            outfile.write("%s\n\n...\n\n" % clipping_text)

f.close()

print("\nExported titles:\n")
for i in output_files:
    print("%s" % i)
