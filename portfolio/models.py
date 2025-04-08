from django.db import models

# Create your models here.


class Command(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    help = models.TextField()
    creation_date = models.DateTimeField("date published")

    def __str__(self):
        return str(self.name)


class Directory(models.Model):
    parent_directory = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="subdirectories",
    )
    name = models.CharField(max_length=200)
    description = models.TextField()
    creation_date = models.DateTimeField("date published")

    def __str__(self):
        return str(self.name)


class BlogPost(models.Model):
    directory = models.ForeignKey(Directory, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        return str(self.title)


class Note(models.Model):
    directory = models.ForeignKey(Directory, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        return str(self.title)


class File(models.Model):
    directory = models.ForeignKey(Directory, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        return str(self.title)
