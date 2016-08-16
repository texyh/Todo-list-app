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
				$(".list_of_items").prepend("<li class='list-group-item'>" + "<div class='text_holder'>" + data.tidy + twoButtons + "</div>" + checkBox + "</li>");
				$("#custom_textbox").val('');
			}
		});
		event.preventDefault();
	});

	$(".list_of_items").on("click", "button.delete", function(){
		var dele = this.value
		$.ajax({
			data : {
				del:dele
			},
			type:'POST',
			url:'/delete'
		})
		.done(function(data){
			if (data){
				$(this).closest("li").remove();
			}
			

		})	
	});

	$(".list_of_items").on("click", "button.edit", function (){
		var id_button = this.value
		var editItemBox = "<form class='edit_input_box'><input type='text' class='itembox'><button class='btn btn-primary'>Update</button></form>";
		var originalItem = $(this).parent().val();
		var deleteButton = "<button class='delete btn btn-warning'>Delete</button>";
		var editButton = "<button class='edit btn btn-success'>Edit</button>";
		var twoButtons = "<div class='btn-group pull-right'>" + deleteButton + editButton + "</div>";
		var checkBox = "<div class='checkbox'><label><input type='checkbox' class='pull-right'></label></div>";
		
		$(this).closest("div.text_holder").replaceWith(editItemBox);
		$("form.edit_input_box ").submit(function(){
			$.ajax({
			data : {
				edit : $(".itembox").val(),
				id : id_button
			},
			type : 'POST',
			url : '/edit'
		})
		.done(function(data){
			if (data){
				$(this).closest(editItemBox).replaceWith("<div>" + data.edited + twoButtons + "</div>"+ checkBox);
			}

		});

		event.preventDefault(); 
		}); 
	});
	
	$(".list_of_items").on("click", ":checkbox", function (){
		$(this).closest("li").toggleClass("completed_item");
	});
});



