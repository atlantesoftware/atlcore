#coding=UTF-8

from django import template

register = template.Library()

@register.inclusion_tag("site/utils/get_image_crop.html")
def get_image_crop(item_image, width=128, height=128):
    from PIL import Image
    import os

    file_dir = os.path.dirname(item_image.path) + '/thumbnails/'
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    file_url_dir = os.path.dirname(item_image.url) + '/thumbnails/' 
    file_name = os.path.basename(item_image.path)
    file_basename = file_name.split('.')[0]
    try:
        file_ext = file_name.split('.')[1]
    except:
        file_ext = ''
    thumbnail_image_path = '%s%s_%sx%s.%s' % (file_dir, file_basename, str(width), str(height), file_ext)
    thumbnail_image_absolute_url = '%s%s_%sx%s.%s' % (file_url_dir, file_basename, str(width), str(height), file_ext)
    
    if not os.path.exists(thumbnail_image_path):            
        image = Image.open(item_image.path)

        src_width, src_height = image.size
        src_ratio = float(src_width) / float(src_height)
        dst_width, dst_height = width, height
        dst_ratio = float(dst_width) / float(dst_height)

        if dst_ratio < src_ratio:
            crop_height = src_height
            crop_width = crop_height * dst_ratio
            x_offset = float(src_width - crop_width) / 2
            y_offset = 0
        else:
            crop_width = src_width
            crop_height = crop_width / dst_ratio
            x_offset = 0
            y_offset = float(src_height - crop_height) / 3
        image = image.crop((int(x_offset), int(y_offset), int(x_offset+crop_width), int(y_offset+crop_height)))
        image = image.resize((int(dst_width), int(dst_height)), Image.ANTIALIAS)
        try:
            image.save(thumbnail_image_path, image.format, quality=90, optimize=1)
        except:
            try:
                image.save(thumbnail_image_path, image.format, quality=90)
            except Exception, e:
                return e
    context = {}
    context['image_absolute_url'] = thumbnail_image_absolute_url
    return context



@register.inclusion_tag("site/utils/get_image_crop_url.html")
def get_image_crop_url( node, width, height):
    image_url = ""
    if node is not None and node.image is not None:
        try:
            image_url = node.get_image_crop(width,height)
        except:
            image_url = ""
    context = {
        'image_url':image_url,
    }
    return context

@register.inclusion_tag("site/utils/get_paginator_near_page_list.html")
def get_paginator_near_page_list(current_page, page_count, page_to_show, search = "None"):
    page_nums = []
    if current_page - page_to_show / 2 + (1 - page_to_show % 2) < 1:
        num = 1
    else:
        if current_page + page_to_show / 2 > page_count:
            if page_count - page_to_show < 1:
                num = 1
            else:
                num = page_count - page_to_show + 1
        else:
            num = current_page - page_to_show / 2 + (1 - page_to_show % 2)
    while (page_to_show > 0) and (num <= page_count):
        page_nums.append(num)
        page_to_show -= 1
        num += 1
    context = {
        'current_page': current_page, 
        'page_nums': page_nums,
        'search': search,
    }
    return context


@register.inclusion_tag("site/utils/get_image_crop_url.html")
def get_crop_image_url( node, width, height):
    return get_image_crop_url(node, width, height)
