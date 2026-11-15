"""Popula o banco com usuários, categorias, posts e comentários de exemplo.

Idempotente: pode ser executado várias vezes sem duplicar registros.
Uso: python manage.py seed_blog
"""
from datetime import datetime
from zoneinfo import ZoneInfo

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from blog.models import Category, Comment, Post

TZ = ZoneInfo('America/Sao_Paulo')


def dt(year, month, day, hour, minute):
    return datetime(year, month, day, hour, minute, tzinfo=TZ)


USERS = [
    ('ana', 'Ana', 'Lima'),
    ('bruno', 'Bruno', 'Costa'),
    ('carla', 'Carla', 'Mendes'),
]

CATEGORIES = [
    ('Comercial', 'Prospecção, qualificação e venda de projetos de dados e IA.'),
    ('Dados e IA', 'Engenharia de dados, dashboards e soluções de inteligência artificial.'),
    ('Projetos', 'Desenho e execução de soluções para clientes do Núcleo de Dados e IA.'),
]

POSTS = [
    {
        'title': 'Coordenador de Negócios no Núcleo de Dados e IA',
        'posted_at': dt(2026, 1, 20, 10, 0),
        'categories': ['Comercial', 'Projetos'],
        'content': (
            '<p><em>Jan 2026 – presente · Poli Júnior, Núcleo de Dados e IA</em></p>\n'
            '<p>Como Coordenador de Negócios (CN) do Núcleo de Dados e IA, respondo pela '
            'gestão do funil comercial da área e participo do processo e do desenho de '
            'cada solução vendida.</p>\n'
            '<h2>Atribuições</h2>\n'
            '<ul>\n'
            '  <li>Venda de projetos para grandes empresas, participando do desenho de cada solução</li>\n'
            '  <li>Gestão do funil comercial da área</li>\n'
            '  <li>Atuação nos quatro canais de entrada: inbound, indicação, fidelização e outbound</li>\n'
            '  <li>Liderança e qualificação de membros da equipe</li>\n'
            '  <li>Participação em decisões estratégicas de inovação da empresa</li>\n'
            '</ul>\n'
            '<h2>Reconhecimento</h2>\n'
            '<ul>\n'
            '  <li><strong>Maior vendedor da empresa no ano de 2026</strong></li>\n'
            '  <li><strong>Terceiro maior vendedor da história da Poli Júnior</strong></li>\n'
            '  <li>Destaque comercial por dois semestres consecutivos: 2025S2 e 2026S1</li>\n'
            '</ul>'
        ),
        'comments': [
            ('ana', dt(2026, 1, 21, 9, 12),
             'Parabéns pela coordenação! Dá para ver o quanto o funil da área amadureceu.'),
            ('bruno', dt(2026, 1, 22, 18, 40),
             'Atuar nos quatro canais ao mesmo tempo deve ser puxado. Como você prioriza os leads?'),
            ('carla', dt(2026, 1, 25, 11, 5),
             'Terceiro maior vendedor da história da PJ é muita coisa. Sucesso no cargo!'),
        ],
    },
    {
        'title': 'Analista de Dados: o lado da execução',
        'posted_at': dt(2025, 11, 10, 9, 30),
        'categories': ['Dados e IA', 'Projetos'],
        'content': (
            '<p><em>Mar 2025 – Nov 2025 · Poli Júnior, Núcleo de Dados e IA</em></p>\n'
            '<p>Como Analista de Dados, atuei na execução de projetos para grandes '
            'empresas — o lado da entrega, complementar à atuação comercial que exerci '
            'nos demais cargos.</p>\n'
            '<h2>Projetos executados</h2>\n'
            '<ul>\n'
            '  <li>Mapeamento de processos para automação em banco</li>\n'
            '  <li>Mapeamento de sistemas para integração CRM + ERP</li>\n'
            '  <li>Extração e consolidação de dados jurídicos</li>\n'
            '</ul>\n'
            '<p>Ferramentas do dia a dia: <code>Python</code>, Power BI e Excel avançado.</p>'
        ),
        'comments': [
            ('bruno', dt(2025, 11, 11, 14, 20),
             'A integração CRM + ERP parece ter sido o projeto mais desafiador. Que stack vocês usaram?'),
            ('carla', dt(2025, 11, 14, 8, 55),
             'Gostei de ver os dois lados do projeto, execução e venda, na mesma trajetória.'),
        ],
    },
    {
        'title': 'Consultor de Negócios: primeiros passos no comercial',
        'posted_at': dt(2025, 5, 28, 18, 0),
        'categories': ['Comercial'],
        'content': (
            '<p><em>Mar 2025 – Mai 2025 · Poli Júnior, Núcleo de Dados e IA</em></p>\n'
            '<p>Como Consultor de Negócios, fui responsável pela captação ativa de '
            'clientes para o Núcleo de Dados e IA.</p>\n'
            '<h2>Atribuições</h2>\n'
            '<ul>\n'
            '  <li>Prospecção <em>outbound</em>, isto é, a captação ativa de clientes</li>\n'
            '  <li>Venda de quatro projetos, entre dashboards e soluções de IA</li>\n'
            '</ul>'
        ),
        'comments': [],
    },
    {
        'title': 'SDR: canais de entrada de leads',
        'posted_at': dt(2025, 12, 15, 14, 0),
        'categories': ['Comercial'],
        'content': (
            '<p><em>Jun 2025 – Dez 2025 · Poli Júnior, Núcleo de Dados e IA</em></p>\n'
            '<p>Como SDR, respondi pelos canais de entrada de leads do Núcleo de Dados '
            'e IA, qualificando as oportunidades que chegavam à área.</p>\n'
            '<h2>Atribuições</h2>\n'
            '<ul>\n'
            '  <li>Três canais de entrada de leads: inbound, indicação e fidelização</li>\n'
            '  <li>Venda de quatro projetos para diversas empresas, participando do desenho de cada solução</li>\n'
            '</ul>'
        ),
        'comments': [
            ('ana', dt(2025, 12, 16, 10, 30),
             'Qualificação bem feita economiza muito tempo do time de execução. Bom resumo!'),
            ('carla', dt(2025, 12, 18, 16, 45),
             'Quais critérios você usava para qualificar os leads de indicação?'),
        ],
    },
]


class Command(BaseCommand):
    help = 'Popula o blog com dados de exemplo (idempotente).'

    @transaction.atomic
    def handle(self, *args, **options):
        User = get_user_model()
        users = {}
        for username, first, last in USERS:
            user, created = User.objects.get_or_create(
                username=username, defaults={'first_name': first, 'last_name': last}
            )
            if created:
                user.set_unusable_password()  # nenhuma senha no repositório
                user.save()
            users[username] = user

        categories = {}
        for name, description in CATEGORIES:
            cat, _ = Category.objects.update_or_create(
                name=name, defaults={'description': description}
            )
            categories[name] = cat

        for data in POSTS:
            post, _ = Post.objects.update_or_create(
                title=data['title'],
                defaults={'content': data['content'], 'posted_at': data['posted_at']},
            )
            post.categories.set(categories[n] for n in data['categories'])
            for username, posted_at, text in data['comments']:
                Comment.objects.update_or_create(
                    post=post,
                    author=users[username],
                    text=text,
                    defaults={'posted_at': posted_at},
                )

        self.stdout.write(self.style.SUCCESS(
            f'Seed ok: {Post.objects.count()} posts, {Category.objects.count()} categorias, '
            f'{Comment.objects.count()} comentários, {len(users)} comentaristas.'
        ))
