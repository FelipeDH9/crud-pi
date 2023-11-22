// iniciar tooltips
const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))



// filter
function filter(input_id, n, type) {
    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById(input_id);
    filter = input.value.toUpperCase();
    table = document.getElementById(type);
    tr = table.getElementsByTagName("tr");
  
    for (i = 0; i < tr.length; i++) {
      td = tr[i].getElementsByTagName("td")[n];
      if (td) {
        txtValue = td.textContent || td.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
          tr[i].style.display = "";
        } else {
          tr[i].style.display = "none";
        }
      }
    }
}



// dialog modal for delete confirmation
const open_buttons = document.querySelectorAll("button.delete");
const modal = document.querySelector('dialog');
const modal_id = document.getElementById("modal_id");

const close = document.getElementById("close");

open_buttons.forEach((button)=>{
  button.addEventListener('click', ()=> {
    // get button value with button.value
    const product_id = button.value;
    // update the value of the input in dialog to product id
    modal_id.value = product_id;
    modal.showModal();
  })
});


close.onclick = function(){
  modal.close();
  modal_id.value = 0;
};