if (typeof (VK_RED) == 'undefined') {

	var VK_RED = KeyEvent.VK_RED || 403;
	var VK_GREEN = KeyEvent.VK_GREEN || 404;
	var VK_YELLOW = KeyEvent.VK_YELLOW || 405;
	var VK_BLUE = KeyEvent.VK_BLUE || 406;

	var VK_LEFT = KeyEvent.VK_LEFT || 37;
	var VK_UP = KeyEvent.VK_UP || 38;
	var VK_RIGHT = KeyEvent.VK_RIGHT || 39;
	var VK_DOWN = KeyEvent.VK_DOWN || 40;
	var VK_ENTER = KeyEvent.VK_ENTER || 13;

	var VK_0 = KeyEvent.VK_0 || 48;
	var VK_1 = KeyEvent.VK_1 || 49;
	var VK_2 = KeyEvent.VK_2 || 50;
	var VK_3 = KeyEvent.VK_3 || 51;
	var VK_4 = KeyEvent.VK_4 || 52;
	var VK_5 = KeyEvent.VK_5 || 53;
	var VK_6 = KeyEvent.VK_6 || 54;
	var VK_7 = KeyEvent.VK_7 || 55;
	var VK_8 = KeyEvent.VK_8 || 56;
	var VK_9 = KeyEvent.VK_9 || 57;

	var VK_PLAY = KeyEvent.VK_PLAY || 415;
	var VK_PAUSE = KeyEvent.VK_PAUSE || 19;
	var VK_STOP = KeyEvent.VK_STOP || 413;
	var VK_FAST_FWD = KeyEvent.VK_FAST_FWD || 417;
	var VK_REWIND = KeyEvent.VK_REWIND || 412;

	var VK_BACK = KeyEvent.VK_BACK || 461;

	var VK_TELETEXT = KeyEvent.VK_TELETEXT || 459;
}

var player;

function initMenu() {
	player = document.getElementById("video");
    player.focus();
	
	try {
		player.onPlayStateChange=function(){
			switch (player.playState){
			case 0:
				storeOffsetAndExit();
                //window.history.back();
				break;
			case 1:
				break;
			case 2:
				break;
			case 3:
				break;
			case 4:
				break;
			case 5:
				break;
			case 6:
				break;
			}
		};
		playpause();
		
		if(player.playTime && player.playTime!='undefined'){
		}
		
		
	} catch (e) {
//		alert("not playing: " + e.toString());
	}
}

function handleNumberButtons(e) {
  switch (e.keyCode)
	{
		case VK_0:
            playpause();
			break;
		case VK_1:
			
			break;
		case VK_2:
			
			break;
		case VK_3:
			
			break;
		case VK_4:
			
			break;
		case VK_5:
			
			break;
		case VK_6:
			
			break;
		case VK_7:
			
			break;
		case VK_8:
			
			break;
		case VK_9:
			
			break;
		case VK_RED:
			
			break;
		case VK_GREEN:
			
			break;
		case VK_YELLOW:
			window.location.href=backlink;
			break;
		case VK_BLUE:
			
			break;
		case VK_PLAY:
			playpause();
			break;
		case VK_PAUSE:
			playpause();
			break;
		case VK_STOP:
			stop();
			break;
		case VK_FAST_FWD:
			player.play(4);
			break;
		case VK_REWIND:
			player.play(-4);
			break;
		case VK_BACK:
			window.location.href=backlink;
			break;
		default:
			
			break;
	}
}



function playpause(){
	if (player.playState != 1 || player.speed==4 || player.speed==-4){
		player.play(1);
	}
	else if (player.playState == 1){
		player.play(0);
	}
}

function stop(){
	player.stop();
}

function debug (debugString){
	oldText=document.getElementById('debug').innerHTML;
	document.getElementById('debug').innerHTML=oldText+"<p>"+debugString+"</p>";
}