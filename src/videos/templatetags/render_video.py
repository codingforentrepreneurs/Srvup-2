from django import template

register = template.Library()

from videos.models import Video

@register.inclusion_tag('videos/snippets/render_video.html')
def render_video(video_obj):
    video = None
    if isinstance(video_obj, Video):
        video = video_obj.embed_code
    return {'video': video}