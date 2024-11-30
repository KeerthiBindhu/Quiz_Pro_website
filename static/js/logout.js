function triggerProfile(){
  // document.getElementById("profileDropdown").classList.toggle("show");
    // console.log(document.getElementById("profileDropdown").classList.contains('show'));
    let profile  = document.getElementById("profileDropdown");
    if(profile.style.display === 'none')
        profile.style.display = 'flex'
    else
        profile.style.display = 'none'
    // document.getElementById("profileDropdown").style.display = 'flex'
}

// Close the dropdown if the user clicks outside of it
window.onclick = function(event) {
    if (!event.target.matches('.dropdownBtn')) {
      var dropdowns = document.getElementsByClassName("profie-content");
      var i;
      for (i = 0; i < dropdowns.length; i++) {
        var openDropdown = dropdowns[i];
        if (openDropdown.classList.contains('show')) {
          openDropdown.classList.remove('show');
        }
      }
    }
  }