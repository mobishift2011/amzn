
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
%LB, RB = '{{', '}}'
<html lang="en" ng-app>
  <head>
    <meta charset="utf-8">
    <title>Crawler Monitor, from Favbuy</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="">
    <meta name="author" content="">

    <!-- Le styles -->
    <link href="../assets/css/bootstrap.css" rel="stylesheet">
    <style>
      body {
        padding-top: 60px; /* 60px to make the container go all the way to the bottom of the topbar */
      }
    </style>
    <link href="../assets/css/bootstrap-responsive.css" rel="stylesheet">


    <script type="text/javascript" charset="utf-8" language="javascript" src="/assets/js/jquery-1.8.2.min.js"></script>
    <script type="text/javascript" charset="utf-8" language="javascript" src="/assets/js/jquery.dataTables.min.js"></script>

    <link rel="stylesheet" type="text/css" href="/assets/css/DT_bootstrap.css">
    <script src="/assets/js/angular.min.js"></script>
    <script src="/assets/js/table.js"></script>
    <script type="text/javascript" charset="utf-8" language="javascript" src="/assets/js/DT_bootstrap.js"></script>

    <!-- Le HTML5 shim, for IE6-8 support of HTML5 elements -->
    <!--[if lt IE 9]>
      <script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>
    <![endif]-->

  </head>

  <body>

    <div class="navbar navbar-inverse navbar-fixed-top">
      <div class="navbar-inner">
        <div class="container">
          <a class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </a>
          <a class="brand" href="#">Monitor</a>
          <div class="nav-collapse collapse">
            <ul class="nav">
              <li class="active"><a href="#">Crawlers</a></li>
              <li><a href="#about">About</a></li>
            </ul>
          </div><!--/.nav-collapse -->
        </div>
      </div>
    </div>

    <div class="container">

      <h1>monitor, control</h1>
        
      <ul class="nav nav-pills">
        <li class="active">
            <a href="#">Tasks</a>
        </li>
        <li><a href="#">Summary</a></li>
        <li><a href="#">Control</a></li>
      </ul>

      <div class="container" style="margin-top: 10px" ng-controller="TableCtrl"> 
        <table cellpadding="0" cellspacing="0" border="0" class="table table-striped table-bordered" id="example">
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

