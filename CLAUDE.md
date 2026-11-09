# BUDO Timer: contexto do projeto

Timer de rounds para jiu-jitsu, criado para a TV da academia onde a dona do projeto treina, e também usado no celular. Gratuito, sem servidor e sem custo de hospedagem.

## Como responder

- Conversa em português (Brasil). Nos textos para a pessoa, não usar travessões.
- A pessoa não é desenvolvedora: explicar passo a passo, com o caminho exato de cada clique e cada comando.
- Mostrar com prints/testes antes de dizer que algo funciona. Depois de cada mudança: gerar as duas versões, testar e enviar para o GitHub.

## Estrutura

| Caminho | O que é |
|---|---|
| `src/budo-timer.html` | Código único (HTML, CSS e JS num arquivo). Toda mudança começa aqui. |
| `build_tv.py` | Gera `tizen/index.html` para a TV Samsung. |
| `build_web.py` | Gera `docs/` (app do celular, PWA publicado pelo GitHub Pages). |
| `tizen/` | `index.html`, `config.xml` (id `BudoTimr01.BudoTimer`) e `icon.png`. |
| `docs/` | `index.html`, `manifest.webmanifest`, `sw.js` e ícones. Publicado em https://rubensvbarbosa.github.io/BUDOTimer/ |

Depois de editar `src/budo-timer.html`, sempre rodar `python3 build_tv.py` e `python3 build_web.py` e enviar `src/`, `tizen/` e `docs/` juntos.

## Restrições da TV (importante)

A TV de casa é uma Samsung UE43RU7025 (2019, Tizen 5.0, Chromium antigo). Ela não entende `clamp()`, `min()`, `max()`, `env()` nem `gap` em flexbox. O `build_tv.py` troca essas funções por valores fixos para 1920x1080 e cria margens no lugar do `gap` (classe `no-fgap`). Não deixar a versão original junto: numa regra com `var()`, a TV aceita na leitura e descarta na hora de aplicar, apagando a reserva.

JavaScript: manter ES5 (sem `=>`, `let`, `const`, crases).

## Decisões de produto já tomadas

- Navegação por foco com as setas e OK do controle (estilo Netflix), nunca cursor. Números 1 a 9 trocam o treino. Voltar fecha o app quando o timer está parado.
- Visual: fundo grafite neutro (sem azul), timer grande no centro, faixa com os graus como contador de rounds, horário local num cartão com mostrador analógico embaixo do nome BUDO Timer.
- Fonte atual: Big Shoulders Display (números e títulos) e Barlow Semi Condensed (textos). Existe uma página comparando com Barlow e Saira, caso queiram trocar.
- Treinos padrão por faixa com os tempos de luta da IBJJF para adultos (branca 5, azul 6, roxa 7, marrom 8, preta 10 min) e Drill. Descanso e rounds são sugestões.
- Treinos criados pelo usuário: nome, tempo, descanso, rounds e cor da faixa. Editados e excluídos em Ajustes (só os criados podem ser excluídos).
- Em Treinos: 1º OK seleciona, 2º OK no mesmo treino volta ao timer.
- Ajustes: só valem depois de Salvar. Duas colunas (treino selecionado | apitos e som). Restaurar padrão volta às faixas da IBJJF e não apaga os treinos criados.
- Apitos: "pi" a cada segundo nos últimos N segundos (padrão 5) de qualquer tempo (preparação, luta, descanso) e um apito longo no fim de cada tempo; dois apitos longos no fim do treino. Tipos: Clássico, Digital, Suave, Grave, Sino. A amostra anterior para quando outra começa.
- Idioma: botão pequeno PT | EN no canto superior direito da tela inicial. Some durante o round junto com os outros botões. Primeira abertura usa o idioma do aparelho.
- Durante o round, os botões somem depois de 4 s. No celular eles saem do layout e o timer cresce; um toque traz os botões de volta sem pausar. Tocar no relógio inicia e pausa.
- Celular sempre deitado; em pé aparece "Gire o celular". Sem destaque de "botão selecionado" no toque.

## Atualizar a TV

1. Copiar `tizen/index.html` para `C:\Users\ruben\workspace\BudoTimer` (substituir).
2. Tizen Studio: botão direito no projeto > Refresh > Build Signed Package.
3. Prompt de Comando, com a TV ligada e o app fechado:

```
C:\tizen-studio\tools\sdb.exe connect 192.168.1.162
cd /d C:\Users\ruben\workspace\BudoTimer
C:\tizen-studio\tools\ide\bin\tizen.bat install -n BudoTimer.wgt -s 192.168.1.162:26101
```

`sdb.exe install` NÃO instala em TV Samsung (só copia). "Run As" no Tizen Studio tenta desinstalar antes e pode falhar se o app estiver aberto, além de apagar os dados salvos na TV.

Certificado Samsung: perfil "BudoTimer", em `C:\Users\ruben\SamsungCertificate\BudoTimer`. Nunca enviar para o GitHub (o `.gitignore` bloqueia `.p12`, `.wgt` e a pasta do certificado).

## TV da academia (pendente)

A TV da academia é uma **TCL Premium QLED** (marca e selo vistos em fotos em 9/11/2026). Falta confirmar o modelo e o sistema: na próxima ida à academia, foto da tela inicial ou de Definições > Sistema > Acerca de.

Se for Google TV / Android TV (o mais provável para TCL QLED em Portugal), o plano é:
- Criar um app Android para TV (APK com WebView, Leanback, tela sempre acesa) carregando o `src/budo-timer.html`, compilado de graça pelo GitHub Actions e publicado como Release no repositório.
- Na TV: instalar o app **Downloader** pela Play Store, permitir "fontes desconhecidas" para ele, digitar o endereço do APK e instalar. Sem computador, sem modo desenvolvedor, sem certificado.
- Conferir no WebView: setas e OK chegam como teclas 37 a 40 e 13; tecla Voltar do Android precisa ser tratada (fechar camadas e sair do app); teclas de mídia podem chegar como 179.

O plano antigo (notebook emprestado + Tizen) só vale se a TV for Samsung.

## Ideias para depois

- Logo ou nome da academia na tela.
- Apresentação para o dono da academia.
- Monetizar no futuro (aí avaliar repositório privado e outra hospedagem).
