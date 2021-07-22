function accordion(id) {
	var x = document.getElementById(id);
	if (x.className.indexOf("show") == -1) {
		x.className += " show";
	} else {
		x.className = x.className.replace(" show", "")
	}
}

var acc = document.getElementByClassName("accordion");
var i;

for (i=0; i < acc.length; i++){
	acc[i].addEventListener("click", function() {
		this.classList.toggle("active");
		var panel = this.nextElementSibling;
		if(panel.style.display === "block") {
			panel.style.display = "none";
		} else {
			panel.style.display = "block";
			
		}
	});
}