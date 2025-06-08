import pandas as pd
import os


def fptsplitdata(file_path, file_ext, out_folder, lines_to_split):
    input_file = file_path + file_ext
    output_file = os.path.join(out_folder, "dev" + file_ext)
    f = open(output_file, 'w', encoding='utf-8')
    count = 0
    with open(input_file, encoding='utf-8') as f1:
        for line in f1:
            count += 1
            if count < lines_to_split:
                f.write(line)
            elif count == lines_to_split:
                f.write(line)
                f.close()
                output_file = os.path.join(out_folder, "test" + file_ext)
                f = open(output_file, 'w', encoding='utf-8')
            elif count < lines_to_split*2:
                f.write(line)
            elif count == lines_to_split*2:
                f.write(line)
                f.close()
                output_file = os.path.join(out_folder, "train" + file_ext)
                f = open(output_file, 'w', encoding='utf-8')
            else:
                f.write(line)
    f.close()
def split_data(folder, input_prefix_file_name, number_of_line):

    ext = ".vi"
    fptsplitdata(os.path.join(folder,input_prefix_file_name), ext, folder, number_of_line)

    ext = ".en"
    fptsplitdata(os.path.join(folder,input_prefix_file_name), ext, folder, number_of_line)
