# coding=utf-8
import os, fnmatch, shutil, sys
from time import localtime, strftime
import xml.etree.ElementTree as ET
from datetime import datetime
import re, ast

id_lis_map = {"HGB": "99901", "HTC": "99902", "WBC": "99903", "PLT": "99904", "RET%": "99905", "S-GLU": "01898", "S-UREA": "03085", "S-KREA": "01511", "S-KM ": "99910", "S-CB ": "99911", "S-ALB": "00504", "S-TBIL": "01153", "S-AST": "99914", "S-ALT": "99915", "S-GMT": "99916", "S-ALP": "99917", "S-CHOL": "99918", "S-TG ": "99919", "S-Fe": "99921", "S-TIBC": "99922", "S-FeSat": "99923", "S-FER": "99924", "S-Na": "99925", "S-K": "99926", "S-Ca": "99927", "S-Mg": "99928", "S-Cl": "99929", "S-P": "99930", "S-CRP hs": "99931","P-PTH": "99932", "S-B2M": "99933", "S-vit.D": "99934", "NEU %": "99939", "U-pH": "99802", "U-BIEL": "99803", "U-GLUK": "99804", "U-KETO ": "99805", "U-KRV": "99806", "U-BILI": "99807", "U-UBG": "99808", "U-ERY": "99812", "U-LEUK": "99813", "U-ValHYAL": "99814", "U-BAKT": "99815", "U-EPIpl": "99816", "GF mer": "99819", "GF korig": "99820", "GFkal muži": "99821", "GFkal ženy": "99821", "TR H2O": "99824", "dU CB": "99825", "U-Na": "99827", "U-K": "99828", "U-Ca": "99829", "U-Mg": "99830", "U-Cl": "99831", "U-P": "99832", "U-KREA": "99834", "FE Na": "99836", "FE K": "99837", "FE Cl": "99838", "FE P": "99839", "FE Ca": "99840"}

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

def modify_lab_date2(xml_tree_node, to_date):
  for parameter_date in xml_tree_node.iter("dat_du"):
    print(parameter_date.text)
    #   print(sample_date.strftime("%Y-%m-%dT%H:%M:%S"))
    parameter_date.text = to_date.strftime("%Y-%m-%dT23:59:59")

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
        modify_lab_date2(xml_tree_node, sample_date)

def modify_patient_ids(xml_tree_node, pids_to_extend):
  for pid in xml_tree_node.iter("rodcis"):
    if pid.text in pids_to_extend:
      pid.text = pid.text + "0"

def get_lab_test_value(xml_tree_node, lab_test_name):
  for lab_test in xml_tree_node.iter("vr"):
 #   if lab_test.find("nazev_lclp").text == lab_test_name:
    if lab_test.get("id_lis") == lab_test_name:
      vrn = lab_test.find("vrn")
      if vrn:
        return vrn.find("hodnota").text
      else:
        return ""

def set_lab_test_value(xml_tree_node, lab_test_name, value):
  for lab_test in xml_tree_node.iter("vr"):
 #   if lab_test.find("nazev_lclp").text == lab_test_name:
    if lab_test.get("id_lis") == lab_test_name:
      vrn = lab_test.find("vrn")
      if vrn:
        vrn.find("hodnota").text = value

def modify_test_value(xml_tree_node, test_value_name, mod_function):
  test_value = get_lab_test_value(xml_tree_node, test_value_name)
  if test_value:
    test_value = test_value.replace(",",".")
    new_test_value = str(mod_function(float(test_value)))
    new_test_value = new_test_value.replace(".",",")
    set_lab_test_value(xml_tree_node, test_value_name, new_test_value)

def modify_b2m(xml_tree_node):
  modify_test_value(xml_tree_node, "B2M", lambda x: round(x*1000,2))
#  test_value = get_lab_test_value(xml_tree_node, "B2M")
#  if test_value:
#    test_value = test_value.replace(",",".")
#    new_test_value = str(round(float(test_value)*1000,2))
#    new_test_value = new_test_value.replace(".",",")
#    set_lab_test_value(root, "B2M", new_test_value)
 
