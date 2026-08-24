const perguntas = [
    {
        pergunta: "Onde você mora?",
        respostas: [
            { texto: "Casa com quintal", tipo: "cao" },
            { texto: "Casa sem quintal", tipo: "cao" },
            { texto: "Apartamento", tipo: "gato" }
        ]
    },

    {
        pergunta: "Quanto tempo você passa em casa?",
        respostas: [
            { texto: "Quase o dia todo", tipo: "cao" },
            { texto: "Boa parte do dia", tipo: "cao" },
            { texto: "Passo pouco tempo em casa", tipo: "gato" }
        ]
    },

    {
        pergunta: "Como é sua rotina?",
        respostas: [
            { texto: "Muito ativa", tipo: "cao" },
            { texto: "Moderadamente ativa", tipo: "cao" },
            { texto: "Mais tranquila", tipo: "gato" }
        ]
    },

    {
        pergunta: "Você gosta de fazer atividades ao ar livre?",
        respostas: [
            { texto: "Sim, bastante", tipo: "cao" },
            { texto: "Às vezes", tipo: "cao" },
            { texto: "Prefiro ficar em casa", tipo: "gato" }
        ]
    },

    {
        pergunta: "Quanto tempo você teria para brincar com o pet?",
        respostas: [
            { texto: "Várias horas", tipo: "cao" },
            { texto: "Algumas horas", tipo: "cao" },
            { texto: "Pouco tempo", tipo: "gato" }
        ]
    },

    {
        pergunta: "Você prefere um pet mais independente?",
        respostas: [
            { texto: "Sim", tipo: "gato" },
            { texto: "Não", tipo: "cao" },
            { texto: "Não tenho preferência", tipo: "cao" }
        ]
    },

    {
        pergunta: "Como você se sente com barulho?",
        respostas: [
            { texto: "Não me incomoda", tipo: "cao" },
            { texto: "Prefiro ambientes tranquilos", tipo: "gato" }
        ]
    },

    {
        pergunta: "Você gostaria de passear com o pet?",
        respostas: [
            { texto: "Sim, gostaria", tipo: "cao" },
            { texto: "Prefiro não precisar", tipo: "gato" }
        ]
    },

    {
        pergunta: "Você já teve algum pet antes?",
        respostas: [
            { texto: "Sim, cachorro", tipo: "cao" },
            { texto: "Sim, gato", tipo: "gato" },
            { texto: "Nunca tive", tipo: "gato" }
        ]
    },

    {
        pergunta: "Você prefere um pet mais brincalhão?",
        respostas: [
            { texto: "Sim", tipo: "cao" },
            { texto: "Prefiro um mais tranquilo", tipo: "gato" }
        ]
    },

    {
        pergunta: "Quanto espaço você tem disponível?",
        respostas: [
            { texto: "Muito espaço", tipo: "cao" },
            { texto: "Espaço médio", tipo: "cao" },
            { texto: "Pouco espaço", tipo: "gato" }
        ]
    },

    {
        pergunta: "Qual característica você mais procura em um pet?",
        respostas: [
            { texto: "Companheirismo", tipo: "cao" },
            { texto: "Energia e diversão", tipo: "cao" },
            { texto: "Independência e tranquilidade", tipo: "gato" }
        ]
    }
];


let perguntaAtual = 0;
let respostasEscolhidas = [];
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
                onclick="selecionarResposta('${resposta.tipo}', ${index})">
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
            ? "Finalizar"
            : "Próxima →";
}


function selecionarResposta(tipo, index) {

    respostasEscolhidas[perguntaAtual] = tipo;
    indicesEscolhidos[perguntaAtual] = index;

    mostrarPergunta();
}


function proxima() {

    if (!respostasEscolhidas[perguntaAtual]) {
        alert("Escolha uma resposta antes de continuar!");
        return;
    }

    if (perguntaAtual < perguntas.length - 1) {
        perguntaAtual++;
        mostrarPergunta();
    } else {
        mostrarResultado();
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


function mostrarResultado() {

    let pontosCao = 0;
    let pontosGato = 0;

    respostasEscolhidas.forEach(resposta => {

        if (resposta === "cao") {
            pontosCao++;
        } else {
            pontosGato++;
        }
    });

    let resultado;

    if (pontosCao > pontosGato) {

        resultado = `
            <div class="resultado">
                <h2>Seu resultado!</h2>
                <h1>Cão</h1>
                <p>
                    Pela suas respostas, um cão pode combinar mais
                    com a sua rotina.
                </p>

                <button class="btn btn-success" onclick="location.reload()">
                    Refazer quiz
                </button>
            </div>
        `;

    } else {

        resultado = `
            <div class="resultado">
                <h2>Seu resultado!</h2>
                <h1>Gato</h1>
                <p>
                    Pelas suas respostas, um gato pode combinar mais
                    com a sua rotina.
                </p>

                <button class="btn btn-success" onclick="location.reload()">
                    Refazer quiz
                </button>
            </div>
        `;
    }

    document.getElementById("pergunta").innerHTML = resultado;

    document.getElementById("numeroPergunta").style.display = "none";
    document.querySelector(".botoes").style.display = "none";
    document.querySelector(".progresso").style.display = "none";
}


mostrarPergunta();