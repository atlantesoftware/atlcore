#coding=UTF-8

#tinymce configuration
import tinymce
TINYMCE_JS_URL = '/atlante_core_media/common/tiny_mce/tiny_mce.js'
TINYMCE_DEFAULT_CONFIG = {
    'plugins': "table,spellchecker,paste,searchreplace",
    'theme': "advanced",
    'theme_advanced_buttons3_add': "|,spellchecker|,pastetext,pasteword,selectall",
    'theme_advanced_toolbar_location' : "top",
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 10,
}
TINYMCE_SPELLCHECKER = False
TINYMCE_COMPRESSOR = False