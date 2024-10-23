from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    class Meta:
        indexes = [
            models.Index(fields=['name'])
        ]

class Book(models.Model):
    STATUS_CHOISES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'), 
    ]
    title = models.CharField(max_length=255)
    publish_date = models.DateField()
    price = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOISES, default='draft')

    def __str__(self):
        return self.title
    
    # Indexing: To make fast the ORM Queries and Optimize the result
    class Meta:
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['publish_date']),
            models.Index(fields=['price']),
            models.Index(fields=['author']),
        ]
    