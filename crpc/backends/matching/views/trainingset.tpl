        <div class="span3">
          <h2>Menu</h2>
          <div class="well sidebar-nav">
            <ul class="nav nav-list">
              <li class="nav-header">View</li>
              <li><a href="/department/">Departments</a></li>
              <li class="active"><a href="/training-set/">Training Sets</a></li>
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
          <h2> Training Sets </h2>
          <h4>Total Classes: {{len(dc)}}, Totoal Documents: {{sum(dc.values())}}</h4>
          <table class="table table-striped span8">
            <thead>
              <tr>
                <th class='span1'>D0</th>
                <th class='span2'>D1</th>
                <th class='span2'>D2</th>
                <th class='span1'>Counts</th>
                <th class='span2'>Details</th>
              </tr>
            </thead>
            <tbody>
            %for k, count in dc.iteritems():
              %d0, d1, d2 = k
              <tr>
                <td>{{d0}}</td>
                <td>{{d1}}</td>
                <td>{{d2}}</td>
                <td>{{count}}</td>
                <td>
                <div>
                  <a href="#detailmodal" role="button" data-toggle="modal" onclick="loadDetail(&quot;{{!d0}}&quot;, &quot;{{!d1}}&quot;, &quot;{{!d2}}&quot;);">See Details</a>
                </div>
                </td>
              </tr>
            %end
            </tbody>
          </table>
        </div><!--/span-->

        <!-- detail modal -->
        <div id="detailmodal" class="modal hide fade" tabindex="-1" role="dialog" aria-labelledby="detaillabel" aria-hidden="true">
          <div class="modal-header">
            <button type="button" class="close" data-dismiss="modal" aria-hidden="true">x</button>
            <h3 id="detaillabel">Details</h3>
          </div>
          <div class="modal-body">
            <p>loading...</p>
          </div>
          <div class="modal-footer">
            <button class="btn" data-dismiss="modal" aria-hidden="true">Close</button>
          </div>
        </div>
        <script type="text/javascript">
          var loadDetail = function(d0, d1, d2, key){
            $.ajax({
              url: "/training-set/load-detail/",
              type: "GET",
              data: {d0:d0, d1:d1, d2:d2},
              dataType: "json",
              success: function(response){
                if (response['status']=='ok'){
                  var content = '<ul>\n'
                  for (var i=0; i<response['data'].length; i++){
                    content += '<li>'
                    content += '<a href="'+response['data'][i]['url']+'">'+response['data'][i]['url']+'</a><br />'
                    content += response['data'][i]['content'] + '<br />'
                    content += '<a class="btn btn-primary" href="/teach/?site_key='+response['data'][i]['site_key']+'">TRAIN AGAIN</a>'
                    content += '</li>\n';
                  }
                  content += '</ul>'
                }
                $("#detailmodal .modal-body").html(content);
              }
            })
          }
        </script>

        %rebase layout
