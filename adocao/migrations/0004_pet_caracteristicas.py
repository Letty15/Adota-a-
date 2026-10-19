# Novos eixos de característica dos pets.
# Os defaults abaixo só existem para linhas antigas (preserve_default=False):
# no cadastro, todos os eixos são obrigatórios e não têm valor padrão.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adocao', '0003_remove_solicitacaoadocao_nome_pet_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pet',
            name='porte',
        ),
        migrations.AddField(
            model_name='pet',
            name='especie',
            field=models.CharField(default='cao', max_length=10, choices=[('cao', 'Cão'), ('gato', 'Gato'), ('outro', 'Outro')], verbose_name='espécie'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pet',
            name='porte',
            field=models.PositiveSmallIntegerField(default=2, choices=[(1, 'Pequeno'), (2, 'Médio'), (3, 'Grande')], verbose_name='porte'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pet',
            name='energia',
            field=models.PositiveSmallIntegerField(default=2, choices=[(1, 'Calmo'), (2, 'Moderado'), (3, 'Agitado')], verbose_name='nível de energia'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pet',
            name='temperamento',
            field=models.PositiveSmallIntegerField(default=2, choices=[(1, 'Arisco'), (2, 'Neutro'), (3, 'Dócil')], verbose_name='temperamento'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pet',
            name='independencia',
            field=models.PositiveSmallIntegerField(default=2, choices=[(1, 'Dependente'), (2, 'Médio'), (3, 'Independente')], verbose_name='independência'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pet',
            name='tolerancia_barulho',
            field=models.PositiveSmallIntegerField(default=2, choices=[(1, 'Sensível'), (2, 'Neutro'), (3, 'Tranquilo')], verbose_name='tolerância a barulho'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pet',
            name='experiencia',
            field=models.PositiveSmallIntegerField(default=2, choices=[(1, 'Iniciante serve'), (2, 'Alguma experiência'), (3, 'Tutor experiente')], verbose_name='experiência exigida do tutor'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pet',
            name='cuidados',
            field=models.PositiveSmallIntegerField(default=2, choices=[(1, 'Poucos'), (2, 'Moderados'), (3, 'Muitos')], verbose_name='cuidados especiais'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pet',
            name='convive_criancas',
            field=models.CharField(default='nt', max_length=3, choices=[('sim', 'Sim'), ('nao', 'Não'), ('nt', 'Não testado')], verbose_name='convive bem com crianças'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pet',
            name='convive_outros_pets',
            field=models.CharField(default='nt', max_length=3, choices=[('sim', 'Sim'), ('nao', 'Não'), ('nt', 'Não testado')], verbose_name='convive bem com outros pets'),
            preserve_default=False,
        ),
    ]
