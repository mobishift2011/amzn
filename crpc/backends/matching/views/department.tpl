        <div class="span3">
          <h2>Menu</h2>
          <div class="well sidebar-nav">
            <ul class="nav nav-list">
              <li class="nav-header">View</li>
              <li class="active"><a href="/department/">Departments</a></li>
              <li><a href="/training-set/">Training Sets</a></li>
              <li class="nav-header">Train</li>
              <li><a href="/teach/">Teach</a></li>
              <li><a href="/validate/">Validate</a></li>
              <li><a href="/event/list/">Events</a></li>
              <li class="nav-header">Test</li>
              <li><a href="/cross-validation/">Cross Validation</a></li>
            </ul>
          </div><!--/.well -->
        </div><!--/span-->
        <div class="span9">
          <h2> Department List </h2>
          <table class="table table-striped span5">
            <thead>
              <tr>
                <th>Tier1</th>
                <th>Tier2</th>
              </tr>
            </thead>
            <tbody>
            %for main, sublist in departments.items():
              %for sub in sublist:
              <tr>
                <td>{{main}}</td>
                <td>{{sub}}</td>
              </tr>
              %end
            %end
            </tbody>
          </table>
        </div><!--/span-->

        %rebase layout
