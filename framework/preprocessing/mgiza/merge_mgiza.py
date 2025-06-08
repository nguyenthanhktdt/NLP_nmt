import os

def process_alignment(line):
    line = line.replace("\n", "")
    arr1 = line.split("})")
    align = ''
    index = 0
    for s in arr1:
        arr2 = s.split("({")
        if arr2[0].strip() == 'NULL' or arr2[0].strip() == '' or arr2[0].strip() == ' ' or len(arr2)==1:
            index = 0
        else:
            index += 1
            num_arr = arr2[1].strip().split(" ")
            for num in num_arr:
                align += str(index) + "-" + num + " "
    return align

def merge_giza(folder):
    number_part = 8 #number of file output from mgiza,
    file_name_pattern = "src_trg.dict.A3.final.part00%s"
    dict ={}

    for part in range(number_part):
        print(part)
        count = 0
        file_name = os.path.join(folder,  (file_name_pattern % str(part)))
        with open(file_name, 'r', encoding='utf-8') as f:
            for line in f:
                count += 1
                if count % 3 == 1:
                    start = line.find("(")
                    end = line.find(")")
                    index = int(line[start+1:end])
                if count % 3 == 0:
                    dict[index] = process_alignment(line)
                if count % 100000 == 0:
                    print(count)

    print("total:", count)

    output_file = os.path.join(folder, "data.align")
    f_out = open(output_file, 'a', encoding='utf-8')

    for key in sorted(dict.keys()):
        f_out.write(dict[key] + "\n")

    f_out.close()
    print("--DONE--")

