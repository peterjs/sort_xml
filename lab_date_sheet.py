import os, fnmatch, sys
import xml.etree.ElementTree as ET
from datetime import datetime
import re, ast

def xmls_in_dir(directory):
    real_path = os.path.realpath(directory)
    if os.path.exists(real_path):
        return os.listdir(real_path)
    return []

def check_xml(file):
    #lower() - fix pre macOS
    return fnmatch.fnmatch(file.lower(), '*.xml')

def get_datetime_from_filename(file_name):
  file_name = sample_date_str = file_name.replace("PRO_OKB_00013_","")
  file_name = sample_date_str = file_name.replace("PRO_OKB_00014_","")
  date_re_pattern = re.compile("\A\d\d\d\d_\d\d_\d\d")
  date_str = date_re_pattern.match(file_name).group()
  sample_date = datetime.strptime(date_str,"%Y_%m_%d")
  return sample_date

def xml_get_patient_name(root):
  return root.find("is").find("ip").find("prijmeni").text






#odmazat aj z druheho suboru
def get_value_from_xml_file(xml_file, values):
  found_value = ""
  f = open(xml_file, 'r', encoding="cp1250")
  lines = f.read()
  for value in values:
    if lines.find(value) != -1:
      found_value = value
  f.close()
  return found_value

def get_name_from_xml(xml_file):
  return get_value_from_xml_file(xml_file, ["HESS"])







def generate_html(table_values):
    head = """<html>
    <style>
    table, th, td {
        border: 1px solid black;
        border-collapse: collapse;
    }
    </style>
    <body>
    <form action="hello2" method="get">
    <input type="submit" value="ulozit">
    <table>
    <tr>
      <col width="150">
      <col width="100">
      <col width="100">
      <col width="100">
      <th>
        meno
      </th>
      <th>
        povodny datum
      </th>
      <th>
        momentalny datum
      </th>
      <th>
        upravit na datum
      </th>
      <th>
        vysetrenia
       </th>
    </tr>"""
    tail = """</table></form>
    </body>
    </html>"""
    table_rows = ""
    for val in table_values:
        bgcolor = "#FFFFFF"
        default_date = val[1].date()
        default_date2 = default_date.strftime("%d-%m-%Y")
        default_date3 = default_date2
        default_date4 = default_date.strftime("%Y-%m-%d")
        try:
            default_date3 = datetime.strptime(val[5],"%Y-%m-%d").strftime("%d-%m-%Y")
            default_date4 = val[5]
            if default_date2 != default_date3:
                bgcolor = "#BB9955"
            # print(default_date)
        except ValueError as e:
            print(val)
            print(e)
        table_rows += "<tr><td><a href='hello3?file=" + val[2] + "'>" + val[0] + "</a></td><td>" + default_date2 + "</td><td bgcolor=" + bgcolor + ">" + default_date3 + "</td><td><input type='date' name='" + val[4] + "' value='" + default_date4 + "'></td><td>" + val[3] + "</td></tr>"
    html = head + table_rows + tail
    return html

def get_lab_test_types(xml_tree_node):
    return [lab_test.get("id_lis") for lab_test in xml_tree_node.iter("vr")]
    for lab_test in xml_tree_node.iter("vr"):
        lab_test.get("id_lis")

def create_page(source_directory):
    name_dates = []
    remaps = {}
    try:
	    with open("date_remaps.txt","r") as date_remaps:
	        remaps = ast.literal_eval(date_remaps.readline())
	        remaps = dict(remaps)
    except FileNotFoundError as fe:
	    print("deta_remaps.txt does not exist")
    for xml_file in xmls_in_dir(source_directory):
        if check_xml(xml_file):
            full_path_to_file = os.path.join(source_directory,xml_file)
            tree = ET.parse(full_path_to_file)
            root = tree.getroot()
            name = xml_get_patient_name(root)
            # name = get_name_from_xml(full_path_to_file)
            lab_datetime = get_datetime_from_filename(xml_file)
            # print(name + " : " + str(lab_datetime))
            name_dates.append((name, lab_datetime, full_path_to_file, str(get_lab_test_types(root)), xml_file, remaps.get(xml_file,"0000-00-00")))
            # print(get_lab_test_types(root))
            # print(generate_html(name_dates))
    return generate_html(name_dates)

if __name__ == '__main__':
    with open("html_out.html","w") as html_out:
        html_out.write(create_page(sys.argv[1]))
