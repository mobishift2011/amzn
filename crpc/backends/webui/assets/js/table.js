function TableCtrl($scope) {
  $scope.tasks = [
    {name:'task1', time:'2012-10-11 04:00:30', dones:0, updates:0, news:0, fails:0},
    {name:'task2', time:'2012-10-11 05:00:30', dones:0, updates:0, news:0, fails:0},
    {name:'task3', time:'2012-10-11 06:00:30', dones:0, updates:0, news:0, fails:0},
    {name:'task4', time:'2012-10-11 07:00:30', dones:0, updates:0, news:0, fails:0},
    {name:'task5', time:'2012-10-11 08:00:30', dones:0, updates:0, news:0, fails:0},
    {name:'task6', time:'2012-10-11 09:00:30', dones:0, updates:0, news:0, fails:0},
    {name:'task7', time:'2012-10-11 10:00:30', dones:0, updates:0, news:0, fails:0},
    {name:'task8', time:'2012-10-11 11:00:30', dones:0, updates:0, news:0, fails:0},
    {name:'task9', time:'2012-10-11 12:00:30', dones:0, updates:0, news:0, fails:0},
    {name:'taska', time:'2012-10-11 13:00:30', dones:0, updates:0, news:0, fails:0},
    {name:'taskb', time:'2012-10-11 14:00:30', dones:0, updates:0, news:0, fails:0},
    {name:'taskc', time:'2012-10-11 15:00:30', dones:0, updates:0, news:0, fails:0},
    {name:'taskd', time:'2012-10-11 16:00:30', dones:0, updates:0, news:0, fails:0},
  ]

$(document).ready(function(){
    if (!window.console) window.console = {};
    if (!window.console.log) window.console.log = function() {};

    updater.poll();
});

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

var updater = {
    errorSleepTime: 500,
    cursor: null,

    poll: function() {
        var args = {"_xsrf": getCookie("_xsrf")};
        if (updater.cursor) args.cursor = updater.cursor;
        $.ajax({
            timeout: 16000,
            url: "/table/all", 
            type: "GET", 
            dataType: "text",
            data: $.param(args), 
            success: updater.onSuccess,
            error: updater.onError
        });
    },

    onSuccess: function(response) {
        try {
            console.log(response);
            $scope.$apply(function(){
                for(var i=0; i<$scope.tasks.length; i++){
                    if (Math.round(Math.random()*$scope.tasks.length)==i){
                        var task = $scope.tasks[i];
                        task.dones++;
                        if (Math.random()<0.9){
                            task.updates++;
                        }else{
                            task.news++;
                        }   
                    }
                }
            })
        } catch (e) {
            updater.onError();
            return;
        }
        updater.errorSleepTime = 500;
        window.setTimeout(updater.poll, 3000);
    },

    onError: function(response) {
        updater.errorSleepTime *= 2;
        console.log("Poll error; sleeping for", updater.errorSleepTime, "ms");
        window.setTimeout(updater.poll, updater.errorSleepTime);
    },
};

}
