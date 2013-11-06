/*
Copyright (c) 2003-2011, CKSource - Frederico Knabben. All rights reserved.
For licensing, see LICENSE.html or http://ckeditor.com/license
*/

CKEDITOR.editorConfig = function( config )
{
	// Define changes to default configuration here. For example:
	// config.language = 'fr';
	config.uiColor = '#AADC6E';
};

/*
	//TODO: Try and test these RAPCMS config settings

CKEDITOR.editorConfig = function( config )
{
	// Define changes to default configuration here. For example:
	// config.language = 'fr';
	// config.uiColor = '#AADC6E';
};

<?
		Header("content-type: application/x-javascript");

		include("../inc/configuration.php");

		//include custom/include.php if exists
		if(file_exists("../custom/include.php")) include "../custom/include.php";
		?>
		CKEDITOR.editorConfig = function( config )
		{
		    // Define changes to default configuration here. For example:
		    // config.language = 'fr';
		    // config.uiColor = '#AADC6E';

		    config.enterMode =  CKEDITOR.ENTER_P;
		    config.forcePasteAsPlainText = true;
		    <?
		    echo "config.contentsCss = 'stylesheet/".$Theme."_style.php?CKstyle=1';";
		    ?>
		    config.filebrowserBrowseUrl = 'ckeditor/filemanager/browser/default/browser.html?Connector=http://<? echo
		    config.filebrowserUploadUrl = 'http://<? echo $_SERVER["SERVER_NAME"]; ?>/ckeditor/filemanager/connectors/
		    config.resize_minWidth = 510;
		    config.toolbar =
		    [
		        ['Source', '-', 'PasteText', '-', 'RemoveFormat', '-', 'Format', '-', 'Font', 'FontSize', '-', 'Bold',
		    ];
		};

		CKEDITOR.on('instanceReady', function(ev)
		    {
		        var tags = ['p', 'ol', 'ul', 'li']; // etc.

		        for (var key in tags) {
		            ev.editor.dataProcessor.writer.setRules(tags[key],
		                {
		                    indent : false,
		                    breakBeforeOpen : true,
		                    breakAfterOpen : false,
		                    breakBeforeClose : false,
		                    breakAfterClose : true
		                });
		        }
		});
*/