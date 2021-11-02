document.addEventListener("DOMContentLoaded", function () {

   function check_active_url(i) {
     let path = window.location.pathname;
     let menu_path = i.dataset.path;
     if ( path.toLowerCase() == menu_path.toLowerCase()) {
       i.className = "side_menu side_menu_active";
     }
   }

    let side_menu = document.querySelectorAll(".side_menu");
    side_menu.forEach( i => {
      check_active_url(i)
    })


    let side_bar = document.querySelector('.left_sidebar');



// MENU
  function toggleMenu() {
    var sideBar = document.querySelector(".left_sidebar");
    if (sideBar.style.display === "none") {
      sideBar.style.display = "block";
    } else {
      sideBar.style.display = "none";
    }
  }

  if (screen.availWidth < 990) {
      toggleMenu();
  }

  document.querySelector("#icon_menu_icon").addEventListener('click', () => {
    toggleMenu()
  })


});
