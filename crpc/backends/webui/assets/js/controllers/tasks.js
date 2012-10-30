
/*
 *   Angular Scripts and Controllers
 */

function TaskCtrl($scope) {
  $scope.tasks = [
  ];

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
            url: "/table/all",
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
            url: "/table/update", 
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
            updater.updateTasks(tasks);
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
            return [t.name, t.status, t.started_at, t.updated_at, t.dones, t.updates, t.news, t.fails];
        }

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
                    $.fn.oTable.fnAddData(row);
                }
            }
        })

        $.fn.oTable.fnDraw();
    },
  }; /* Updater */
} /* TaskCtrl */
