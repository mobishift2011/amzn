
/*
 *   Angular Scripts and Controllers
 */

function TaskCtrl($scope) {
  $scope.tasks = [];

  $(document).ready(function(){
    updater.init();
    updater.poll();
  });

  function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
  }

  var updater = {
    errorSleepTime: 500,

    // initiate table arguments
    init: function() {
        $.ajax({
            url: "/task/all",
            type: "GET",
            dataType: "json",
            success: function(response){
                updater.updateTasks(response['tasks']);
            }
        });
    },

    poll: function() {
        $.ajax({
            timeout: 16000,
            url: "/task/update", 
            type: "GET", 
            dataType: "json",
            success: updater.onSuccess,
            error: updater.onError
        });
    },

    onSuccess: function(response) {
        try {
            console.log(response);
            var tasks = response['tasks'];
            // we will block updates if we are viewing fails
            // canUpdate is a global variable (I apologize for that)
            if (tasks!=[] && canUpdate){
                updater.updateTasks(tasks);
            }
        } catch (e) {
            updater.onError();
            return;
        }
        updater.errorSleepTime = 500;
        window.setTimeout(updater.poll, 100);
    },

    onError: function(response) {
        updater.errorSleepTime *= 2;
        console.log("Poll error; sleeping for", updater.errorSleepTime, "ms");
        window.setTimeout(updater.poll, updater.errorSleepTime);
    },


    updateTasks: function(tasks) {
        var task2row = function(t) {
            $scope.tasks.push(t);
            // modal for errors
            var taskid = t.updated_at.replace(/:/g,'').replace(/\./g,'').replace(/-/g,'');
            var tabletrs = "";
            
            var failsdiv = "<div id='"+taskid+"'class='modal hide fade' role='dialog' style='display:none;'>"+
                        "<div class='modal-header'><button type='button' class='close' data-dismiss='modal' aria-hidden='true' onclick='toggleCanUpdate()'>x</button><h3>Fails</h3></div>" +
                        "<div class='modal-body'>"+
                            "<table class='table table-striped'>"+
                                "<thead><tr><th>Time</th><th>Caller</th><th>Message</th></tr></thead>"+
                                "<tbody>"+tabletrs+"</tbody>"+
                            "</table>"+
                        "</div>"+
                        "<div class='modal-footer'><p id="+t.ctx+" onclick='showFails(this)'><button class='btn' data-dismiss='modal' onclick='toggleCanUpdate()'>Close</button></p></div>"+
                    "</div>"
                    + "<div><a href='#"+taskid+"' data-toggle='modal' onclick='toggleCanUpdate()'>"+t.fails+"</div>";
            return [t.name, t.status, t.started_at, t.updated_at, t.dones, t.updates, t.news, failsdiv];
        }

        var rows_to_add = [];

        $scope.$apply(function(){
            for(var i=0; i<tasks.length; i++){
                var found = false;
                for(var j=0; j<$scope.tasks.length; j++){
                    if( $scope.tasks[j].started_at == tasks[i].started_at ){
                        // alter what we binded
                        for (key in $scope.tasks[j]){
                            $scope.tasks[j][key] = tasks[i][key];
                        }

                        // alter values in datatable
                        for (var k=0; k<$scope.tasks.length; k++){
                            var therow = $.fn.oTable.fnGetData(k);
                            if (therow && therow[2] == tasks[i].started_at){
                                $.fn.oTable.fnUpdate(task2row(tasks[i]), k);
                            }
                        }
                        
                        found = true;
                        break;
                    }
                }

                if (!found){
                    var row = task2row(tasks[i]);
                    rows_to_add.push(row);
                }
            }
        })

        $.fn.oTable.fnAddData(rows_to_add);
        //$.fn.oTable.fnDraw();
    },
  }; /* Updater */
} /* TaskCtrl */


// dirty works
var canUpdate = true;
var toggleCanUpdate = function(){
    canUpdate = !canUpdate;
}

var showFails = function(p){
	var url = '/task/'+p.getAttribute('id')+'/fails';
    $.get(url, function(data){
    	var node = p.parentNode.previousSibling.firstChild.lastChild;
    	tabletrs = '';
        for (var i=0; i<data.fails.length; i++){
            tabletrs += "<tr><td>"+data.fails[i].time+"</td>"+
                            "<td>"+data.fails[i].name+"</td>"+
                            "<td>"+data.fails[i].message.replace(/\n/g,'<br/>').replace(/ /g,'&nbsp;')+"</td></tr>";
        }
        node.innerHTML = tabletrs;
    });
};
