%include header title="Publish Check", description="", author="", scripts=["/assets/js/controllers/DT_bootstrap.js"], csses=["/assets/css/DT_bootstrap.css"]

% LB, RB = '{{', '}}'

  <body>

    %include navigation
    <div class='row'>

      <div class="container">
        <h1>monitor, control</h1>
          
        <ul class="nav nav-pills">
          <li><a href="/task">Tasks</a> </li>
          <li><a href="/control">Control</a></li>
          <li class="active"><a href="#">Publish</a></li>
        </ul>

        <div class='span1'>
          <ul class='nav nav-pills nav-stacked'>
            <li class='active'><a href='/publish/chkpub'>check</a></li>
            <li><a href='/publish/stats'>stats</a></li>
          </ul>
        </div>

        <div class='span12'>
          %if stats or stats == []:
            % for stat in stats:
            <table class='table table-striped'>
                <thead>
                  <tr>
                    <th>site</th>
                    <th>{{ stat['site'] }}</th>
                  </tr>
                </thead>
                <tbody>
                  %for data in stat['data']:
                    <tr>
                      <td>{{ data[0] }}</td>
                      <td>{{ data[1] }}</td>
                    </tr>
                  %end
                </tbody>
            </table>
            <br />
            %end

          %else:
            <form method='post' action='#'>
              <div class='span3'>
                <label>site</label>
                <select name='site'>
                    <option>all</option>
                    %for site in sites:
                    <option>{{site}}</option>
                    %end
                </select>             
              </div>
              <div class='span3'>
                <label>doctype</label>
                <select name='doctype'>
                  <option>event</option>
                  <option>product</option>
                </select>
              </div>
              <div class='span3'>
                <p></p>
                <input type='submit' value='check' />
              </div>
            </form>
          %end
        </div>

      </div> <!-- /container -->

    </div>
    <!-- Le javascript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->

  </body>
</html>