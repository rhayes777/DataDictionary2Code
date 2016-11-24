def create_class(name):
    text_file = open("classes.py", "w")
    text_file.write("class %s:\n    pass" % name)
    text_file.close()
