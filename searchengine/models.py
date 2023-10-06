from django.db import models

class Document(models.Model):
    doc_id = models.IntegerField(db_index=True)
    text = models.TextField()
    title = models.TextField()

    def __str__(self):
        return self.title