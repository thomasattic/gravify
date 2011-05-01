/*
					connectLink		disconnectLink	publishLink		unpublishLink	
on load				enabled			hidden			disabled 		hidden	
entered room		hidden			shown/enabled	enabled			hidden	
leave room			shown/enabled	hidden			shown/disabled	hidden	
activate camera		hidden			shown/enabled	hidden			shown/enabled	
disable camera		hidden			shown/enabled	shown/enabled	hidden	
*/

function room_loads() {
	show('connectLink');
	hide('disconnectLink');
	show_and_disable('publishLink');
	hide('unpublishLink');
}

$(document).ready(room_loads);

function room_entered() {
	hide('connectLink');
	show_and_enable('disconnectLink');
	enable('publishLink');
	hide('unpublishLink');
}

function room_left() {
	show_and_enable('connectLink');
	hide('disconnectLink');
	show_and_disable('publishLink');
	hide('unpublishLink');
}

function room_camera_on() {
	hide('connectLink');
	show_and_enable('disconnectLink');
	hide('publishLink');
	show_and_enable('unpublishLink');
}

function room_camera_off() {
	hide('connectLink');
	show_and_enable('disconnectLink');
	show_and_enable('publishLink');
	hide('unpublishLink');
}