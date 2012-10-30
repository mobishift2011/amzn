var monitor = angular.module('monitor', []);
    
if (!window.console) window.console = {};
if (!window.console.log) window.console.log = function() {};

function ScheduleCtrl($scope) {
  	$scope.schedules = [
  	];

  	$scope.initSchedules = function(){
  		$.ajax({
  			url: '/control/all',
  			type: 'GET',
  			dataType: 'json',
  			success: function(response){
  				$scope.$apply(function(){
  					$scope.schedules = [];
	  				var schedules = response['schedules'];
	  				for (var i=0; i<schedules.length; i++){
	  					$scope.schedules.push(schedules[i]);
	  				}
  				})
  			}
  		})
  	}

  	// initializing
  	$scope.initSchedules();

  	$scope.editedSchedule1 = null;
  	$scope.editedSchedule2 = null;
  	$scope.editedSchedule3 = null;
	$scope.oldcron = null;
	$scope.newSchedule = {};  	

  	$scope.editSchedule1 = function(schedule){
  		$scope.editedSchedule1 = schedule;
  	};

  	$scope.doneEditing1 = function( schedule ) {
    	if ( !schedule.name ) {
      		$scope.removeSchedule(schedule);
    	}else{
    		$scope.saveSchedule(schedule);
    	}
    	$scope.editedSchedule1 = null;
  	};

  	$scope.editSchedule2 = function(schedule){
  		$scope.editedSchedule2 = schedule;
  	};

  	$scope.doneEditing2 = function(schedule) {
       	if ( !schedule.description ) {
      		$scope.removeSchedule(schedule);
    	}else{
    		$scope.saveSchedule(schedule);
    	}
    	$scope.editedSchedule2 = null;
  	}

  	$scope.editSchedule3 = function(schedule){
  		$scope.oldcron = schedule.crontab_arguments;
  		$scope.editedSchedule3 = schedule;
  	};

  	$scope.doneEditing3 = function(schedule) {
       	if ( !schedule.crontab_arguments ) {
      		$scope.removeSchedule(schedule);
    	}else{
    		$scope.saveSchedule(schedule, $scope.oldcron);
    	}
    	$scope.editedSchedule3 = null;
  	}

  	$scope.editSchedule4 = function(schedule){
  		schedule.enabled = !schedule.enabled;
  		$scope.saveSchedule(schedule);
  	};


  	$scope.removeSchedule = function( schedule ) {
  		$.ajax({
  			url: '/control/del',
  			type: 'POST',
  			contentType: "application/json; charset=utf-8",
  			data: JSON.stringify(schedule),
  			success: function(response){
  				console.log(response);
  			}
  		});
    	$scope.schedules.splice($scope.schedules.indexOf(schedule), 1);
  	};

  	$scope.saveSchedule = function(schedule, oldcron) {
  		$.ajax({
  			url: '/control/save',
  			type: 'POST',
  			contentType: "application/json; charset=utf-8",
  			data: JSON.stringify(schedule),
  			success: function(response){
  				// restore crontab argument if error occured
  				if (response['status'] == 'error' && oldcron){
  					$scope.$apply(function(){
  						schedule.crontab_arguments = oldcron;
  					})
  				}
  				if (response['pk']){
  					$scope.$apply(function(){
  						schedule.pk = response['pk'];
  					});
  				}

  				console.log(response['status'], response['reason']);
  			},
  			error: function(response){
  				console.log(response['status'], response['reason']);
  			}
  		});
  	}

  	$scope.addSchedule = function() {
  		console.log($scope.newSchedule);
  		var s = {
  				'name': $scope.newSchedule.name,
  				'description': $scope.newSchedule.description,
  				'crontab_arguments': $scope.newSchedule.cron,
  				'enabled': false
  		}
		$scope.schedules.push(s);
  		$scope.saveSchedule(s);
  	}
}

monitor.directive('ctrlFocus', function( $timeout ) {
  return function( scope, elem, attrs ) {
    scope.$watch(attrs.ctrlFocus, function( newval ) {
      if ( newval ) {
        $timeout(function() {
          elem[0].focus();
        }, 0, false);
      }
    });
  };
});

monitor.directive('ctrlBlur', function() {
  return function( scope, elem, attrs ) {
    elem.bind('blur', function() {
      scope.$apply(attrs.ctrlBlur);
    });
  };
});
