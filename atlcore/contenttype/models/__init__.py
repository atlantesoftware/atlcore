#coding=UTF-8
from django.db.models.signals import post_save

# models
from atlcore.contenttype.models.node import Node
from atlcore.contenttype.models.content import Content
from atlcore.contenttype.models.container import Container
from atlcore.contenttype.models.folder import Folder
from atlcore.contenttype.models.news import News
from atlcore.contenttype.models.video import Video
from atlcore.contenttype.models.audio import Audio
from atlcore.contenttype.models.banner import Banner
from atlcore.contenttype.models.document import Document
from atlcore.contenttype.models.file import File
from atlcore.contenttype.models.image import Picture
from atlcore.contenttype.models.link import Link
from atlcore.contenttype.models.map import Map
# signals
from atlcore.contenttype.models.signals.node import create_ct_relation

post_save.connect(create_ct_relation)
