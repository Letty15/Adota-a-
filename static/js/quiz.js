/*
 * Quiz de compatibilidade.
 *
 * Cada resposta pode:
 *   - valores:  {eixo: 1..3}  -> entra na média daquele eixo (mesmos eixos do cadastro do pet)
 *   - especie:  {cao|gato|outro: pontos} -> votos que decidem qual espécie combina mais
 *   - filtro:   {criancas|outros_pets: 0|1} -> restrições eliminatórias
 *
 * Ao final, o perfil (média por eixo) vai para /adocao/quiz/resultado/ pela URL,
 * e o Django calcula os 3 pets mais compatíveis.
 */

const perguntas = [
    {
        pergunta: "Onde você mora?",
        respostas: [
            { texto: "Casa com quintal", valores: { porte: 3, energia: 3 }, especie: { cao: 2 } },
            { texto: "Casa sem quintal", valores: { porte: 2, energia: 2 }, especie: { cao: 1, gato: 1 } },
            { texto: "Apartamento", valores: { porte: 1, energia: 1 }, especie: { gato: 2, outro: 1 } }
        ]
    },
    {
        pergunta: "Quanto tempo você passa em casa?",
        respostas: [
            { texto: "Quase o dia todo", valores: { independencia: 1 }, especie: { cao: 1 } },
            { texto: "Boa parte do dia", valores: { independencia: 2 }, especie: { cao: 1, gato: 1 } },
            { texto: "Passo pouco tempo em casa", valores: { independencia: 3 }, especie: { gato: 1, outro: 1 } }
        ]
    },
    {
        pergunta: "Como é sua rotina?",
        respostas: [
            { texto: "Muito ativa", valores: { energia: 3 }, especie: { cao: 1 } },
            { texto: "Moderadamente ativa", valores: { energia: 2 }, especie: { cao: 1, gato: 1 } },
            { texto: "Mais tranquila", valores: { energia: 1 }, especie: { gato: 1 } }
        ]
    },
    {
        pergunta: "Você gosta de fazer atividades ao ar livre?",
        respostas: [
            { texto: "Sim, bastante", valores: { energia: 3 }, especie: { cao: 1 } },
            { texto: "Às vezes", valores: { energia: 2 }, especie: { cao: 1, gato: 1 } },
            { texto: "Prefiro ficar em casa", valores: { energia: 1 }, especie: { gato: 1, outro: 1 } }
        ]
    },
    {
        pergunta: "Quanto tempo você teria para brincar com o pet?",
        respostas: [
            { texto: "Várias horas", valores: { energia: 3, temperamento: 3 }, especie: { cao: 1 } },
            { texto: "Algumas horas", valores: { energia: 2 }, especie: { cao: 1, gato: 1 } },
            { texto: "Pouco tempo", valores: { energia: 1, independencia: 3 }, especie: { gato: 1, outro: 1 } }
        ]
    },
    {
        pergunta: "Você prefere um pet mais independente?",
        respostas: [
            { texto: "Sim", valores: { independencia: 3 }, especie: { gato: 1, outro: 1 } },
            { texto: "Não, quero um pet bem apegado", valores: { independencia: 1 }, especie: { cao: 1 } },
            { texto: "Não tenho preferência", valores: { independencia: 2 }, especie: {} }
        ]
    },
    {
        pergunta: "Como é o ambiente da sua casa em relação a barulho?",
        respostas: [
            { texto: "Movimentado e barulhento (música, visitas, crianças)", valores: { tolerancia_barulho: 3 }, especie: { cao: 1 } },
            { texto: "Normal, com momentos de agito e de silêncio", valores: { tolerancia_barulho: 2 }, especie: {} },
            { texto: "Bem silencioso e tranquilo", valores: { tolerancia_barulho: 1 }, especie: { gato: 1, outro: 1 } }
        ]
    },
    {
        pergunta: "Você gostaria de passear com o pet?",
        respostas: [
            { texto: "Sim, todos os dias", valores: { energia: 3 }, especie: { cao: 2 } },
            { texto: "De vez em quando", valores: { energia: 2 }, especie: { cao: 1, gato: 1 } },
            { texto: "Prefiro não precisar", valores: { energia: 1 }, especie: { gato: 1, outro: 1 } }
        ]
    },
    {
        pergunta: "Você já teve algum pet antes?",
        respostas: [
            { texto: "Nunca tive", valores: { experiencia: 1 }, especie: {} },
            { texto: "Já tive cachorro", valores: { experiencia: 2 }, especie: { cao: 1 } },
            { texto: "Já tive gato", valores: { experiencia: 2 }, especie: { gato: 1 } },
            { texto: "Já tive outro tipo de animal", valores: { experiencia: 2 }, especie: { outro: 1 } },
            { texto: "Tenho bastante experiência, inclusive com animais resgatados", valores: { experiencia: 3 }, especie: {} }
        ]
    },
    {
        pergunta: "Você prefere um pet mais brincalhão?",
        respostas: [
            { texto: "Sim", valores: { energia: 3, temperamento: 3 }, especie: { cao: 1 } },
            { texto: "Tanto faz", valores: { energia: 2, temperamento: 2 }, especie: {} },
            { texto: "Prefiro um mais tranquilo", valores: { energia: 1 }, especie: { gato: 1 } }
        ]
    },
    {
        pergunta: "Quanto espaço você tem disponível?",
        respostas: [
            { texto: "Muito espaço", valores: { porte: 3 }, especie: { cao: 1 } },
            { texto: "Espaço médio", valores: { porte: 2 }, especie: { cao: 1, gato: 1 } },
            { texto: "Pouco espaço", valores: { porte: 1 }, especie: { gato: 1, outro: 1 } }
        ]
    },
    {
        pergunta: "Como você gostaria que o pet fosse com as pessoas?",
        respostas: [
            { texto: "Dócil e carinhoso, que busque colo e atenção", valores: { temperamento: 3 }, especie: { cao: 1 } },
            { texto: "Equilibrado, carinhoso quando quer", valores: { temperamento: 2 }, especie: { gato: 1 } },
            { texto: "Mais reservado, aceito ganhar a confiança dele aos poucos", valores: { temperamento: 1 }, especie: { gato: 1, outro: 1 } }
        ]
    },
    {
        pergunta: "Quanto tempo e dinheiro você pode dedicar a cuidados (veterinário, escovação, medicação)?",
        respostas: [
            { texto: "Poucos: quero um pet de rotina simples", valores: { cuidados: 1 }, especie: {} },
            { texto: "Moderados: o básico bem feito", valores: { cuidados: 2 }, especie: {} },
            { texto: "Muitos: aceito um pet com necessidades especiais", valores: { cuidados: 3 }, especie: {} }
        ]
    },
    {
        pergunta: "Qual característica você mais procura em um pet?",
        respostas: [
            { texto: "Companheirismo", valores: { temperamento: 3, independencia: 1 }, especie: { cao: 1 } },
            { texto: "Energia e diversão", valores: { energia: 3 }, especie: { cao: 1 } },
            { texto: "Independência e tranquilidade", valores: { independencia: 3, energia: 1 }, especie: { gato: 1, outro: 1 } }
        ]
    },
    {
        pergunta: "Tem crianças morando ou frequentando sua casa?",
        respostas: [
            { texto: "Sim", valores: {}, especie: {}, filtro: { criancas: 1 } },
            { texto: "Não", valores: {}, especie: {}, filtro: { criancas: 0 } }
        ]
    },
    {
        pergunta: "Você já tem outros pets em casa?",
        respostas: [
            { texto: "Sim", valores: {}, especie: {}, filtro: { outros_pets: 1 } },
            { texto: "Não", valores: {}, especie: {}, filtro: { outros_pets: 0 } }
        ]
    }
];


