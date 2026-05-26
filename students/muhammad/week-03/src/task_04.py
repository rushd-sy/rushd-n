def read_large_fild(file_path):
    for line in open(file_path):
        yield line
