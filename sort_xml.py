# coding=utf-8
import os, fnmatch, shutil,sys
from time import localtime, strftime

def xmls_in_dir(directory):
  real_path = os.path.realpath(directory)
  if os.path.exists(real_path):
     return os.listdir(real_path)
  return []

def check_xml(file):
  return fnmatch.fnmatch(file, '*.xml')
  
def read_xml():
  return
  
def get_value_from_xml_file(xml_file, values):
  found_value = ""
  f = open(xml_file, 'r')
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
      elif sr_kod == "P21697063201":
        copy_file_to_dir(full_path_to_file, amb_directory)
      elif sr_kod == "P21697063203":
        copy_file_to_dir(full_path_to_file, amb2_directory)
      else:
        log("log.txt", xml_file)
  return
  
main()
