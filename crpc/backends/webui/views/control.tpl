
%include header title="Crawler Controls", description="", author="", scripts=["/assets/js/controllers/controls.js"], csses=["/assets/css/controls.css"]

%LB, RB = '{{', '}}'

    <body>
        
      %include navigation

      <div class="container">
        <h1>monitor, control</h1>
        
        <ul class="nav nav-pills">
          <li><a href="/task">Tasks</a></li>
          <li class="active"><a href="#">Control</a></li>
          <li><a href="/publish">Publish</a></li>
        </ul>
        <div class="container" style="margin-top: 10px" ng-controller="ScheduleCtrl">

        <form>
            <a href="#" class="btn btn-primary" ng-click="autoSchedule(true)">Start Auto-Schedule</a>
            <a href="#" class="btn btn-primary" ng-click="autoSchedule(false)">Stop Auto-Schedule</a>
        </form>
        
        <em>* Click Cell to Edit</em>
<table cellpadding="0" cellspacing="0" border="0" class="table table-striped table-bordered" id="schedule">
    <thead>
        <tr>
            <th>Crawler.Method</th>
            <th>Description</th>
            <th>Crontab Arguments</th>
            <th>Enabled</th>
            <th>Control</th>
        </tr>
    </thead>
    <tbody>
        <tr ng-repeat="s in schedules">
            <td ng-class="{editing: s == editedSchedule1}">
                <div class="view"><label ng-click="editSchedule1(s)">{{LB}}s.name{{RB}}</label></div>
                <form class="edit"><input ng-model="s.name" ctrl-blur="doneEditing1(s)" ctrl-focus="s == editedSchedule1"></form>
            </td>
            <td ng-class="{editing: s == editedSchedule2}">
                <div class="view"><label ng-click="editSchedule2(s)">{{LB}}s.description{{RB}}</label></div>
                <form class="edit"><input ng-model="s.description" ctrl-blur="doneEditing2(s)" ctrl-focus="s == editedSchedule2"></form>
            </td>
            <td ng-class="{editing: s == editedSchedule3}">
                <div class="view"><label ng-click="editSchedule3(s)">{{LB}}s.crontab_arguments{{RB}}</label></div>
                <form class="edit"><input ng-model="s.crontab_arguments" ctrl-blur="doneEditing3(s)" ctrl-focus="s == editedSchedule3"></form>
            </td>
            <td>
                <label ng-click="editSchedule4(s)">{{LB}}s.enabled{{RB}}</label>
            </td>
            <td><a href="#" ng-click="removeSchedule(s)">Delete</a>&nbsp;|&nbsp;<a herf="#" ng-click="runSchedule(s)">Run</a></td>
        </tr>
    </tbody>
</table>
        <form id="schedule-form" ng-submit="addSchedule()">
            <input type="text" class="span3" placeholder="CrawlerName" ng-model="newSchedule.name">
            <input type="text" class="span4" placeholder="Describe what it would do." ng-model="newSchedule.description">
            <input type="text" class="span2" placeholder="0 * * * *" ng-model="newSchedule.cron">
            <a href="#" class="btn btn-primary" ng-click="addSchedule()">ADD SCHEDULE</a>
        </form>
        

        </div>  <!-- ControlTask -->
      </div> <!-- containers -->
    </body>
</html>
