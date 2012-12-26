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
        <div class="container span9">
          <div>
          <h3>D0 List</h3>
          %for name in d0:
            <button class="btn" style="margin:3px;">{{name}}</button>
          %end
          </div>
          <div>
          <h3>D1 List</h3>
          %for name in d1:
            <button class="btn" style="margin:3px;">{{name}}</button>
          %end
          </div>
          <div>
          <h3>D2 List</h3>
            %for d1, d2list in d2dict.iteritems():
              <div>
              <span style="font-size:1.5em;">{{d1}}</span> 
              %for name in d2list:
                <button class="btn" style="margin:3px;">{{name}}</button>
              %end
              </div>
            %end
          </div>
        </div><!--/span-->

        %rebase layout
