from livesettings import *

SITE_GROUP = ConfigurationGroup('SITE', 'Site Settings', ordering=0)


config_register_list(
    StringValue(SITE_GROUP,
        'TITLE',
        description='Site Title',
        ordering=0,
        default='',
    ),
    LongStringValue(SITE_GROUP,
        'KEYWORDS',
        description='Site Keywords',
        help_text='Enter a comma-separated list of keywords that describe your site.  This helps some search engines index your pages.',
        ordering=1,
        default='',
    ),
    LongStringValue(SITE_GROUP,
        'DESCRIPTION',
        description='Site Description',
        help_text='Enter a description for your site. This is used by some search engines.',
        ordering=2,
        default='',
    ),
)
