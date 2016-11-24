INDENT = "    "
NEW_LINE_INDENT = "\n%s" % INDENT

def create_class(name):
    text_file = open("classes.py", "w")
    text_file.write("class %s:%spass" % (name, NEW_LINE_INDENT))
    text_file.close()
