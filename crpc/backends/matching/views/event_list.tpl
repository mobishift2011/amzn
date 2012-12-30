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
        <div class="tabbable span9">
          <ul class="nav nav-tabs">
            %for i, site_events in enumerate(sk.iteritems()):
              %site, events = site_events
              %if events:
                %if i==0:
                  <li class="active"><a href="#tab-{{site}}" data-toggle="tab">{{site}}</a></li>
                %else:
                  <li><a href="#tab-{{site}}" data-toggle="tab">{{site}}</a></li>
                %end
              %end
            %end
          </ul>
          <div class="tab-content">
          %for i, site_events in enumerate(sk.iteritems()):
            %site, events = site_events
            %if i==0:
              <div class="tab-pane active" id="tab-{{site}}">
            %else:
              <div class="tab-pane" id="tab-{{site}}">
            %end
            %if events:
              <h3>Events for {{ site }}</h3>
              %for eid, url in events:
              <div style="width:20%;padding:5px;float:left;">
                <a href="/event/{{site}}_{{eid}}/"><img src="{{!url}}" /></a>
              </div>
              %end
            %end
            </div>
          %end
          </div>
        </div><!--/tabbable-->

        %rebase layout
