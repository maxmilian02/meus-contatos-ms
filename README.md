# Meus Contatos MS - Teste Conecta Suite

Sistema de organização de contatos da Microsoft por domínio de e-mail.

**Stack:** Vue.js 3, Flask, MSAL, TailwindCSS

## 🚀 Setup Rápido

### 1. Configuração do Azure AD

1. Acesse [Azure Portal](https://portal.azure.com/)
2. Vá para "Registros de aplicativo" → "Novo registro"
3. Configure:
   * **Nome:** Meus Contatos MS
   * **Tipos de conta:** Contas pessoais e organizacionais
   * **URI de Redirecionamento (Web):** `http://localhost:5000/auth/login/callback`
4. Anote o **ID do Aplicativo (cliente)**
5. Em "Certificados & segredos" → Criar **Novo segredo do cliente**
6. Copie o **Valor** (não o ID)

### 2. Backend (Flask)

```bash
cd backend

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Criar arquivo .env
cp .env.example .env
# Edite .env com suas credenciais

# Gerar chave secreta forte
python -c "import secrets; print(secrets.token_hex(32))"
# Cole no SECRET_KEY do .env

# Iniciar servidor
flask run
```

O backend estará em `http://localhost:5000`

### 3. Frontend (Vue.js)

```bash
cd frontend/vue-project

# Instalar dependências
npm install

# Criar arquivo de ambiente
echo "VITE_API_URL='http://localhost:5000'" > .env.local

# Iniciar servidor de desenvolvimento
npm run dev
```

O frontend estará em `http://localhost:5173`

## 🧪 Testando

1. Acesse `http://localhost:5173`
2. Clique em "Entrar com Microsoft"
3. Faça login com sua conta Microsoft
4. Autorize o aplicativo
5. Você será redirecionado para `/contatos` com seus contatos agrupados

## 📋 Checklist de Validação

* [X] Backend rodando sem erros
* [X] Frontend conectando ao backend
* [X] Login redirecionando para Microsoft
* [X] Callback retornando sem "state_mismatch"
* [X] Contatos sendo listados e agrupados
* [ ] Logout funcionando corretamente

## 🐛 Troubleshooting

### "state_mismatch"

* ✅ Corrigido na versão atual

### "not_authenticated"

* Verifique se o cookie de sessão está sendo enviado (`credentials: 'include'`)
* Confirme que `FRONTEND_URL` está correto no `.env`

### "CORS error"

* Verifique se `FRONTEND_URL` no backend corresponde à URL do frontend
* Confirme que o backend tem `supports_credentials=True`

### Redirecionamento infinito

* Limpe os cookies do navegador
* Verifique se `/contatos` não está em loop com a guard de autenticação

## 📦 Deploy

### Backend (Google Cloud Run)

```bash
# Build da imagem
docker build -t meus-contatos-backend .

# Deploy
gcloud run deploy meus-contatos-backend \
  --image gcr.io/SEU_PROJETO/meus-contatos-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars MS_CLIENT_ID=xxx,MS_CLIENT_SECRET=yyy,SECRET_KEY=zzz
```

**Importante:** Atualize o `MS_REDIRECT_URI` no Azure para a URL do Cloud Run

### Frontend (Firebase Hosting)

```bash
cd frontend/vue-project

# Build de produção
npm run build

# Deploy
firebase deploy --only hosting
```

**Importante:** Atualize `VITE_API_URL` para a URL do backend em produção

## 🎯 Melhorias Implementadas

1. **Segurança:**
   * Validação estrita do state OAuth2
   * Configuração adequada de cookies de sessão
   * CORS configurado com origins específicas
2. **UX:**
   * Loading states em todas as operações
   * Tratamento de erros com mensagens claras
   * Design responsivo com Tailwind CSS 4
3. **Código:**
   * Separação de concerns (blueprints, stores, services)
   * Tratamento de erros robusto
   * Comentários e documentação
