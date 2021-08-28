LINE_BREAK = "="*50

def read_file(filename: str):
    with open(filename, 'r', encoding='utf-8-sig') as f:
        return f.read()

def write_to_file(filename: str, content: str, mode='w'):
    with open(filename, mode, encoding='utf-8-sig') as f:
        f.write(content)
