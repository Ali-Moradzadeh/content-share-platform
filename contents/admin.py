from django.contrib import admin
from .models import Comment, Post, PostPart, Story, StoryInteraction, BookmarkAlbum, AlbumFileDetail, ChatRoom, ChatRoomJoinDetail, Chat, ChatReaction, PrivateChat, PrivateChatDetail


register = lambda i: admin.site.register(i)

register(Post)
register(PostPart)
register(Comment)
register(Story)
register(StoryInteraction)
register(BookmarkAlbum)
register(AlbumFileDetail)
register(ChatRoom)
register(ChatRoomJoinDetail)
register(Chat)
register(ChatReaction)
register(PrivateChat)
register(PrivateChatDetail)
