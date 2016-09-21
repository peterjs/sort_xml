# coding=utf-8
import os, fnmatch, shutil

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
  return get_value_from_xml_file(xml_file, ["P21697063201","P21697208301"])
  
def get_sr_kod_from_xml2(xml_file):
  sr_kod = ""
  f = open(xml_file, 'r')
  lines = f.read()
  if lines.find("P21697063201") != -1:
    sr_kod = "P21697063201"
  elif lines.find("P21697208301") != -1:
    sr_kod = "P21697208301"
  f.close()
  return sr_kod

def copy_file_to_dir(vstup_subor, vystup_zlozka):
  shutil.copy(vstup_subor, vystup_zlozka)
  return
  
def log(log_file, text):
  #concat pripoj text k suboru log_file 
  return

def main():
  source_directory = "C:\\export_winlab_lab_lv"
  amb_directory = "C:\\vysledky_amb"
  dial_directory = "C:\\vysledky_dial"
  for xml_file in xmls_in_dir(source_directory):
    if check_xml(xml_file):
      full_path_to_file = os.path.join(source_directory,xml_file)
      print(full_path_to_file)
      sr_kod = get_sr_kod_from_xml(full_path_to_file)
      name = get_name_from_xml(full_path_to_file)
      print(sr_kod)
      if sr_kod == "P21697208301" and name == "HESS":
        copy_file_to_dir(full_path_to_file, dial_directory)        
      elif sr_kod == "P21697063201" and name == "HESS":
        copy_file_to_dir(full_path_to_file, amb_directory)
      else:
        log("log.txt","chybny sr_kod " + str(sr_kod) + " v subore " + str(xml_file) +"\n")
  return
  
main()
