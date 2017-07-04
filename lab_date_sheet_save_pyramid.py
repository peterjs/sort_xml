from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPResetContent
import lab_date_sheet
from pyramid.response import Response
import sort_xml

@view_config(route_name='hello')
def hello_world(request):
    # return 'Hello World'
    patient_table = lab_date_sheet.create_page("../hd_lv/")
    # return request.GET
    return Response(patient_table)

@view_config(route_name='hello2', renderer='string')
def hello_world2(request):
    #save to date_remaps.txt
    print(list(request.GET.items()))
    with open("date_remaps.txt","w") as date_remaps:
        date_remaps.write(str(list(request.GET.items())))
    # return HTTPResetContent(location="file:///Users/peter/Code/sort_xml_peterjs/html_out.html")
    sort_xml.main("/Users/peter/Code/ftpes_lab_vysledky", "/Users/peter/Code/amb_lv", "/Users/peter/Code/amb_zel", "/Users/peter/Code/hd_lv", "/Users/peter/Dropbox/it/laboratorne_lv/pids_list.txt")
    return HTTPFound(location="http://localhost:8080")

@view_config(route_name='hello3', renderer='string')
def hello_world3(request):
    #save to date_remaps.txt
    sort_xml.main("/Users/peter/Code/ftpes_lab_vysledky", "/Users/peter/Code/amb_lv", "/Users/peter/Code/amb_zel", "/Users/peter/Code/hd_lv", "/Users/peter/Dropbox/it/laboratorne_lv/pids_list.txt")
    # return HTTPResetContent(location="file:///Users/peter/Code/sort_xml_peterjs/html_out.html")
    return HTTPFound(location="http://localhost:8080")

if __name__ == '__main__':
    config = Configurator()
    config.add_route('hello', '/')
    config.add_route('hello2', '/hello2')
    config.add_route('hello3', '/hello3')
    config.scan()
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()
