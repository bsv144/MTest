from urllib.parse import parse_qs
from html import escape
import sqlite3

# Path to sqlite3 DB file
DB_FILE = './db/test.db'
DB_INITSCRIPT = './db/init.sql'


# Make and init db
def db_init():
    with sqlite3.connect(DB_FILE) as conn:
        #Read init sql script and execute
        with open(DB_INITSCRIPT,'r',encoding='utf-8') as f:
            sql_script = f.read()
            conn.executescript(sql_script)
        conn.commit()


# html.escape
def app_wsgi(environ, start_response):
    path_info = environ['PATH_INFO'].strip("/")
    query_string = environ['QUERY_STRING']
    request_method = environ['REQUEST_METHOD']
    print("path_info: %s" % path_info)
    print("query_string: %s" % query_string)
    print("request_method: %s" % request_method)
    start_response('200 OK', [('Content-Type', 'Text/Html')])
    routes = {'admin':app_admin(),'comment':app_comment(environ),'view':app_view(),'stat':app_stat()}
    if path_info in routes:
        padge = routes[path_info]
    else:
        padge = routes['comment']
    return[str.encode(padge)]

def app_admin():
    db_init()
    return('Admin  page')

def app_comment(environ):
    if environ['REQUEST_METHOD'] == 'POST':
        #Обрабатываем ajax запрос по региону
        try:
            request_body_size = int(environ['CONTENT_LENGTH'])
            request_body = environ['wsgi.input'].read(request_body_size)
        except (TypeError, ValueError):
            request_body = 0
        #print(parse_qs(request_body.decode('utf-8')))
        #print(type(request_body.decode('utf-8')))
        with sqlite3.connect(DB_FILE) as conn:
            cur = conn.cursor()
            q_param = (parse_qs(request_body.decode('utf-8'))['region'][0],)
            cicies_list = [row[0] for row in cur.execute("select city from cities inner join regions on cities.region_id = regions.region_id where region = ?;", q_param)]
        #print(cicies_list)
        #print(type(cicies_list))
        #print(",".join(cicies_list))
        return(",".join(cicies_list))
    else:
        with open('./html/form_comment.html','r',encoding='utf-8') as f:
            padge = f.read()
        #Добавляем регионы в шаблон
        with sqlite3.connect(DB_FILE) as conn:
            cur = conn.cursor()
            option_list = ["<option> %s </option>" % row for row in cur.execute("select region from regions;")]
        region_option = "".join(option_list)
        padge = padge.replace('{region}', region_option)
        return(padge)


def app_view():
    return('View page')

def app_stat():
    return('Stat page')

if __name__ == '__main__':
    try:
        from wsgiref.simple_server import make_server
        httpd = make_server('', 8080, app_wsgi)
        print('Serving on port 8080...')
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('Goodbye.')