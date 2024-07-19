from django.db import models


# Create your models here.
class Puzzle(models.Model):
    title = models.CharField(max_length=255, blank=True, default="")
    date = models.DateTimeField()
    byline = models.CharField(
        max_length=255,
    )
    publisher = models.CharField(
        max_length=12,
    )

    def __str__(self):
        return f"{self.publisher}:{self.date.strftime('%Y-%m-%d')}"


class Entry(models.Model):
    entry_text = models.CharField(max_length=50, unique=True, default="")

    def __str__(self):
        return self.entry_text


class Clue(models.Model):
    entry = models.ForeignKey(
        Entry,
        models.PROTECT,
    )
    puzzle = models.ForeignKey(
        Puzzle,
        models.PROTECT,
    )
    clue_text = models.TextField(max_length=512)
    theme = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.entry.entry_text}: {self.clue_text}"
