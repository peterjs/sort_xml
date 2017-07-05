from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPResetContent
import lab_date_sheet
from pyramid.response import Response
import sort_xml
import os

HD_LV = "C:\\Users\\admin\\laboratorne\\hd_lv"
PIDS_LIST = "C:\\Users\\admin\\laboratorne\\pids_list.txt"
HD_LV = "/Users/peter/Code/hd_lv/"
HD_LV = "../hd_lv/"
PIDS_LIST = "/Users/peter/Dropbox/it/laboratorne_lv/pids_list.txt"
#"http://192.168.48.242:8080"

@view_config(route_name='hello')
def hello_world(request):
    # return 'Hello World'
    patient_table = lab_date_sheet.create_page(HD_LV)
    # return request.GET
    return Response(patient_table)

@view_config(route_name='hello2', renderer='string')
def hello_world2(request):
    #save to date_remaps.txt
    print(list(request.GET.items()))
    with open("date_remaps.txt","w") as date_remaps:
        multiple_dates_to_change = [(item[0],request.GET.get(item[0])) for item in list(request.GET.items()) if item[1] == "on"]
        set_to_date = ""
        if len(multiple_dates_to_change):
            set_to_date = multiple_dates_to_change[0][1]
        multiple_dates_to_change = {item[0]:set_to_date for item in multiple_dates_to_change}
        mappings = [(item[0], multiple_dates_to_change.get(item[0], item[1])) for item in list(request.GET.items()) if item[1] != "on"]
        print("multiple_dates_to_change")
        print(multiple_dates_to_change)
        print("")
        print("mappings")
        print(mappings)
        date_remaps.write(str(mappings))
    # return HTTPResetContent(location="file:///Users/peter/Code/sort_xml_peterjs/html_out.html")
    # sort_xml.main("C:\\Users\\admin\\ftpes_lab_vysledky", "C:\\Users\\admin\\laboratorne\\amb_lv", "C:\\Users\\admin\\laboratorne\\amb_zel", "C:\\Users\\admin\\laboratorne\\hd_lv", "C:\\Users\\admin\\laboratorne\\pids_list.txt")
    sort_xml.change_dial_dates(HD_LV, PIDS_LIST)
    return HTTPFound(location="http://localhost:8080")
    #return HTTPFound(location="")

@view_config(route_name='hello3', renderer='string')
def hello_world3(request):
    filename = request.GET["file"]
    try:
        with open(os.path.join(HD_LV, filename), "r", encoding="cp1250") as xml_file:
            return xml_file.read()
    except FileNotFoundError as fe:
        print("filename " + "does not exist")
    return HTTPFound(location="http://localhost:8080")
    #return HTTPFound(location="")

if __name__ == '__main__':
    config = Configurator()
    config.add_route('hello', '/')
    config.add_route('hello2', '/hello2')
    config.add_route('hello3', '/hello3')
    #config.add_static_view(name='static', path="c:\\Users\\admin\\laboratorne")
    config.scan()
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()
