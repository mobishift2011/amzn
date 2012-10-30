%include header title="Crawler Tasks", description="", author="", scripts=["/assets/js/controllers/tasks.js","/assets/js/controllers/DT_bootstrap.js"], csses=["/assets/css/DT_bootstrap.css"]

% LB, RB = '{{', '}}'

  <body>

    %include navigation

    <div class="container">

      <h1>monitor, control</h1>
        
      <ul class="nav nav-pills">
        <li class="active">
            <a href="#">Tasks</a>
        </li>
        <li><a href="/control">Control</a></li>
      </ul>

      <div class="container" style="margin-top: 10px" ng-controller="TaskCtrl"> 
        <table cellpadding="0" cellspacing="0" border="0" class="table table-striped table-bordered" id="taskTable">
          <thead>
            <tr>
              <th>Task</th>
              <th>Status</th>
              <th>Started At</th>
              <th>Updated At</th>
              <th>Dones</th>
              <th>Updates</th>
              <th>News</th>
              <th>Fails</th>
            </tr>
          </thead>
          <tbody>
            <tr ng-repeat="task in tasks">
              <td>{{LB}}task.name{{RB}}</td>
              <td>{{LB}}task.status{{RB}}</td>
              <td>{{LB}}task.started_at{{RB}}</td>
              <td>{{LB}}task.updated_at{{RB}}</td>
              <td>{{LB}}task.dones{{RB}}</td>
              <td>{{LB}}task.updates{{RB}}</td>
              <td>{{LB}}task.news{{RB}}</td>
              <td>{{LB}}task.fails{{RB}}</td>
            </tr>
          </tbody>
        </table>            
      </div>
    </div> <!-- /container -->

    <!-- Le javascript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->

  </body>
</html>

