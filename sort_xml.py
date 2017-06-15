# coding=utf-8
import os, fnmatch, shutil,sys
from time import localtime, strftime
import xml.etree.ElementTree as ET
from datetime import datetime
import re

id_lis_map = {"HGB": "99901", "HTC": "99902", "WBC": "99903", "PLT": "99904", "RET%": "99905", "S-GLU": "01898", "S-UREA": "03085", "S-KREA": "01511", "S-KM ": "99910", "S-CB ": "99911", "S-ALB": "00504", "S-TBIL": "01153", "S-Fe": "99921", "S-TIBC": "99922", "S-FeSat": "99923", "S-FER": "99924", "S-Na": "99925", "S-K": "99926", "S-Ca": "99927", "S-Mg": "99928", "S-Cl": "99929", "S-P": "99930", "S-CRP hs": "99931","P-PTH": "99932", "S-vit.D": "99934", "U-pH": "99802", "U-BIEL": "99803", "U-GLUK": "99804", "U-KETO": "99805", "U-KRV": "99806", "U-BILI": "99807", "U-UBG": "99808", "U-ERY": "99812", "U-LEUK": "99813", "U-ValHYAL": "99814", "U-BAKT": "99815", "U-EPIguľ": "99816"}

def xmls_in_dir(directory):
  real_path = os.path.realpath(directory)
  if os.path.exists(real_path):
     return os.listdir(real_path)
  return []

def check_xml(file):
  #lower() - fix pre macOS
  return fnmatch.fnmatch(file.lower(), '*.xml')

def read_xml():
  return

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

def get_sr_kod_from_xml(xml_file):
  return get_value_from_xml_file(xml_file, ["P21697063201","P21697208301","P21697063203"])

def load_patient_ids_to_extend(pid_file):
  pids_list = []
  with open(pid_file, "r") as pids:
    for pid in pids:
      pids_list.append(pid.strip())
  return pids_list

def xml_get_patient_name(root):
  return root.find("is").find("ip").find("prijmeni").text

def modify_lab_test_codes(xml_tree_node):
  for lab_test in xml_tree_node.iter("vr"):
    lab_test.set("klic_nclp", id_lis_map.get(lab_test.get("id_lis"),""))

def modify_lab_date(xml_tree_node):
  #poznamka kedy bola vzorka prijata - nemusi sa zhodovat s dnom vyhodnotenia
  #nastavi pri jednotlivych vysetrovanych parametroch datum prijatia vzorky s casom pred polnocou
  for note in xml_tree_node.iter("ptext"):
    #print(note.tag)
    if(note.text):
      #if prijaty dna -1 and filename 0 then change dates, else log error
      print(note.text)
      #<ptext>@@147=536</ptext>
      if note.text[0] != "@":
        sample_date_str = note.text.replace("Materiál prijatý dňa ","")
        #<ptext>Materiál prijatý dňa 1.5.2017 v ÚPS, vyšetrenie doordinované.</ptext>
        sample_date_str = sample_date_str.replace(" v ÚPS, vyšetrenie doordinované.", "")
        #<ptext>Materiál prijatý dňa 29.5.2017 , vyšetrenia doordinované.\n@@ č.232</ptext>
        #Materiál prijatý dňa  30.5.2017, vyšetrenia doordinované.\n@@60
        sample_date_str = sample_date_str.strip()
        date_re_pattern = re.compile("\A\d{1,2}.\d{1,2}.\d\d\d\d")
        sample_date_str = date_re_pattern.match(sample_date_str).group()
        sample_date = datetime.strptime(sample_date_str,"%d.%m.%Y")
        # print()
        # print(sample_date)
        # print()
        for parameter_date in xml_tree_node.iter("dat_du"):
        #   print(parameter_date.text)
        #   print(sample_date.strftime("%Y-%m-%dT%H:%M:%S"))
          parameter_date.text = sample_date.strftime("%Y-%m-%dT23:59:59")

def modify_patient_ids(xml_tree_node, pids_to_extend):
  for pid in xml_tree_node.iter("rodcis"):
    if pid.text in pids_to_extend:
      pid.text = pid.text + "0"

def modify_xml(xml_file, pids_list_path):
  #with open(xml_file, "w+", encoding="cp1250") as lab_tests_file:
  tree = ET.parse(xml_file)
  root = tree.getroot()
  print(xml_get_patient_name(root))
  modify_lab_test_codes(root)
  modify_lab_date(root)
  modify_patient_ids(root, load_patient_ids_to_extend(pids_list_path))
  tree.write(xml_file,encoding="cp1250")

def get_datetime_from_filename(file_name):
  file_name = sample_date_str = file_name.replace("PRO_OKB_00013_","")
  file_name = sample_date_str = file_name.replace("PRO_OKB_00014_","")
  date_re_pattern = re.compile("\A\d\d\d\d_\d\d_\d\d")
  date_str = date_re_pattern.match(file_name).group()
  sample_date = datetime.strptime(date_str,"%Y_%m_%d")
  return sample_date

def rm_from_dir(directory):
  files = [os.path.join(directory, item) for item in os.listdir(directory)]
  for f in files:
    os.remove(f)

def copy_file_to_dir(vstup_subor, vystup_zlozka):
  shutil.copy(vstup_subor, vystup_zlozka)
  return

def log(log_file, xml_file):
  with open(log_file, "a+") as log:
      err_message = ("Neplatny kod ambulancie v subore " + str(xml_file) +"\n")
      formated_date_time = strftime("%Y-%m-%d %H:%M:%S", localtime())
      log.write( "[  " + formated_date_time + "  ]" + "  :" + "  " + err_message )
  return

def help_syntax():
  print("python sort_xml.py source_directory  ambulance1_directory ambulance2_directory ambulance3_directory")
  return

def main():
  source_directory = sys.argv[1]
  amb_directory = sys.argv[2]
  amb2_directory = sys.argv[3]
  dial_directory = sys.argv[4]
  pids_list_path = sys.argv[5]
  #cleanup
  if datetime.today().hour == 14:
    rm_from_dir(amb_directory)
    rm_from_dir(amb2_directory)
    rm_from_dir(dial_directory)
  for xml_file in xmls_in_dir(source_directory):
    if check_xml(xml_file):
      full_path_to_file = os.path.join(source_directory,xml_file)
      print(full_path_to_file)
      sr_kod = get_sr_kod_from_xml(full_path_to_file)
      name = get_name_from_xml(full_path_to_file)
      get_datetime_from_filename(xml_file)
      sample_age = datetime.today() - get_datetime_from_filename(xml_file)
      if sample_age.days < 11:
          #      print(sr_kod)
        if sr_kod == "P21697208301":
          copy_file_to_dir(full_path_to_file, dial_directory)
          modify_xml(os.path.join(dial_directory,xml_file), pids_list_path)
        elif sr_kod == "P21697063201":
          copy_file_to_dir(full_path_to_file, amb_directory)
          modify_xml(os.path.join(amb_directory,xml_file), pids_list_path)
        elif sr_kod == "P21697063203":
          copy_file_to_dir(full_path_to_file, amb2_directory)
          modify_xml(os.path.join(amb2_directory,xml_file), pids_list_path)
        else:
          log("log.txt", xml_file)
  return

main()
