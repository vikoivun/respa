from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.gis.db import models
from django.contrib.gis.db.models import Q
from django.utils.translation import ugettext_lazy as _
from guardian.shortcuts import get_objects_for_user
from resources.models import Reservation, Unit

COMMENTABLE_MODELS = ('reservation',)


class CommentQuerySet(models.QuerySet):
    def can_view(self, user):
        if not user.is_authenticated():
            return self.none()

        allowed_units = get_objects_for_user(
            user, 'resources.can_access_reservation_comments', klass=Unit
        )
        allowed_reservation_ids = Reservation.objects.filter(
            Q(resource__unit__in=allowed_units) | Q(user=user)
        ).values_list('id', flat=True)

        content_type = ContentType.objects.get_for_model(Reservation)
        return self.filter(
            Q(created_by=user) |
            (Q(content_type=content_type) & Q(object_id__in=allowed_reservation_ids))
        )


class Comment(models.Model):
    created_at = models.DateTimeField(verbose_name=_('Time of creation'), auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Created by'),
                                   null=True, blank=True, related_name='%(class)s_created')
    text = models.TextField(verbose_name=_('Text'))
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={'model__in': COMMENTABLE_MODELS}
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    objects = CommentQuerySet.as_manager()

    class Meta:
        ordering = ('id',)
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
        index_together = (('content_type', 'object_id'),)

    def __str__(self):
        author = self.created_by.get_display_name() if self.created_by else 'Unknown author'
        text = self.text if len(self.text) < 40 else self.text[:37] + '...'
        return '%s %s %s: %s' % (self.content_type.model, self.object_id, author, text)

    @staticmethod
    def can_user_comment_object(user, target_object):
        if not (user and user.is_authenticated()):
            return False

        target_type = target_object.__class__.__name__.lower()
        if target_type not in COMMENTABLE_MODELS:
            return False

        if target_type == 'reservation':
            if user == target_object.user:
                return True
            if user.has_perm('resources.can_access_reservation_comments', target_object.resource.unit):
                return True

        return False
