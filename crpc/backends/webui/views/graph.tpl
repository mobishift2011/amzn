%include header title="Graphs", description="", author="", scripts=["/assets/js/controllers/tasks.js","/assets/js/controllers/DT_bootstrap.js"], csses=["/assets/css/DT_bootstrap.css"]

% LB, RB = '{{', '}}'

  <body>

    %include navigation

    <div class="container">

      <h1>monitor, control</h1>
        
      <ul class="nav nav-pills">
        <li><a href="/task">Tasks</a></li>
        <li><a href="/control">Control</a></li>
        <li><a href="/publish">Publish</a></li>
        <li><a href="/history">History</a></li>
        <li class="active"><a href="/graph">Graph</a></li>
      </ul>

	<div class="btn-group" data-toggle="buttons-radio">
	  <button type="button" class="btn btn-primary active" id="beyondtherack">beyondtherack</button>
	  <button type="button" class="btn btn-primary" id="bluefly">bluefly</button>
	  <button type="button" class="btn btn-primary" id="gilt">gilt</button>
	  <button type="button" class="btn btn-primary" id="hautelook">hautelook</button>
	  <button type="button" class="btn btn-primary" id="ideeli">ideeli</button>
	  <button type="button" class="btn btn-primary" id="myhabit">myhabit</button>
	  <button type="button" class="btn btn-primary" id="nomorerack">nomorerack</button>
	  <button type="button" class="btn btn-primary" id="onekingslane">onekingslane</button>	
	  <button type="button" class="btn btn-primary" id="ruelala">ruelala</button>
	  <button type="button" class="btn btn-primary" id="zulily">zulily</button>
	</div>
	
      <div class="container" style="margin-top: 10px" >  
	<h3>Events History</h3>
	   <div id="graphevent"></div>
	<h3>Product History</h3>
	   <div id="graphproduct"></div>
      </div>
    </div> <!-- /container -->

    <!-- Le javascript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
	<script type="text/javascript" src="/assets/js/libs/highstock.js"></script>
	<script type="text/javascript" src="/assets/js/libs/gray.js"></script>
	<script type="text/javascript">
	theme = 'gray';
	$(function(){
	    Highcharts.setOptions({
	        global:{
	            useUTC:true
	        }
	        });
	    var yAxisOptions = [],
	    seriesCounter = 0,
	    colors = Highcharts.getOptions().colors;
		plot('beyondtherack');
		
		function plot(site) {
			$.getJSON('/graph/event/'+site, function(data) {
			 	createChart('graphevent',data)
			})
			$.getJSON('/graph/product/'+site, function(data) {
			 	createChart('graphproduct',data)
			})
		};

  	    function createChart(render_id, seriesopt){
	        var chart = new Highcharts.StockChart({
	            chart:{renderTo:render_id},
	            rangeSelector:{
	                selected:4,
	                buttons: [{
	                        type: 'minute',
	                        count: 10,
	                        text:'10m'
	                    }, {
	                        type: 'minute',
	                        count: 120,
	                        text: '1h'
	                    }, {
	                        type: 'day',
	                        count: 1,
	                        text: '1d'
	                    }, {
	                        type: 'week',
	                        count: 1,
	                        text: '1w'
	                    }, {
	                        type: 'all',
	                        text: 'All'
	                    }]
	            },
	            yAxis:{
	                labels:{
	                    formatter:function(){
	                        return this.value;
	                    }
	                    },
	                plotLines:[{
	                    value:0,
	                    width:1,
	                    color:'silver'
	                }]
	            },
	            tooltip:{
	                pointFormat:'<span style="color:{series.color}">{series.name}</span>: <b>{point.y}</b><br/>',
	                yDecimals:0
	            },
	            series:seriesopt
	        });
	    };
	
	$("#beyondtherack").on("click", function() { plot('beyondtherack'); });
	$("#bluefly").on("click", function() { plot('bluefly'); });
	$("#gilt").on("click", function() { plot('gilt'); });
	$("#hautelook").on("click", function() { plot('hautelook'); });
	$("#myhabit").on("click", function() { plot('myhabit'); });
	$("#nomorerack").on("click", function() { plot('nomorerack'); });
	$("#onekingslane").on("click", function() { plot('onekingslane'); });
	$("#ruelala").on("click", function() { plot('ruelala'); });
	$("#zulily").on("click", function() { plot('zulily'); });
	
	});
	</script>
  </body>
</html>

