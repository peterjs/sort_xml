from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPResetContent
import lab_date_sheet
from pyramid.response import Response
import sort_xml
import os

@view_config(route_name='hello')
def hello_world(request):
    # return 'Hello World'
    patient_table = lab_date_sheet.create_page("C:\\Users\\admin\\laboratorne\\hd_lv")
    # return request.GET
    return Response(patient_table)

@view_config(route_name='hello2', renderer='string')
def hello_world2(request):
    #save to date_remaps.txt
    print(list(request.GET.items()))
    with open("date_remaps.txt","w") as date_remaps:
        date_remaps.write(str(list(request.GET.items())))
    # return HTTPResetContent(location="file:///Users/peter/Code/sort_xml_peterjs/html_out.html")
    # sort_xml.main("C:\\Users\\admin\\ftpes_lab_vysledky", "C:\\Users\\admin\\laboratorne\\amb_lv", "C:\\Users\\admin\\laboratorne\\amb_zel", "C:\\Users\\admin\\laboratorne\\hd_lv", "C:\\Users\\admin\\laboratorne\\pids_list.txt")
    sort_xml.change_dial_dates("C:\\Users\\admin\\laboratorne\\hd_lv", "C:\\Users\\admin\\laboratorne\\pids_list.txt")
    return HTTPFound(location="http://192.168.48.242:8080")
    #return HTTPFound(location="")

@view_config(route_name='hello3', renderer='string')
def hello_world3(request):
    filename = request.GET["file"]
    try:
        with open(os.path.join("C:\\Users\\admin\\laboratorne\\hd_lv", filename), "r") as xml_file:
            return xml_file.read()
    except FileNotFoundError as fe:
        print("filename " + "does not exist")
    return HTTPFound(location="http://192.168.48.242:8080")
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
