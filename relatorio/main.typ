#import "cover.typ": cover
#import "template.typ": *

#show: project

#cover(title: "Monitorização Distribuída de Redes", authors: (
  (name: "Fábio Magalhães", number: "A104365"), 
  (name: "André Pinto", number: "A104267"), 
  (name: "Gonçalo Costa", number: "A93309")), 
  "Dezembro, 2024")

#set page(numbering: "i", number-align: center)
#counter(page).update(1)

#heading(numbering: none, outlined: false)[Resumo]

O presente trabalho teve como objetivo desenvolver um sistema de monitorização distribuída de redes capaz de coletar métricas detalhadas sobre o desempenho de dispositivos e links, bem como notificar em tempo real sobre condições críticas.

O servidor central é responsável por coordenar os agentes, interpretar tarefas descritas em ficheiros JSON, e armazenar as métricas coletadas, utilizando os protocolos *NetTask* (baseado em UDP) e *AlertFlow* (baseado em TCP). Os agentes, por sua vez, executam tarefas de monitorização, como medições de latência, largura de banda e uso de recursos, reportando os dados ao servidor e enviando alertas em caso de anomalias. A modularidade do sistema foi assegurada por uma implementação organizada em ficheiros distintos, cobrindo funções específicas, como coleta de métricas, gestão de tarefas e comunicação.

O sistema foi testado em um ambiente simulado utilizando o emulador CORE, demonstrando eficácia na coleta e reporte de métricas, mesmo em cenários com múltiplos agentes. Limitações foram identificadas, como o controle simplificado de conexões no protocolo *AlertFlow*, que suporta até 5 conexões simultâneas sem uma lógica de redistribuição em casos de sobrecarga. No entanto, os resultados obtidos validam a confiabilidade e a escalabilidade do sistema para os cenários propostos.

Conclui-se que a solução desenvolvida cumpre os objetivos iniciais e apresenta um ponto de partida sólido para futuros aprimoramentos, como controle avançado de conexões, integração com plataformas de gestão de incidentes e suporte a um maior número de agentes.



\

*Área de Aplicação*: Desempenho e monitorização em Redes de Computadores

*Palavras-Chave*: Python, Camada de Transporte, Redes de Computadores, Socket, Desempenho

#show outline: it => {
    show heading: set text(size: 18pt)
    it
}

#{
  show outline.entry.where(level: 1): it => {
    v(5pt)
    strong(it)
  }

  outline(
    title: [Índice], 
    indent: true, 
  )
}

#v(-0.4em)
#outline(
  title: none,
  target: figure.where(kind: "attachment"),
  indent: n => 1em,
)

#outline(
  title: [Lista de Figuras],
  target: figure.where(kind: image),
)

#outline(
  title: [Lista de Tabelas],
  target: figure.where(kind: table),
)

// Make the page counter reset to 1
#set page(numbering: "1", number-align: center)
#counter(page).update(1)

#import "pages/mainPage.typ" as mainPage
#mainPage