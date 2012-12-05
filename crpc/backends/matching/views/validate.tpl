        <div class="span3">
          <h2>Menu</h2>
          <div class="well sidebar-nav">
            <ul class="nav nav-list">
              <li class="nav-header">View</li>
              <li><a href="/department/">Departments</a></li>
              <li><a href="/training-set/">Training Sets</a></li>
              <li class="nav-header">Train</li>
              <li><a href="/teach/">Teach</a></li>
              <li class="active"><a href="/validate/">Validate</a></li>
              <li class="nav-header">Test</li>
              <li><a href="/cross-validation/">Cross Validation</a></li>
            </ul>
          </div><!--/.well -->
        </div><!--/span-->
        <div class="span9">
          <h2> I'll show you how talent I am! </h2>
          <h4> for the text below </h4>
          <div class="well">
            {{!content}}
          </div>
          <h4>I guess it belongs to {{result}}</h4>
          <a id="ok" class="btn btn-success">Good Job!</a>
          <a id="teach" class="btn btn-danger">You Idiot!</a>
        </div><!--/span-->

        <script>
          $('#ok').live('click', function(){
            window.location.href = '/validate/';
          })
          $('#teach').live('click', function(){
            window.location.href = '/teach/?site_key='+'{{!site_key}}';
          })
        </script>

        %rebase layout