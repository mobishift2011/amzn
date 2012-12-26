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
              <li><a href="/event/list/">Events</a></li>
              <li class="nav-header">Test</li>
              <li><a href="/cross-validation/">Cross Validation</a></li>
            </ul>
          </div><!--/.well -->
        </div><!--/span-->
        <div class="span9 row-fluid">
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
          <div class="row span9">
            <div id="d0" class="well row">
            %for name in d0:
              <a class="btn" style="margin:2px;" name="d0" d0="{{name}}">{{name}}</a>
            %end
            </div>
            <div id="d1" class="well row">
            %for name in d1:
              <a class="btn" style="margin:2px;" name="d1" d1="{{name}}">{{name}}</a>
            %end
            </div>
            <div id="d2" class="well row">
              Please Choose D1 First!
            </div>
            <div class="row">
              <h3><a href="#" id="teach" class="btn disabled">Teach Another</a></h3>
            </div>
          </div>

        </div><!--/span-->

        <script>
          var d2dict = {{!d2dict_json}};
          var d0 = "";
          var d1 = "";
          var d2 = "";
          $("#d2").hide();
          $("a[name=d0]").live('click', function(){
            d0 = $(this).attr('d0');
            $("a[name=d0]").removeClass('btn-primary');
            $(this).addClass('btn-primary');
          });
          $("a[name=d1]").live('click', function(){
            d1 = $(this).attr('d1');
            $("a[name=d1]").removeClass('btn-primary');
            $(this).addClass('btn-primary');
            var html = "";
            var sublist = d2dict[d1];
            if (sublist){
                for (var i=0; i<sublist.length; i++){
                    html += "<a class='btn' style='margin:2px;' name='d2' d2=\""+sublist[i]+"\">"+sublist[i]+"</a>"
                }
                $('#d2').html(html);
                $('#d2').show();
                $('#teach').addClass('disabled').removeClass('btn-primary');
            }else{
                $('#d2').hide();
                d2 = "";
                if (d0 && d1){
                    $('#teach').addClass('btn-primary').removeClass('disabled');
                }
            }
          })
          $("a[name=d2]").live('click', function(){
            d2 = $(this).attr('d2');
            $("a[name=d2]").removeClass('btn-primary');
            $(this).addClass('btn-primary');
            if (d0){
                $('#teach').addClass('btn-primary').removeClass('disabled');
            }
          })
          $('#teach').live('click', function(){
            var content = $('#content').html().replace(/<br[^>]*>/, '');
            $.ajax({
              url: "/teach/train/",
              type: "POST",
              data: {d0:d0, d1:d1, d2:d2, content:content, site_key:'{{site_key}}'},
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
