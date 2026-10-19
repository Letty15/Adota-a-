"""Cálculo de compatibilidade entre o perfil do quiz e os pets.

Sem dependência do Django: recebe e devolve dicionários simples.

Perfil do adotante: valor de 1 a 3 (pode ser decimal, é a média das respostas)
para cada eixo, mais os votos de espécie e as restrições (crianças / outros pets).

Três tipos de eixo:
  - simétrico:  quanto mais perto, melhor (energia, porte, temperamento, independência)
  - necessidade: o pet "exige" algo do tutor; só pesa contra se exigir MAIS do que o
                 tutor oferece (experiência, cuidados)
  - ambiente:   o pet precisa aguentar o ambiente; só pesa contra se for menos
                tolerante do que a casa exige (tolerância a barulho)
"""

EIXOS = {
    # campo do pet: (tipo, peso, rótulo)
    "energia": ("simetrico", 3.0, "energia"),
    "porte": ("simetrico", 2.0, "porte"),
    "temperamento": ("simetrico", 2.0, "temperamento"),
    "independencia": ("simetrico", 2.0, "independência"),
    "tolerancia_barulho": ("ambiente", 1.5, "tolerância a barulho"),
    "experiencia": ("necessidade", 1.5, "experiência exigida"),
    "cuidados": ("necessidade", 1.5, "cuidados"),
}

PESO_ESPECIE = 3.0
LIMIAR_COMBINA = 0.8


def _pontuar_eixo(tipo, valor_pet, valor_user):
    """Devolve uma nota de 0 a 1."""
    if tipo == "simetrico":
        distancia = abs(valor_pet - valor_user)
    elif tipo == "necessidade":
        distancia = max(0.0, valor_pet - valor_user)
    elif tipo == "ambiente":
        distancia = max(0.0, valor_user - valor_pet)
    else:
        raise ValueError(f"tipo de eixo desconhecido: {tipo}")
    return max(0.0, 1.0 - distancia / 2.0)


def especie_recomendada(votos_especie):
    """Lista das espécies com mais votos (mais de uma em caso de empate)."""
    if not votos_especie:
        return []
    maximo = max(votos_especie.values())
    if maximo <= 0:
        return []
    return [e for e, v in votos_especie.items() if v == maximo]


def calcular(pet, perfil, votos_especie):
    """Compatibilidade (0-100) de um pet com o perfil.

    `pet` é um dict com as chaves de EIXOS e 'especie'.
    `perfil` é um dict {eixo: valor}; eixos ausentes são ignorados.
    """
    total = 0.0
    soma_pesos = 0.0
    combina = []

    for campo, (tipo, peso, rotulo) in EIXOS.items():
        if campo not in perfil:
            continue
        nota = _pontuar_eixo(tipo, pet[campo], perfil[campo])
        total += nota * peso
        soma_pesos += peso
        if nota >= LIMIAR_COMBINA:
            combina.append(rotulo)

    maximo_votos = max(votos_especie.values()) if votos_especie else 0
    if maximo_votos > 0:
        nota_especie = votos_especie.get(pet["especie"], 0) / maximo_votos
        total += nota_especie * PESO_ESPECIE
        soma_pesos += PESO_ESPECIE

    pct = round(total / soma_pesos * 100) if soma_pesos else 0
    return {"pct": pct, "combina": combina}


def passa_restricoes(pet, tem_criancas, tem_outros_pets):
    """Filtro eliminatório: pet marcado como 'não convive' é excluído."""
    if tem_criancas and pet["convive_criancas"] == "nao":
        return False
    if tem_outros_pets and pet["convive_outros_pets"] == "nao":
        return False
    return True


def ranking(pets, perfil, votos_especie, tem_criancas=False,
            tem_outros_pets=False, limite=3):
    """Os `limite` pets mais compatíveis, já sem os eliminados.

    Cada item devolvido é o dict do pet acrescido de 'pct' e 'combina'.
    """
    resultado = []
    for pet in pets:
        if not passa_restricoes(pet, tem_criancas, tem_outros_pets):
            continue
        item = dict(pet)
        item.update(calcular(pet, perfil, votos_especie))
        resultado.append(item)

    resultado.sort(key=lambda p: (-p["pct"], str(p.get("nome", ""))))
    return resultado[:limite]
