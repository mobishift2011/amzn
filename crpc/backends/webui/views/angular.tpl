<!doctype html>
%LB, RB = '{{', '}}'
<html ng-app>
  <head>
        <script src="/assets/js/angular.min.js"></script>
        <script src="/assets/js/todo.js"></script>
        <link rel="stylesheet" href="/assets/css/todo.css">
  </head>
  <body>
    <h2>Todo</h2>
    <div ng-controller="TodoCtrl">
      <span>{{LB}}remaining(){{RB}} of {{LB}}todos.length{{RB}} remaining</span>
      [ <a href="" ng-click="archive()">archive</a> ]
      <ul class="unstyled">
        <li ng-repeat="todo in todos">
          <input type="checkbox" ng-model="todo.done">
          <span class="done-{{LB}}todo.done{{RB}}">{{LB}}todo.text{{RB}}</span>
        </li>
      </ul>
      <form ng-submit="addTodo()">
        <input type="text" ng-model="todoText"  size="30"
               placeholder="add new todo here">
        <input class="btn-primary" type="submit" value="add">
      </form>
    </div>
  </body>
</html>
