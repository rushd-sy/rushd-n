from typing import Iterator


def read_file(file_path: str) -> Iterator[str]:
    with open(file_path, 'r') as file:
        for line in file:
            yield line.strip()

if __name__ == "__main__":
    file_path = 'test.txt'
    gene = read_file(file_path)
    for line in gene:
        print(line)