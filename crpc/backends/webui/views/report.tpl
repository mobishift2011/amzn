<html>
  <head>
  </head>
  <body>
    <form method="POST">
      <input type="date" name="date">
      <input type="submit" value="GO">
    </form>
    <div>

      <table class='table table-striped'>
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
            <td>{{prd['product_num']}}</td>
            <td>{{prd['published_num']}}</td>
            <td>{{prd['no_image_url_num']}}</td>
            <td>{{prd['no_image_path_num']}}</td>
            <td>{{prd['no_dept_num']}}</td>
            <td>{{prd['event_not_ready']}}</td>
            <td>{{prd['unknown']}}</td>
          </tr>
          % end
        </tbody>
      </table>

      <table class='table table-striped'>
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
  </body>
</html>
