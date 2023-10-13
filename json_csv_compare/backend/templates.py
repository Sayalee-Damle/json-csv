system_template_converter = """You are desgined to convert json into a csv format"""

human_template_converter = """
You will give Python code to convert json file into a CSV file with all the keys as the column names and values as rows.
For the file {json}
Tell it to save at {path}
use pandas for execution
pass raw format of path
example: use r before path
do not change type of data from integer to decimal
"""

system_template_compare = """You are designed to compare files and point out the discrepencies between the two"""
human_template_compare = """
You will be given 2 .csv files. You will compare {csv1} with {csv2}. 
Give out the discrepencies and DO NOT MAKE CHANGES in any file!! 
show output in a csv file at {path} and mark discrepencies in red.
"""

system_template_change_output_format = """You are designed to change the format of the output"""
human_template_change_output_format = """show the following in a pretty format with bullet points {changed_lines}
like
"""