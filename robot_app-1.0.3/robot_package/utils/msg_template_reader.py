def get_template_from_file(filename):
    with open(filename, 'r') as f:
        msg = f.read()
    return msg
