var addTaskButton = document.getElementById("add_task");
var removeTaskButton = document.getElementById("remove_task");
var taskTemplate = document.getElementsByClassName("task")[0].innerHTML;
var taskContainer = document.getElementById("task_container");
var budgetInput = document.getElementById('budget_input');

addTaskButton.onclick = function(){
  var newTask = document.createElement("div");
  newTask.class = "task";
  newTask.innerHTML = taskTemplate;
  taskContainer.appendChild(newTask);
};

removeTaskButton.onclick = function(){
  var taskChilds = taskContainer.childElementCount;
  if (taskChilds == 1){
    alert("A project needs a minimum of 1 task");
  }else{
    taskContainer.removeChild(taskContainer.lastChild);
  }


};

// Listen for input event on numInput.
budgetInput.onkeypress = function(e) {
    if(!((e.keyCode > 95 && e.keyCode < 106)
      || (e.keyCode > 47 && e.keyCode < 58)
      || e.keyCode == 8)) {
        return false;
    }
}
