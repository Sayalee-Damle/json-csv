import csv
import difflib
from json_csv_compare.log_factory import logger

def compare_csv_files(file1_path, file2_path):
    with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
        csv_reader1 = csv.reader(file1)
        csv_reader2 = csv.reader(file2)

        lines1 = list(csv_reader1)
        lines2 = list(csv_reader2)
        return compare_lines(lines1, lines2)

def compare_lines(lines1, lines2):
    differ = difflib.Differ()
    missing_lines = []
    changed_lines = []
    new_lines = []

    f = True
    
    l = 1
    #while f == True:
        
    diff = list(differ.compare(lines1, lines2))
    print(diff)
    #if l == max(len(lines1)-1, len(lines2)-1):
        #f = False
    
    line_num = 0
    for line in diff:
        line_num += 1
        if line.startswith('  '):
            continue
        elif line.startswith('- '):
            missing_lines.append(line_num)
        elif line.startswith('+ '):
            new_lines.append(line_num)
        elif line.startswith('? '):
            changed_lines.append(line_num)

    
    return missing_lines,new_lines,changed_lines

def display(lines1, lines2, missing_lines, changed_lines, new_lines):
    missing = []
    new = []
    changed = []
    print("Missing Lines:")
    for line_num in missing_lines:
        missing.append(f"Line {line_num} from File 1: {','.join(lines1[line_num - 1])}")
        logger.info(missing)

    print("\nChanged Lines:")
    for line_num in changed_lines:
        changed.append([f"Line {line_num} from File 1: {','.join(lines1[line_num - 1])}", f"Line {line_num} from File 2: {','.join(lines2[line_num - 1])}"])
        logger.info(changed)

    print("\nNew Lines:")
    for line_num in new_lines:
        new.append(f"Line {line_num} from File 2: {','.join(lines2[line_num - 1])}")
        logger.info(new)
    return missing,new,changed

if __name__ == "__main__":
    file1_path = r"C:/tmp/CSVfiles/EmployeeData.csv"
    file2_path = r"C:/tmp/files/EmployeeData2.csv"
    compare_csv_files(file1_path, file2_path)
