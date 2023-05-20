from django.db import models
from accounting.models import UserProfile
from datetime import timedelta
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from random import shuffle
import uuid


class Post(models.Model):
    owners = models.ManyToManyField(UserProfile, related_name="posts")
    caption = models.TextField()
    likes = models.ManyToManyField(UserProfile, related_name="posts_like")
    created_at = models.DateTimeField(auto_now_add=True)
    
    @property
    def type(self):
        return "image"
    
    def __str__(self):
        return f"{self.id} | {str(self.owners)}"


class PostPart(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_parts")
    file = models.FileField(upload_to="posts/")
    
    def __str__(self):
        return f"{self.id}"


class Comment(models.Model):
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    body = models.CharField(max_length=255)
    reply_to = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, related_name="replies")
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    
    @property
    def is_reply(self):
        return bool(self.reply_to)
        
    def __str__(self):
        return f"{self.body} | {self.owner.user.username}"


class Story(models.Model):
    STORY_TYPE = (
        ("F", "Followes"),
        ("C", "Close Friends"),
    )
    
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="stories")
    interactions = models.ManyToManyField(UserProfile, through="StoryInteraction", related_name="story_interactions")
    file = models.FileField(upload_to="current_stories/")
    created_at = models.DateTimeField(auto_now_add=True)
    kind = models.CharField(max_length=1, choices=STORY_TYPE)
    
    class Meta:
        verbose_name_plural = "stories"
    
    
    
    @property
    def expire_at(self):
        return self.created_at + timedelta(days=1)
 
    def __str__(self):
        return f"{self.id} | {self.owner.user.username} | {self.created_at}"
    
    
class StoryInteraction(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name="profile_interactions")
    interactive = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="story_interactions_as_interactive")
    liked = models.BooleanField(default=False)
    reply_text = models.CharField(max_length=255, null=True, blank=True)
    occured_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if self.interactive != self.story.owner:
            return super().save(*args, **kwargs)
    
    
    def __str__(self):
        return f"{self.interactive.user.username} seen story={self.story.owner.user.username} at {self.occured_at}"
    

class BookmarkAlbum(models.Model):
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="albums")
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    files = models.ManyToManyField(Post, through="AlbumFileDetail", related_name="album")
    
    class Meta:
        unique_together = ("owner", "title")
    
    def __str__(self):
        return f"{self.title}|{self.owner.user.username} contains {self.files.count()} file"
    
    
class AlbumFileDetail(models.Model):
    album = models.ForeignKey(BookmarkAlbum, on_delete=models.CASCADE, related_name="files_details")
    file = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="bookmark_details")
    bookmarked_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.file} in {self.album.title}"


class PrivateChat(models.Model):
    code = models.UUIDField(default=uuid.uuid4, editable=False)
    members = models.ManyToManyField(UserProfile, through="PrivateChatPare", related_name="private_chat_pare")
    
    def __str__(self):
        return str(self.code)


class PrivateChatPare(models.Model):
    member = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="private_chat_details")
    private_chat = models.ForeignKey(PrivateChat, on_delete=models.CASCADE, related_name="private_chat_details")
    
    class Meta:
        unique_together = ("member", "private_chat")
    
    def clean(self, *args, **kwargs):
        if self.private_chat.members.count() >= 2:
            raise ValidationError("You Cant assign more than 2 accounts in one private chat")
        return super().clean(*args, **kwargs)
    
    def __str__(self):
        return f"{self.member.user.username} | {self.private_chat}"
    

class ChatRoom(models.Model):
    members = models.ManyToManyField(UserProfile, through="ChatRoomJoinDetail", related_name="joined_chat_rooms")
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    
    def __str__(self):
        return f"{self.title}"
    

class ChatRoomJoinDetail(models.Model):
    member = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="chatroom_membering_details")
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name="member_joining_details")
    join_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.member.user.username} joined {self.chatroom.title} at {self.join_at}"


class Chat(models.Model):
    chat_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    chat_id = models.PositiveBigIntegerField()
    obj = GenericForeignKey("chat_type", "chat_id")
    
    publisher = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="chat_published")
    reactions = models.ManyToManyField(UserProfile, through="ChatReaction", related_name="reactions")
    body = models.CharField(max_length=255)
    
    def clean(self, *args, **kwargs):
        try:
            self.obj.members.get(id=self.publisher.id)
            super().clean(*args, **kwargs)
        except UserProfile.DoesNotExist:
            raise ValidationError(f"{self.publisher.user.username} can only send messages to joined chat rooms")
    
    def __str__(self):
        return f"{self.body} published by {self.publisher.user.username} at {self.obj}"


class ChatReaction(models.Model):
    reactor = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="chat_reactions")
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="chat_reactions")
    liked = models.BooleanField(default=False)
    seen_at = models.DateTimeField(auto_now_add=True)
    
    def clean(self, *args, **kwargs):
        try:
            self.chat.obj.members.get(id=self.reactor.id)
            super().clean(*args, **kwargs)
        except UserProfile.DoesNotExist:
            raise ValidationError(f"{self.reactor.user.username} can only react to messages in joined chat rooms")
    
    def __str__(self):
        return f"{self.reactor.user.username} seen {self.chat.body} at {self.seen_at}"