 $(document).ready(function() {
	var count = -1; // turn count
	var active = 0; //deck number
	var max = 39; // max cards
	var min = 0; // min card
	var range = 0; // base number
	var order;
	var imgFolder = "originalCard/";
	var deck = "";
	shuffle();

function shuffle() {
		 var u = false; //unique val check bol
		 order = new Array(max);	
		 for(var i = 0; i < max; i++)
			{
				while(u == false)
				{
				var rand = Math.floor(Math.random() * max) +  1;
				order[i] = rand + range; 
				u = true;
				 for(var j = 0; j < i; j++)
					if (order[i] == order[j])
						u = false;
				}
				u = false;
			}
		count = -1;
		$("#card").attr("src", "planeback.jpg");
		$("#text").text("Click the card to Land Shift!");
}
function startCard() {
		active = 0;
		next();
	/*	active = active + 1;
		newCard = imgFolder +  order[active] + ".jpg";
		$("#buffer").attr("src", newCard);
		count = count + 1;
				$("#card").attr("src", "#buffer");
				$("#buffer").attr("src", newCard); */
				count = count + 1;
		var message = "Click the card to roll!";
		$("#text").text(message);
}
function next(){
			var newCard = imgFolder +  order[active] + ".jpg";
			if (active == max)
			active = 0;
			else
			active = active + 1;
			$("#card").attr("src", newCard);
}
});