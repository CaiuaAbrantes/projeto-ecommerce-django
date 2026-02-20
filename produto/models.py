from django.db import models
from PIL import Image
import os
from django.conf import settings

class Produto(models.Model):
    nome = models.CharField(max_length=255)
    descricao_curta = models.TextField(max_length=255)
    descricao_longa = models.TextField()
    imagem = models.ImageField((""), upload_to='media/produto_imagens', blank=True)
    models.SlugField(unique=True)
    preco_marketing = models.FloatField(default=0)
    preco_marketing_promocional = models.FloatField(default=0)
    tipo = models.CharField(
        default='V',
        max_length=1,
        choices=(
            ('V', 'Variacao'),
            ('S', 'Simples'),
        )
    )
    
    def resize_image(self, img, new_width=800): 
        img_full_path = os.path.join(settings.MEDIA_ROOT, img.name)
        img_pillow = Image.open(img_full_path)
        original_width, original_height =  img_pillow.size
        if original_width <= new_width:
            print('retornando menor')
            img_pillow.close()
            return
        new_height = round((new_width * original_height) / original_width)
        new_img = img_pillow.resize((new_width, new_height), Image.LANCZOS)
        new_img.save(
            img_full_path,
            optimize = True,
            quality = 50,   
        )
        print('a imagem foi redimencionada')


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        max_image_size = 800
        if self.imagem:
            self.resize_image(self.imagem, max_image_size)

    def __str__(self):
        return self.nome

class Variacao(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    nome = models.CharField(max_length=50, blank=True, null=True)
    preco = models.FloatField()
    preco_promocional = models.FloatField(default=0)
    estoque = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = "Variação"
        verbose_name_plural = "Variações"

    def __str__(self):
        return self.nome or self.produto.nome