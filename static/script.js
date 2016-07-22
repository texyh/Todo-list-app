$(document).ready(function(){
	$("#main_input_box").submit(function(event){
		
		var deleteButton = "<button class='delete btn btn-warning'>Delete</button>";
		var editButton = "<button class='edit btn btn-success'>Edit</button>";
		var twoButtons = "<div class='btn-group pull-right'>" + deleteButton + editButton + "</div>";
		var checkBox = "<div class='checkbox'><label><input type='checkbox' class='pull-right'></label></div>";
		$.ajax({
			data : {
				todo : $("#custom_textbox").val()

			},
			type : 'POST',
			url : '/todo'
		})
		.done(function(data){
			if (data){
				$(".list_of_items").append("<li class='list-group-item'>" + "<div class='text_holder'>" + data.tidy + twoButtons + "</div>" + checkBox + "</li>");
				$("#custom_textbox").val('');
			}
		});
		event.preventDefault();
	});

	$(".list_of_items").on("click", "button.delete", function(){

		$(this).closest("li").remove();
	});

	$(".list_of_items").on("click", "button.edit", function (){
		var editItemBox = "<form class='edit_input_box'><input type='text' class='itembox'></form>";
		var originalItem = $(this).parent().val();
		var deleteButton = "<button class='delete btn btn-warning'>Delete</button>";
		var editButton = "<button class='edit btn btn-success'>Edit</button>";
		var twoButtons = "<div class='btn-group pull-right'>" + deleteButton + editButton + "</div>";
		$(this).closest("div.text_holder").replaceWith(editItemBox);
		$("form.edit_input_box ").on("submit", function(){
			event.preventDefault(); 
			var checkBox = "<label><input type='checkbox'></label>";
			$(this).replaceWith("<div>" + $(".itembox").val() + twoButtons + "</div>");
		}); 
	});
	
	$(".list_of_items").on("click", ":checkbox", function (){
		$(this).closest("li").toggleClass("completed_item");
	});
});



