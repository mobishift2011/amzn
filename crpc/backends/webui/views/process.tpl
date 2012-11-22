%include header title="Crawler Tasks", description="", author="", scripts=["/assets/js/controllers/DT_bootstrap.js"], csses=["/assets/css/DT_bootstrap.css"]

% LB, RB = '{{', '}}'

  <body>

    %include navigation

    <div class="container">

      <h1>monitor, control</h1>
        
      <ul class="nav nav-pills">
        <li><a href="/task">Tasks</a> </li>
        <li><a href="/control">Control</a></li>
        <li class="active"><a href="#">Progress</a></li>
      </ul>

      <div class="container" style="margin-top: 10px" ng-controller="TaskCtrl"> 
        <table cellpadding="0" cellspacing="0" border="0" class="table table-striped table-bordered" id="taskTable">
          <thead>
            <tr>
              <th>site</th>
              <th>key</th>
              <th>image complete</th>
              <th>image num</th>
              <th>branch complete</th>
              <th>transfered</th>
              <th>sold out</th>
              <th>started</th>
              <th>updated</th>
              <th>task</th>
              <th>task start</th>
            </tr>
          </thead>
          <tbody>
           %for progress in progresses:
            <tr>
              <td>{{progress.get('site')}}</td>
              <td>{{progress.get('key')}}</td>
              <td>{{progress.get('image_complete')}}</td>
              <td>{{progress.get('num_image')}}</td>
              <td>{{progress.get('branch_complete')}}</td>
              <td>{{progress.get('transfered')}}</td>
              <td>{{progress.get('soldout')}}</td>
              <td>{{progress.get('started_at')}}</td>
              <td>{{progress.get('updated_at')}}</td>
              <td>{{progress.get('task_title')}}</td>
              <td>{{progress.get('task_start')}}</td>
            </tr>
            %end
          </tbody>
        </table>            
      </div>
    </div> <!-- /container -->

    <!-- Le javascript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->

  </body>
</html>

