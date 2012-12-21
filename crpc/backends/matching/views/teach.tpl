        <div class="span3">
          <h2>Menu</h2>
          <div class="well sidebar-nav">
            <ul class="nav nav-list">
              <li class="nav-header">View</li>
              <li><a href="/department/">Departments</a></li>
              <li><a href="/training-set/">Training Sets</a></li>
              <li class="nav-header">Train</li>
              <li class="active"><a href="/teach/">Teach</a></li>
              <li><a href="/validate/">Validate</a></li>
              <li class="nav-header">Test</li>
              <li><a href="/cross-validation/">Cross Validation</a></li>
            </ul>
          </div><!--/.well -->
        </div><!--/span-->
        <div class="span9 row-fluidi">
          <h2>Thank you for sharing knowledge with me!</h2>
          <h3>Here's some text from my database:</h3>
          <div class="well">
            <p id="content">
            {{!content}}
            </p>
            <p id="images">
            %for url in image_urls[:3]:
              <img src="{{!url}}" width="300px"/>
            %end
            </p>
          </div>
          <br />
          <h3>It belongs to...</h3>
          <div>
            <div id="main" class="well span5">
            %for dept in departments.keys():
              <a class="btn" style="margin:2px;" name="main" main="{{dept}}">{{dept}}</a>
            %end
            </div>
            <div id="sub" class="well span7">
              Please Choose Main Department First!
            </div>
          </div>
          <br />
          <br />
          <br />
          <br />
          <br />
          <br />
          <br />
          <br />
          <h3><a href="#" id="teach" class="btn disabled">Teach Another</a></h3>

        </div><!--/span-->

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
              url: "/teach/train/",
              type: "POST",
              data: {main:main, sub:sub, content:content, site_key:'{{site_key}}'},
              dataType: "json",
              success: function(response){
                //console.log(response);
                if (response.status == 'ok'){
                  window.location.href = "/teach/"; 
                }
              }
            })
          })
        </script>

        %rebase layout
