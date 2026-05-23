def read_file(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            yield line.strip()

if __name__ == "__main__":
    file_path = 'test.txt'
    gene = read_file(file_path)
    while True:
        try:
            line = next(gene)
            print(line)
        except StopIteration:
            break