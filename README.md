# BUDO Timer

Timer de rounds para jiu-jitsu. Roda na TV (só com o controle remoto) e no celular, com a tela deitada, como app instalado.

**Versão:** 1.0.0

## O que tem

- Treinos por faixa com os tempos de luta da IBJJF para adultos (branca 5 min, azul 6, roxa 7, marrom 8, preta 10) e um Drill.
- Treinos criados por você, com nome, tempo de luta, descanso, rounds e cor da faixa.
- Ajustes do treino selecionado (tempo de luta, descanso e rounds) e botão para restaurar o padrão.
- Apitos nos últimos segundos de cada tempo e um apito longo no fim, com cinco tipos de apito.
- Horário local no canto da tela.
- Navegação com as setas e o OK do controle; os números 1 a 9 trocam o treino.

## Pastas

| Pasta / arquivo | Para que serve |
|---|---|
| `src/budo-timer.html` | Versão principal. Abre em qualquer navegador moderno e é onde as mudanças são feitas. |
| `tizen/` | App da TV Samsung: `index.html`, `config.xml` e `icon.png`. |
| `docs/` | App do celular, publicado pelo GitHub Pages. |
| `build_tv.py` | Gera `tizen/index.html` a partir de `src/budo-timer.html`, com ajustes para TVs Samsung antigas (2019 ou anteriores). |
| `build_web.py` | Gera a pasta `docs/` a partir de `src/budo-timer.html` (precisa do Pillow para os ícones: `pip install pillow`). |
| `android/` e `build_android.py` | App para TVs Android / Google TV, compilado pelo GitHub Actions. |

## Celular

### Publicar (uma vez)

1. Suba o projeto para um repositório no GitHub.
2. No repositório, vá em **Settings > Pages**.
3. Em **Source**, escolha **Deploy from a branch**. Em **Branch**, escolha `main` e a pasta `/docs`. Clique em **Save**.
4. Em um ou dois minutos, o endereço aparece no topo da página, por exemplo `https://<seu-usuario>.github.io/budo-timer/`.

### Instalar no celular

- **Android (Chrome):** abra o endereço, toque no menu ⋮ e escolha **Instalar app** (ou **Adicionar à tela inicial**).
- **iPhone (Safari):** abra o endereço, toque em **Compartilhar** e escolha **Adicionar à Tela de Início**.

O ícone do BUDO Timer aparece na tela inicial. Ele abre em tela cheia, funciona sem internet depois da primeira vez e atualiza sozinho quando uma versão nova sobe para o GitHub.

### Dicas

- Use o celular deitado. Em pé, aparece um aviso para girar. No iPhone, desligue o **bloqueio de rotação** na Central de Controle.
- Tocar no relógio grande inicia e pausa o timer.
- A tela não apaga durante o treino (depende do navegador; no iPhone, iOS 16.4 ou mais novo).
- No iPhone com iOS 17 ou mais novo, os apitos tocam mesmo com a chave do silencioso ligada. Em versões antigas, desligue o silencioso.

### Atualizar o app do celular

1. Faça a mudança em `src/budo-timer.html`.
2. Rode `python3 build_web.py` (no Windows, `py build_web.py`).
3. Suba as mudanças para o GitHub. Na próxima vez que o app abrir com internet, ele pega a versão nova.

## TV Android / Google TV (TCL, Sony, Philips, Xiaomi...)

O GitHub gera o app sozinho (`BudoTimer.apk`) sempre que `src/` ou `android/` mudam, pelo GitHub Actions (aba **Actions**, "App para TV Android"). O arquivo fica em **Releases**, na versão "tv".

### Instalar na TV (uma vez)

1. Na TV, abra a **Play Store** (Google Play), procure **Downloader** (ícone laranja, da AFTVnews) e instale.
2. Vá em **Definições > Sistema > Programador / Opções de programador**, ou em **Definições > Apps > Segurança e restrições > Fontes desconhecidas**, e autorize o **Downloader** a instalar apps. Em muitas TVs, o próprio Downloader pede essa permissão na primeira instalação e leva direto à tela certa.
3. Abra o Downloader e, no campo de endereço, digite: `rubensvbarbosa.github.io/BUDOTimer/tv`
4. Na página que abrir, aperte OK em **Baixar para a TV** e depois em **Instalar**.
5. O BUDO Timer aparece em **Apps** (e pode ser fixado na tela inicial).

### Atualizar

Repita os passos 3 e 4. A versão nova instala por cima e mantém os treinos e ajustes salvos.

### Detalhes técnicos

- `build_android.py` copia `src/budo-timer.html` para `android/app/src/main/assets/index.html`.
- O app é um WebView em tela cheia (`app.budotimer.tv`), com a tela sempre acesa. O botão Voltar chama `window.budoBack()` na página: fecha janelas, mostra os botões durante o round e, com o timer parado, sai do app.
- A chave de assinatura (`android/budo-timer.keystore`, senha `budotimer`) fica no repositório de propósito: as atualizações precisam ser assinadas sempre com a mesma chave. Não é um segredo; serve só para este app.

## Atualizar o app da TV Samsung depois de mudar o código

1. Faça a mudança em `src/budo-timer.html`.
2. Na pasta do projeto, rode `python3 build_tv.py` (no Windows, `py build_tv.py`).
3. Copie `tizen/index.html` (e `config.xml` ou `icon.png`, se mudaram) para a pasta do projeto no Tizen Studio, por exemplo `C:\Users\<você>\workspace\BudoTimer`.
4. No Tizen Studio: botão direito no projeto, **Refresh** e depois **Build Signed Package** (gera o `BudoTimer.wgt` nessa pasta).
5. Com a TV ligada e o app fechado nela, instale por cima da versão antiga pelo Prompt de Comando. Assim a TV mantém os treinos e ajustes salvos:

```
C:\tizen-studio\tools\sdb.exe connect <IP da TV>
cd /d C:\Users\<você>\workspace\BudoTimer
C:\tizen-studio\tools\ide\bin\tizen.bat install -n BudoTimer.wgt -s <IP da TV>:26101
```

Atenção: em TV Samsung, `sdb.exe install` só copia o arquivo e não instala. Use o `tizen.bat install`.

Depois, feche o app na TV (botão Voltar com o timer parado) e abra de novo pelo menu Apps.

## Instalar numa TV Samsung nova

1. Instale o Tizen Studio com **TV Extensions** e **Samsung Certificate Extension** (aba Extension SDK do Package Manager).
2. Na TV: Apps, digitar `12345`, ligar **Developer Mode** com o IP do computador e reiniciar a TV.
3. Conectar: `C:\tizen-studio\tools\sdb.exe connect <IP da TV>`.
4. Certificate Manager: perfil Samsung > TV, com o código (DUID) da TV na lista do distribuidor. Para ver o DUID de uma TV conectada: `sdb.exe shell 0 getduid`.
5. Criar o projeto (Template > TV > Web Application > Basic Project), copiar os três arquivos de `tizen/` por cima e rodar **Run As > Tizen Web Application** (ou **Build Signed Package** e o `tizen.bat install` acima).

## Importante

- **Nunca envie para o GitHub os certificados** (pasta `SamsungCertificate`, arquivos `.p12`) nem a senha deles. O `.gitignore` já bloqueia esses arquivos.
- Guarde uma cópia do certificado e da senha fora do computador. Sem eles, para atualizar o app é preciso apagá-lo da TV e instalar de novo.
