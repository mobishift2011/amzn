
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
%LB, RB = '{{', '}}'
<html ng-app>
    <head>
        <meta http-equiv="content-type" content="text/html; charset=utf-8" />
        
        <title>DataTables example</title>
        
        <link rel="shortcut icon" type="image/ico" href="http://www.datatables.net/favicon.ico" />
        <link rel="stylesheet" type="text/css" href="/assets/css/bootstrap.css">

        <script type="text/javascript" charset="utf-8" language="javascript" src="/assets/js/jquery-1.8.2.min.js"></script>
        <script type="text/javascript" charset="utf-8" language="javascript" src="/assets/js/jquery.dataTables.min.js"></script>

        <link rel="stylesheet" type="text/css" href="/assets/css/DT_bootstrap.css">
        <script src="/assets/js/angular.min.js"></script>
        <script src="/assets/js/table.js"></script>
        <script type="text/javascript" charset="utf-8" language="javascript" src="/assets/js/DT_bootstrap.js"></script>
    </head>
    <body>
        <div class="container" style="margin-top: 10px" ng-controller="TableCtrl">
            
<table cellpadding="0" cellspacing="0" border="0" class="table table-striped table-bordered" id="example">
    <thead>
        <tr>
            <th>Task</th>
            <th>Status</th>
            <th>Update At</th>
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
            <td>{{LB}}task.updated_at{{RB}}</td>
            <td>{{LB}}task.dones{{RB}}</td>
            <td>{{LB}}task.updates{{RB}}</td>
            <td>{{LB}}task.news{{RB}}</td>
            <td>{{LB}}task.fails{{RB}}</td>
        </tr>
    </tbody>
</table>
            
        </div>
    </body>
</html>
