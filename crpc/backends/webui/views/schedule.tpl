<html>
    <head>
    </head>
    <body>
      <div class=span12>
        % for site in schedules:
            <h4>{{site.keys()[0]}}</h4>
            <ul>
                % for time, count in site.values()[0].iteritems():
                    <li>{{time}} &nbsp; &nbsp; &nbsp; &nbsp; {{count}}</li>
                % end
            </ul>
        % end
      </div>
    </body>
</html>
