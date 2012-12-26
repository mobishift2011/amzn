%include header title="Publish Stats", description="", author="", scripts=["/assets/js/controllers/DT_bootstrap.js"], csses=["/assets/css/DT_bootstrap.css"]

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
            <li><a href='/publish/chkpub'>check</a></li>
            <li class='active'><a href='/publish/stats'>stats</a></li>
          </ul>
        </div>

        <div class='span12'>
          %if stats or stats == []:
            <table class='table table-striped'>
                <thead>
                  <tr>
                    <th>image number</th>
                    <th>propagate number</th>
                    <th>publish number </th>
                    <th>begin</th>
                    <th>end</th>
                  </tr>
                </thead>
                <tbody>
                  %for stat in stats:
                    <tr>
                      <td>{{ stat['image_num'] }}</td>
                      <td>{{ stat['prop_num'] }}</td>
                      <td>{{ stat['publish_num'] }}</td>
                      <td>{{ stat['extent_left'] }}</td>
                      <td>{{ stat['extent_right'] }}</td>
                    </tr>
                  %end
                </tbody>
            </table>

          %else:
            <form method='post' action='#'>
              <div class='row'>
                <div class='span4'>
                  <label>begin from</label>
                  <input size="30" id="f_begin" name='begin_at'/><button id="f_btn_begin">choose</button><br />
                </div>
                <div class='span4'>
                  <label>end to</label>
                  <input size="30" id="f_end" name='end_at'/><button id="f_btn_end">choose</button><br />
                </div>
                <div class='span4'>
                  <label>interval</label>
                  <input type='number' name='time_value' value='1'/> 
                  <select name='time_cell'>
                    <option>minutes</option>
                    <option>hours</option>
                    <option>days</option>
                  </select>
                </div>
              </div>
              <br/>

              <div class='row'>
                <div class='span4'>
                  <label>site</label>
                  <select name='site'>
                    %for site in sites:
                    <option>{{ site }}</option>
                    %end
                  </select>             
                </div>
                <div class='span4'>
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
              </div>

            </form>
          %end
        </div>

      </div> <!-- /container -->

    </div>
    <!-- Le javascript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->

    <script src="../assets/js/cal/jscal2.js"></script>
    <script src="../assets/js/cal/lang/en.js"></script>
    <link rel="stylesheet" type="text/css" href="../assets/css/cal/jscal2.css" />
    <link rel="stylesheet" type="text/css" href="../assets/css/cal/border-radius.css" />
    <link rel="stylesheet" type="text/css" href="../assets/css/cal/steel/steel.css" />

    <script type="text/javascript">//<![CDATA[
      Calendar.setup({
        inputField : "f_begin",
        trigger    : "f_btn_begin",
        onSelect   : function() { this.hide() },
        showTime   : true,
        dateFormat : "%Y-%m-%d %H:%M:00"
      });
      Calendar.setup({
        inputField : "f_end",
        trigger    : "f_btn_end",
        onSelect   : function() { this.hide() },
        showTime   : true,
        dateFormat : "%Y-%m-%d %H:%M:00"
      });
    //]]></script>
  </body>
</html>