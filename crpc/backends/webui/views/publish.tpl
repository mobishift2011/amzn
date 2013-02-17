%include header title="Data Process Tasks", description="", author="", scripts=["/assets/js/controllers/DT_bootstrap.js"], csses=["/assets/css/DT_bootstrap.css"]

% LB, RB = '{{', '}}'

  <body>

    %include navigation

    <div class="container">

      <h1>monitor, control</h1>
        
      <ul class="nav nav-pills">
        <li><a href="/task">Tasks</a> </li>
        <li><a href="/control">Control</a></li>
        <li class="active"><a href="/publish">Publish</a></li>
        <li><a href="/history">History</a></li>
        <li><a href="/graph">Graph</a></li>
      </ul>

      <div class='span1'>
        <ul class='nav nav-pills'>
          <li><a href='/publish/chkpub'>check</a></li>
          <li><a href='/publish/stats'>stats</a></li>
          <li><a href='/publish/report'>report</a></li>
          <li><a href='/publish/updatereport'>updatereport</a></li>
        </ul>
      </div>
    </div> <!-- /container -->

    <!-- Le javascript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->

  </body>
</html>

