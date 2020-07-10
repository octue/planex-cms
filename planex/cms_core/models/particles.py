from django.db import models
from wagtail.snippets.models import register_snippet

from ..fields import ColorField


@register_snippet
class ParticlesConfiguration(models.Model):
    """ Snippet for configuring particlejs options which can then be included elsewhere
    """

    PARTICLES_TYPE_CHOICES = (
        (1, "circle"),
        (2, "edge"),
        (3, "triangle"),
        (4, "polygon"),
        (5, "star"),
        (6, "image"),
    )
    PARTICLES_MOVE_DIRECTION_CHOICES = (
        (1, "none"),
        (2, "top"),
        (3, "top-right"),
        (4, "right"),
        (5, "bottom-right"),
        (6, "bottom"),
        (7, "bottom-left"),
        (8, "left"),
    )
    title = models.CharField(max_length=50)
    number = models.PositiveSmallIntegerField(default=50)
    shape_type = models.PositiveSmallIntegerField(choices=PARTICLES_TYPE_CHOICES, default=1)
    polygon_sides = models.PositiveSmallIntegerField(default=5)
    size = models.DecimalField(default=2.5, max_digits=4, decimal_places=1)
    size_random = models.BooleanField(default=False)
    colour = ColorField(default="ffffff", help_text="Don't include # symbol.")
    opacity = models.DecimalField(default=0.9, max_digits=2, decimal_places=1)
    opacity_random = models.BooleanField(default=False)
    move_speed = models.DecimalField(default=2.5, max_digits=2, decimal_places=1)
    move_direction = models.PositiveSmallIntegerField(choices=PARTICLES_MOVE_DIRECTION_CHOICES, default=1)
    line_linked = models.BooleanField(default=True)
    css_background_colour = ColorField(blank=True, help_text="Don't include # symbol. Will be overridden by linear gradient")
    css_background_linear_gradient = models.CharField(
        blank=True, max_length=255, help_text="Enter in the format 'to right, #2b2b2b 0%, #243e3f 28%, #2b2b2b 100%'"
    )
    css_background_url = models.URLField(blank=True, max_length=255)

    class Meta:
        verbose_name = "Particles Configuration"
        verbose_name_plural = "Particles Configurations"

    def __str__(self):
        return '{} "{}"'.format(self.Meta.verbose_name, self.title)
