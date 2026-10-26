# Deploy no PythonAnywhere

Guia para colocar o Adota Aí no ar em `https://SEUUSUARIO.pythonanywhere.com`.
Troque `SEUUSUARIO` pelo seu nome de usuário do PythonAnywhere em todos os passos.

## Por que o deploy precisa de cuidados
Com `DEBUG=False` o Django **não serve** CSS, JS nem as fotos dos pets. No
PythonAnywhere quem serve esses arquivos é o próprio servidor, por mapeamentos
na aba **Web > Static files**. O projeto já está preparado (`STATIC_ROOT`,
`ALLOWED_HOSTS` e `CSRF_TRUSTED_ORIGINS` por variável de ambiente).

## 1. Código
No console **Bash** do PythonAnywhere:

```bash
git clone https://github.com/SEU_REPOSITORIO/Adota-a--main.git
cd Adota-a--main
```

## 2. Ambiente virtual e dependências
O Django do projeto exige Python recente. Confira na aba **Web** qual versão
do Python está disponível e use a mais nova (3.12 ou superior).

```bash
mkvirtualenv adota --python=python3.12
pip install -r requirements.txt
```

## 3. Banco e administrador
O `db.sqlite3` não vai no Git (está no `.gitignore`), então no servidor o banco
começa vazio. As fotos dos pets (`media/pets/`) e os dados iniciais dos pets
(`adocao/fixtures/pets.json`) vão no Git e são carregados no passo abaixo:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
python manage.py loaddata pets
```

`collectstatic` cria a pasta `staticfiles/`.

## 4. Aba Web
Crie o app em **Web > Add a new web app > Manual configuration**
(mesma versão do Python do passo 2) e preencha:

| Campo | Valor |
|---|---|
| Source code | `/home/SEUUSUARIO/Adota-a--main` |
| Virtualenv | `/home/SEUUSUARIO/.virtualenvs/adota` |

### Static files (esta parte faz o CSS e as fotos aparecerem)
| URL | Directory |
|---|---|
| `/static/` | `/home/SEUUSUARIO/Adota-a--main/staticfiles` |
| `/media/` | `/home/SEUUSUARIO/Adota-a--main/media` |

### Arquivo WSGI
Clique no link do arquivo WSGI (na aba Web), apague tudo e deixe só:

```python
import os
import sys

path = '/home/SEUUSUARIO/Adota-a--main'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'adota_ai.settings'

# Produção
os.environ['DJANGO_DEBUG'] = 'False'
os.environ['DJANGO_SECRET_KEY'] = 'COLE-AQUI-UMA-CHAVE-LONGA-E-ALEATORIA'
os.environ['DJANGO_ALLOWED_HOSTS'] = 'SEUUSUARIO.pythonanywhere.com'
os.environ['DJANGO_CSRF_TRUSTED_ORIGINS'] = 'https://SEUUSUARIO.pythonanywhere.com'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

Para gerar uma `SECRET_KEY` nova, no console:

```bash
python -c "from django.core.management.utils import get_random_secret_key as g; print(g())"
```

## 5. Publicar
Na aba **Web**, clique em **Reload**. Acesse `https://SEUUSUARIO.pythonanywhere.com`.

## 6. Cadastrar os pets
Entre com o superusuário criado no passo 3, abra o menu do seu nome e clique em
**Cadastrar pet**. As fotos enviadas ficam em `media/pets/` no servidor.

## Atualizando depois
```bash
cd ~/Adota-a--main
git pull
workon adota
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
```
Se você cadastrou novos pets e quer levá-los ao GitHub, veja a seção
**Levando novos pets para o GitHub** abaixo.

E clique em **Reload** na aba Web.

## Problemas comuns
- **Página sem estilo (CSS):** faltou `collectstatic` ou o mapeamento `/static/`.
- **Foto do pet quebrada:** faltou o mapeamento `/media/`.
- **`DisallowedHost`:** o domínio não está em `DJANGO_ALLOWED_HOSTS`.
- **`403 CSRF` ao enviar formulário:** confira `DJANGO_CSRF_TRUSTED_ORIGINS`
  (com `https://`).
- **Qualquer erro 500:** veja a aba **Web > Error log**.

## Levando novos pets para o GitHub
Fotos enviadas pelo formulário ficam em `media/pets/` (não em `static/`, que é
só para logo, CSS e JS). Depois de cadastrar pets na sua máquina:

```bash
python manage.py dumpdata adocao.Pet --indent 2 -o adocao/fixtures/pets.json
git add media/pets adocao/fixtures/pets.json
git commit -m "Atualiza pets"
git push
```
No servidor: `git pull` e `python manage.py loaddata pets`.
