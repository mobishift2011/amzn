
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html lang="en" ng-app="monitor">
  <head>
    <meta charset="utf-8">
    <title>{{ title }}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{{ description }}">
    <meta name="author" content="{{ author }}">

    <!-- Le styles -->
    <link href="/assets/css/bootstrap.css" rel="stylesheet">
    <link href="/assets/css/bootstrap-responsive.css" rel="stylesheet">
    <link href="/assets/css/base.css" rel="stylesheet">


    <script type="text/javascript" charset="utf-8" language="javascript" src="/assets/js/libs/jquery-1.8.2.min.js"></script>
    <script type="text/javascript" charset="utf-8" language="javascript" src="/assets/js/libs/jquery.dataTables.min.js"></script>
    <script src="/assets/js/libs/angular.min.js"></script>
    <script src="/assets/js/monitor.js"></script>

    % for scriptpath in scripts:
        <script src="{{scriptpath}}"></script>

    % for csspath in csses:
        <link href="{{csspath}}" rel="stylesheet">

    <!-- Le HTML5 shim, for IE6-8 support of HTML5 elements -->
    <!--[if lt IE 9]>
      <script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>
    <![endif]-->

  </head>