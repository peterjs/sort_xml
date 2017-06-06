# coding=utf-8
import os, fnmatch, shutil,sys
from time import localtime, strftime
import xml.etree.ElementTree as ET

id_lis_map = {"HGB": "99901", "HTC": "99902", "WBC": "99903", "PLT": "99904", "RET%": "99905", "S-GLU": "01898", "S-UREA": "03085", "S-KREA": "01511", "S-KM ": "99910", "S-CB ": "99911", "S-ALB": "00504", "S-TBIL": "01153", "S-Fe": "99921", "S-TIBC": "99922", "S-FeSat": "99923", "S-FER": "99924", "S-Na": "99925", "S-K": "99926", "S-Ca": "99927", "S-Mg": "99928", "S-Cl": "99929", "S-P": "99930", "S-CRP hs": "99931", "S-vit.D": "99934", "U-pH": "99802", "U-BIEL": "99803", "U-GLUK": "99804", "U-KETO": "99805", "U-KRV": "99806", "U-BILI": "99807", "U-UBG": "99808", "U-ERY": "99812", "U-LEUK": "99813", "U-ValHYAL": "99814", "U-BAKT": "99815", "U-EPIguľ": "99816"}


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

def modify_lab_test_codes(xml_file):
  #with open(xml_file, "w+", encoding="cp1250") as lab_tests_file:
  tree = ET.parse(xml_file)
  root = tree.getroot()
  for lab_test in root.iter("vr"):
    print(lab_test.get("id_lis"))
    print(id_lis_map.get(lab_test.get("id_lis"),""))
    print()
    lab_test.set("klic_nclp", id_lis_map.get(lab_test.get("id_lis"),""))
  tree.write(xml_file,encoding="cp1250")

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
  for xml_file in xmls_in_dir(source_directory):
    if check_xml(xml_file):
      full_path_to_file = os.path.join(source_directory,xml_file)
      print(full_path_to_file)
      sr_kod = get_sr_kod_from_xml(full_path_to_file)
      name = get_name_from_xml(full_path_to_file)
#      print(sr_kod)
      if sr_kod == "P21697208301":
        copy_file_to_dir(full_path_to_file, dial_directory)
        modify_lab_test_codes(os.path.join(dial_directory,xml_file))
      elif sr_kod == "P21697063201":
        copy_file_to_dir(full_path_to_file, amb_directory)
        modify_lab_test_codes(os.path.join(amb_directory,xml_file))
      elif sr_kod == "P21697063203":
        copy_file_to_dir(full_path_to_file, amb2_directory)
        modify_lab_test_codes(os.path.join(amb2_directory,xml_file))
      else:
        log("log.txt", xml_file)
  return

main()
