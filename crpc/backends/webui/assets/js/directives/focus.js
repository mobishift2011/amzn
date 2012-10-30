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
