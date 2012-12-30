        <div class="span3">
          <h2>Menu</h2>
          <div class="well sidebar-nav">
            <ul class="nav nav-list">
              <li class="nav-header">View</li>
              <li><a href="/department/">Departments</a></li>
              <li><a href="/training-set/">Training Sets</a></li>
              <li class="nav-header">Train</li>
              <li><a href="/teach/">Teach</a></li>
              <li><a href="/validate/">Validate</a></li>
              <li class="active"><a href="/event/list/">Events</a></li>
              <li class="nav-header">Test</li>
              <li><a href="/cross-validation/">Cross Validation</a></li>
            </ul>
          </div><!--/.well -->
        </div><!--/span-->
        <div class="span9">
          <h2>Products of this Event</h2>
          <table class="table table-striped">
            <thead>
              <tr>
                <th>Product</th>
                <th>Guess</th>
                <th>Control</th>
              </tr>
            </thead>
            <tbody>
              %for p, r in zip(products, results):
              <tr>
                <td>
                  %for url in p.image_urls[:2]:
                    <img src="{{url}}" width="240" />
                  %end
                </td>
                <td>{{r}}</td>
                <td><a href="/teach/?site_key={{site}}_{{p.key}}">ReTrain</a></td>
              </tr>
              %end
            </tbody>
          </table> 

          <h2>The whole event belongs to...</h2>
          <div class="container">
          <div><a href="#" id="teach" class="btn">Train!!</a></div>
        </div>

        <script>
        </script>

        %rebase layout
