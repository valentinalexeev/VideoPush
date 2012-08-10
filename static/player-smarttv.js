var Player =
{
    plugin : null,
    state : -1,
    originalSource : null,

    STOPPED : 0,
    PLAYING : 1,
    PAUSED : 2,  
}

Player.init = function()
{
	var success = true;
    this.state = this.STOPPED;
    
    this.plugin = document.getElementById("pluginPlayer");
    
    if (!this.plugin)
    {
         success = false;
    }
    
    this.setFullscreen();
    
    return success;
}




Player.deinit = function()
{
      alert("Player deinit !!! " );       
      
      if (this.plugin)
      {
            this.plugin.Stop();
      }
}

Player.setFullscreen = function()
{
    this.plugin.SetDisplayArea(0, 0, 960, 540);
}

Player.setWindow = function()
{
    this.plugin.SetDisplayArea(458, 58, 472, 270);
}

Player.setVideoURL = function(url)
{
    this.url = url;
}

Player.pauseVideo = function()
{
    this.state = this.PAUSED;
    this.plugin.Pause();
    alert("Paused...");
}

Player.stopVideo = function() {
    if (this.state != this.STOPPED) {
        this.state = this.STOPPED;
        this.plugin.Stop();
    }
    else
    {
        alert("Ignoring stop request, not in correct state");
    }
}

Player.resumeVideo = function() {
    this.state = this.PLAYING;
    this.plugin.Resume();
}

Player.skipForwardVideo = function()
{
    this.plugin.JumpForward(5);
}

Player.skipBackwardVideo = function()
{
    this.plugin.JumpBackward(5);
}

Player.getState = function()
{
    return this.state;
}

Player.playVideo = function()
{
    if (this.url == null)
    {
        alert("No videos to play");
    }
    else
    {
        this.state = this.PLAYING;
        this.plugin.Play( this.url );
        alert("Playing...");
    }
}

// Global functions called directly by the player 
startDrawLoading = function() { alert("startDrawLoading"); }

endDrawLoading = function() { alert("endDrawLoading"); }

getBandwidth = function(bandwidth) { alert("getBandwidth " + bandwidth); }

onDecoderReady = function() { alert("onDecoderReady"); }

onRenderError = function() { alert("onRenderError"); }

popupNetworkErr = function() { alert("popupNetworkErr"); }

setCurTime = function(time) { alert("setCurTime " + time); }

setTottalTime = function(time) { alert("setTottalTime " + time); }

stopPlayer = function() { alert("stopPlayer"); }

setTottalBuffer = function(buffer) { alert("setTottalBuffer " + buffer); }

setCurBuffer = function(buffer) { alert("setCurBuffer " + buffer); }

onServerError = function() { alert("onServerError"); }

Add the following code to Player.init().
    this.plugin.OnCurrentPlayTime = 'Player.setCurTime';
    this.plugin.OnStreamInfoReady = 'Player.setTotalTime';
    this.plugin.OnBufferingStart = 'Player.onBufferingStart';
    this.plugin.OnBufferingProgress = 'Player.onBufferingProgress';
    this.plugin.OnBufferingComplete = 'Player.onBufferingComplete';           

Player.onBufferingStart = function()
{
}

Player.onBufferingProgress = function(percent)
{
}

Player.onBufferingComplete = function()
{
}

Player.setCurTime = function(time)
{
}

Player.setTotalTime = function()
{
}

onServerError = function()
{
}

onNetworkDisconnected = function()
{
}

getBandwidth = function(bandwidth) { }

onDecoderReady = function() {  }

onRenderError = function() { }

stopPlayer = function()
{
    Player.stopVideo();
}

setTottalBuffer = function(buffer) { }