document.addEventListener("DOMContentLoaded", function () {

    fetch('/api/get_client')
    .then(response => response.json())
    .then(data =>  get_details(data) );


function get_details(data){
  if (data['status'] != "no user") {
    get_cart(data['id'])
  }
}

function get_cart(client_id) {
  fetch(`/api/get_cart/${client_id}`)
  .then(response => response.json())
  .then(data =>  update_cart(data) );
}

function update_cart(data){
  if (data['status'] != "no cart") {
    let cart_icon = document.querySelector('#cart_header');
    cart_icon.innerHTML = `    ${data['products'].length}`;

  }
}

});
