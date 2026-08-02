# https://docs.python.org/3/tutorial/inputoutput.html#tut-files -- Main info
# https://docs.python.org/3/library/functions.html#open -- Extras (Line 21+)

# 'with' is basically a 'try', 'finally' clause, except in this case it closes the file afterwards.
# 'as' is used to set a value to a variable whilst a special action is being preformed;
# This is done because you cannot define a variable to something that is being affected by a 'with' clause;
# Don't even try.
with open('workfile.txt', "r", encoding="utf-8") as file: # "utf-8" is the standard for .txt files*.
    message = file.read()
    print(message)
# Automatically closes the file. Don't ask me why exactly it does that SPECIFICALLY,
# I was too lazy to read more of the python doccumentation.

# I don't really know what an encoding IS, but I guess maybe it's some sort of codec?
# Now that I think of it, they both have "cod" in them so maybe..

# Extra Methods
#file.close() # closes the file manually
file.closed # returns a boolean expression

import locale # Don't ask me what this library is, it just is there in the second link
locale.getencoding() # Find your device's locale encoding (usually utf-8)

# Useless information below:
# The 'newline' keyword argument is by default set to None. He's how it works:
# 1. Python converts anything that could be a newline style to '\n'
# 2. You write to the file using '\n'
# 3. Python converts it back based on your operating system

# However if it is set to "", then it will display ALL line endings, but not change them,
# and any  line ending you write will be unaffected.

# If it is say, "\r\n" (Windows default), it will only display that line ending,
# and when you write any line ending it will convert it back to the one specified.