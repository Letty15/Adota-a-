"""Opções dos eixos de característica dos pets.

Os eixos de 1 a 3 são ordinais: quanto maior o número, mais "intenso" é o traço.
Mantido sem dependência do Django para a lógica de compatibilidade ser testável.
"""

ESPECIE = [
    ("cao", "Cão"),
    ("gato", "Gato"),
    ("outro", "Outro"),
]

PORTE = [(1, "Pequeno"), (2, "Médio"), (3, "Grande")]

ENERGIA = [(1, "Calmo"), (2, "Moderado"), (3, "Agitado")]

TEMPERAMENTO = [(1, "Arisco"), (2, "Neutro"), (3, "Dócil")]

INDEPENDENCIA = [(1, "Dependente"), (2, "Médio"), (3, "Independente")]

TOLERANCIA_BARULHO = [(1, "Sensível"), (2, "Neutro"), (3, "Tranquilo")]

EXPERIENCIA = [
    (1, "Iniciante serve"),
    (2, "Alguma experiência"),
    (3, "Tutor experiente"),
]

CUIDADOS = [(1, "Poucos"), (2, "Moderados"), (3, "Muitos")]

CONVIVE = [("sim", "Sim"), ("nao", "Não"), ("nt", "Não testado")]
