from bottle import route, run, template
from crawlers.common.models import Stat, session

@route('/')
def index():
    ss = session.query(Stat)
    return template('''
        <table border="1">
        <thead>
          <tr>
            <td>ID</td>
            <td>Crawler</td>
            <td>Created at</td>
            <td>Updated at</td>
            <td>Finished?</td>
            <td>num of operations</td>
            <td>num of errors</td>
            <td>the errors list</td>
          </tr>
        </thead> 
        <tbody>
        %for s in ss:
          <tr>
            <td>{{s.sid}}</td>
            <td>{{s.crawler}}</td>
            <td>{{s.created_at}}</td>
            <td>{{s.updated_at}}</td>
            <td>{{s.stopped}}</td>
            <td>{{s.loops}}</td>
            <td>{{s.errors}}</td>
            <td>{{s.errors_list}}</td>
          </tr>
        %end
        </tbody>
        </table>
    ''', ss=ss)

run(host='0.0.0.0', port=8111)