def modify_xml(xml_file_dir, xml_file, pids_list_path):
 #with open(xml_file, "w+", encoding="cp1250") as lab_tests_file:
  xml_file_joined = os.path.join(xml_file_dir, xml_file)
  tree = ET.parse(xml_file_joined)
  root = tree.getroot()
  modify_xml_common(root, xml_file, pids_list_path)
  modify_xml_values(root)
  tree.write(xml_file_joined,encoding="cp1250")  

def modify_xml_witohut_values(xml_file_dir, xml_file, pids_list_path):
 #with open(xml_file, "w+", encoding="cp1250") as lab_tests_file:
  xml_file_joined = os.path.join(xml_file_dir, xml_file)
  tree = ET.parse(xml_file_joined)
  root = tree.getroot()
  modify_xml_common(root, xml_file, pids_list_path)
  tree.write(xml_file_joined,encoding="cp1250")  
  
def modify_xml_values(root):
 # modify_b2m(root)
  modify_test_value(root, "S-B2M", lambda x: round(x/1000,3))
  modify_test_value(root, "TR H2O", lambda x: round(x/100,3))
  modify_test_value(root, "FE Na", lambda x: round(x*100,2))
  modify_test_value(root, "FE K", lambda x: round(x*100,2))
  modify_test_value(root, "FE Cl", lambda x: round(x*100,2))
  modify_test_value(root, "FE P", lambda x: round(x*100,2))
  modify_test_value(root, "FE Ca", lambda x: round(x*100,2))
 
def modify_xml_common(root, xml_file, pids_list_path):
  modify_lab_test_codes(root)
  modify_lab_date(root)
  try:
    with open("date_remaps.txt","r") as date_remaps:
      remaps = ast.literal_eval(str.lower(date_remaps.readline()))
      remaps = dict(remaps)
      #print(xml_file)
      if remaps.get(str.lower(xml_file)):
      #   print(remaps)
        modify_lab_date2(root, datetime.strptime(remaps[str.lower(xml_file)],"%Y-%m-%d"))
        #print("REMAPPING")
        #print("REMAPPING")
  except FileNotFoundError as fe:
    print("deta_remaps.txt does not exist")
  modify_patient_ids(root, load_patient_ids_to_extend(pids_list_path))

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
  print("python sort_xml.py source_directory ambulance1_directory ambulance2_directory ambulance3_directory")
  return
  
def change_dial_dates(dial_directory, pids_list_path):
  for xml_file in xmls_in_dir(dial_directory):
    if check_xml(xml_file):
      full_path_to_file = os.path.join(dial_directory,xml_file)
      print(full_path_to_file)
      sr_kod = get_sr_kod_from_xml(full_path_to_file)
      name = get_name_from_xml(full_path_to_file)
      get_datetime_from_filename(xml_file)
      sample_age = datetime.today() - get_datetime_from_filename(xml_file)
      if sr_kod == "P21697208301":
        modify_xml_witohut_values(dial_directory, xml_file, pids_list_path)
      else:
        log("log.txt", xml_file)
  return

def main(source_directory, amb_directory, amb2_directory, dial_directory, pids_list_path):
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
          modify_xml(dial_directory, xml_file, pids_list_path)
        elif sr_kod == "P21697063201":
          copy_file_to_dir(full_path_to_file, amb_directory)
          modify_xml(amb_directory, xml_file, pids_list_path)
        elif sr_kod == "P21697063203":
          copy_file_to_dir(full_path_to_file, amb2_directory)
          modify_xml(amb2_directory, xml_file, pids_list_path)
        else:
          log("log.txt", xml_file)
  return

if __name__ == '__main__':
  source_directory = sys.argv[1]
  amb_directory = sys.argv[2]
  amb2_directory = sys.argv[3]
  dial_directory = sys.argv[4]
  pids_list_path = sys.argv[5]
  main(source_directory, amb_directory, amb2_directory, dial_directory, pids_list_path)