let perguntaAtual = 0;
let indicesEscolhidos = [];

function mostrarPergunta() {

    const pergunta = perguntas[perguntaAtual];

    document.getElementById("numeroPergunta").innerText =
        `Pergunta ${perguntaAtual + 1} de ${perguntas.length}`;

    let html = `
        <div class="pergunta">
            <h3>${pergunta.pergunta}</h3>
    `;

    pergunta.respostas.forEach((resposta, index) => {

        const selecionada =
            indicesEscolhidos[perguntaAtual] === index
                ? "selecionada"
                : "";

        html += `
            <button
                class="resposta ${selecionada}"
                onclick="selecionarResposta(${index})">
                ${resposta.texto}
            </button>
        `;
    });

    html += `</div>`;

    document.getElementById("pergunta").innerHTML = html;

    atualizarProgresso();

    document.getElementById("btnAnterior").style.display =
        perguntaAtual === 0 ? "none" : "block";

    document.getElementById("btnProxima").innerText =
        perguntaAtual === perguntas.length - 1
            ? "Ver meus pets"
            : "Próxima →";
}


function selecionarResposta(index) {

    indicesEscolhidos[perguntaAtual] = index;

    mostrarPergunta();
}


function proxima() {

    if (indicesEscolhidos[perguntaAtual] === undefined) {
        alert("Escolha uma resposta antes de continuar!");
        return;
    }

    if (perguntaAtual < perguntas.length - 1) {
        perguntaAtual++;
        mostrarPergunta();
    } else {
        enviarResultado();
    }
}


function anterior() {

    if (perguntaAtual > 0) {
        perguntaAtual--;
        mostrarPergunta();
    }
}


function atualizarProgresso() {

    const progresso =
        ((perguntaAtual + 1) / perguntas.length) * 100;

    document.getElementById("barraProgresso").style.width =
        progresso + "%";
}


function calcularPerfil() {

    const somas = {};
    const contagens = {};
    const votos = { cao: 0, gato: 0, outro: 0 };
    const filtros = { criancas: 0, outros_pets: 0 };

    indicesEscolhidos.forEach((indice, i) => {

        const resposta = perguntas[i].respostas[indice];

        Object.entries(resposta.valores || {}).forEach(([eixo, valor]) => {
            somas[eixo] = (somas[eixo] || 0) + valor;
            contagens[eixo] = (contagens[eixo] || 0) + 1;
        });

        Object.entries(resposta.especie || {}).forEach(([esp, pontos]) => {
            votos[esp] += pontos;
        });

        Object.entries(resposta.filtro || {}).forEach(([chave, valor]) => {
            filtros[chave] = valor;
        });
    });

    const perfil = {};
    Object.keys(somas).forEach(eixo => {
        perfil[eixo] = (somas[eixo] / contagens[eixo]).toFixed(2);
    });

    return { perfil, votos, filtros };
}


function enviarResultado() {

    const { perfil, votos, filtros } = calcularPerfil();

    const params = new URLSearchParams(perfil);
    params.set("v_cao", votos.cao);
    params.set("v_gato", votos.gato);
    params.set("v_outro", votos.outro);
    params.set("criancas", filtros.criancas);
    params.set("outros_pets", filtros.outros_pets);

    window.location.href = RESULTADO_URL + "?" + params.toString();
}


mostrarPergunta();
