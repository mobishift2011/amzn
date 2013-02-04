%include header title="Publish Report", description="", author="", scripts=["/assets/js/controllers/DT_bootstrap.js"], csses=["/assets/css/DT_bootstrap.css"]

<html>
  <head>
  </head>
  <body>
    <form action="/publish/report" method="POST">
      <input type="date" name="date">
      <input type="submit" value="GO">
    </form>
    <div>

      <table cellpadding='0' cellspacing='0' border='0' class='table table-striped table-bordered'>
        <thead>
          <tr>
            <th>Site</th>
            <th>Product</th>
            <th>Published product</th>
            <th>No image url</th>
            <th>No image path</th>
            <th>No dept</th>
            <th>Event not ready</th>
            <th>Unknown</th>
          </tr>
        </thead>

        <tbody>
          % for prd in product:
          <tr>
            <td>{{prd['site']}}</td>
            <td class='product_num'>{{prd['product_num']}}</td>
            <td class='published_num'>{{prd['published_num']}}</td>
            <td class='no_image_url_num'>{{prd['no_image_url_num']}}</td>
            <td class='no_image_path_num'>{{prd['no_image_path_num']}}</td>
            <td class='no_dept_num'>{{prd['no_dept_num']}}</td>
            <td class='event_not_ready'>{{prd['event_not_ready']}}</td>
            <td class='unknown'>{{prd['unknown']}}</td>
          </tr>
          % end
          <tr>
            <td>Total</td>
            <td id='total_product_num'></td>
            <td id='total_published_num'></td>
            <td id='total_no_image_url_num'></td>
            <td id='total_no_image_path_num'></td>
            <td id='total_no_dept_num'></td>
            <td id='total_event_not_ready'></td>
            <td id='total_unknown'></td>
          </tr>
        </tbody>
      </table>

      <table cellpadding='0' cellspacing='0' border='0' class='table table-striped table-bordered'>
        <thead>
          <tr>
            <th>Site</th>
            <th>Event</th>
            <th>Published event</th>
            <th>Not leaf event</th>
            <th>Upcoming no image url</th>
            <th>Upcoming no image path</th>
            <th>Onsale no product</th>
            <th>Onsale no image url</th>
            <th>Onsale no image path</th>
            <th>Propagation not complete</th>
            <th>Unknown</th>
          </tr>
        </thead>

        <tbody>
          % for ev in event:
          <tr>
            <td>{{ev['site']}}</td>
            <td>{{ev['event_num']}}</td>
            <td>{{ev['published_num']}}</td>
            <td>{{ev['not_leaf_num']}}</td>
            <td>{{ev['upcoming_no_image_url_num']}}</td>
            <td>{{ev['upcoming_no_image_path_num']}}</td>
            <td>{{ev['onsale_no_product_num']}}</td>
            <td>{{ev['onsale_no_image_url_num']}}</td>
            <td>{{ev['onsale_no_image_path_num']}}</td>
            <td>{{ev['onsale_propagation_not_complete']}}</td>
            <td>{{ev['unknown']}}</td>
          </tr>
          % end
        </tbody>
      </table>

    </div>
    <script type="text/javascript">
      $(function(){
        var fields = ['product_num', 'published_num', 'no_image_url_num', 'no_image_path_num', 'no_dept_num', 'event_not_ready', 'unknown']
        for(var i in fields){
          var node = 'td.' + fields[i];
          var total_node = '#total_' + fields[i];
          var total = 0;
          var products = $(node);
          for(var j in products){
            var value = parseInt(products[j].innerText);
            if(value){
              total += value
            }
          }

          $(total_node).append(total);
        }
      })
    </script>
  </body>
</html>
