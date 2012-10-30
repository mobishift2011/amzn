
monitor.directive('ctrlBlur', function() {
  return function( scope, elem, attrs ) {
    elem.bind('blur', function() {
      scope.$apply(attrs.ctrlBlur);
    });
  };
});