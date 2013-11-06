/**

   Created and copyrighted by Massimo Di Pierro <massimo.dipierro@gmail.com>
   (MIT license)  

   Example:

   <script src="share.js"></script>

**/

var script_source = $('script[src*="share.js"]').attr('src');
    var params = function(name,default_value) {
        var match = RegExp('[?&]' + name + '=([^&]*)').exec(script_source);
        return match && decodeURIComponent(match[1].replace(/\+/g, ' '))||default_value;
    }
var path = params('static','social');
var url = window.location.href;
var host =  window.location.hostname;
var title = escape($('title').text());
var twit = 'http://twitter.com/home?status='+title+'%20'+url;
var facebook = 'http://www.facebook.com/sharer.php?u='+url;
var gplus = 'https://plus.google.com/share?url='+url;
var linkedin = 'http://www.linkedin.com/shareArticle?mini=true&url='+encodeURIComponent(url)+'&title='+title+'&source=OnsAlexander';
var tbar = '<div id="socialdrawer"><span>Share<br/></span><div id="sicons"><a href="'+twit+'" id="twit" title="Share on twitter" target="_blank"><img src="'+path+'/twitter.png"  alt="Share on Twitter" width="32" height="32" /></a><a href="'+facebook+'" id="facebook" title="Share on Facebook" target="_blank"><img src="'+path+'/facebook.png"  alt="Share on facebook" width="32" height="32" /></a><a href="'+linkedin+'" id="linkedin" title="Share on LinkedIn" target="_blank"><img src="'+path+'/linkedin.png"  alt="Share on LinkedIn" width="32" height="32" /></a><a href="'+gplus+'" id="gplus" title="Share on Google Plus" target="_blank"><img src="'+path+'/gplus-32.png"  alt="Share on Google Plus" width="32" height="32" /></a></div></div>';	
// Add the share tool bar.
$('body').append(tbar); 
var st = $('#socialdrawer');
st.css({'opacity':'.7','z-index':'3000','background':'#FFF','border':'solid 1px #666','border-width':' 1px 0 0 1px','height':'20px','width':'40px','position':'fixed','bottom':'0','right':'0','padding':'2px 5px','overflow':'hidden','-webkit-border-top-left-radius':' 12px','-moz-border-radius-topleft':' 12px','border-top-left-radius':' 12px','-moz-box-shadow':' -3px -3px 3px rgba(0,0,0,0.5)','-webkit-box-shadow':' -3px -3px 3px rgba(0,0,0,0.5)','box-shadow':' -3px -3px 3px rgba(0,0,0,0.5)'});
$('#socialdrawer a').css({'float':'left','width':'32px','margin':'3px 2px 2px 2px','padding':'0'});
$('#socialdrawer span').css({'float':'left','margin':'2px 3px','text-shadow':' 1px 1px 1px #FFF','color':'#444','font-size':'12px','line-height':'1em', 'cursor':'pointer'});
    $('#socialdrawer img').hide();
// hover
st.click(function(){
	$(this).animate({height:'40px', width:'210px', opacity: 0.95}, 300);
	$('#socialdrawer img').show();
    });
//leave
st.mouseleave(function(){ 
    st.animate({height:'20px', width: '40px', opacity: .7}, 300); 
    $('#socialdrawer img').hide();
    return false;
    }  );
