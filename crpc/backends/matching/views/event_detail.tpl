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
            <div id="main" class="well span5">
            %for dept in departments.keys():
              <a class="btn" style="margin:2px;" name="main" main="{{dept}}">{{dept}}</a>
            %end
            </div>
            <div id="sub" class="well span7">
              Please Choose Main Department First!
            </div>
          </div>
          <div><a href="#" id="teach" class="btn">Train!!</a></div>
        </div>

        <script>
          var departments_object = {{!departments_object}};
          var main = "";
          var sub = "";
          $("a[name=main]").live('click', function(){
            main = $(this).attr('main');
            $("a[name=main]").removeClass('btn-primary');
            $(this).addClass('btn-primary');
            var html = "";
            var sublist = departments_object[main];
            for (var i=0; i<sublist.length; i++){
              html += "<a class='btn' style='margin:2px;' name='sub' sub=\""+sublist[i]+"\">"+sublist[i]+"</a>"
            }
            $('#sub').html(html);
            $('#teach').addClass('disabled').removeClass('btn-primary');
          })
          $("a[name=sub]").live('click', function(){
            sub = $(this).attr('sub');
            $("a[name=sub]").removeClass('btn-primary');
            $(this).addClass('btn-primary');
            $('#teach').addClass('btn-primary').removeClass('disabled');
          })
          $('#teach').live('click', function(){
            var content = $('#content').text();
            $.ajax({
              url: "/event/train/",
              type: "POST",
              data: {main:main, sub:sub, site:'{{site}}', key:'{{key}}'},
              dataType: "json",
              success: function(response){
                console.log(response);
                if (response.status == 'ok'){
                }
              }
            })
          })
        </script>

        %rebase layout
