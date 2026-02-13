# ARCHITECTURE.md

## 📐 Padrões Arquiteturais

- **Separação por pastas**:  
  - `models/` → cada entidade (Order, Customer, Product) com seu próprio arquivo.  
  - `serializers/` → cada recurso com seu serializer dedicado.  
  - `views/` → controladores separados por domínio.  
  - `services.py` → lógica principal concentrada no módulo de pedidos (Order).  

- **Service Layer**:  
  - A lógica de negócio foi extraída dos serializers e centralizada em `services.py`.  
  - Isso garante que os serializers cuidem apenas da transformação de dados, mantendo o princípio de responsabilidade única (SRP).

---

## 🔑 Decisões Técnicas

- **Foco no ERP**: endpoints implementados conforme o teste, sem autenticação/login, mas com validações adicionais e logs para proteger os endpoints.  
- **Logs estruturados**: adicionados para rastrear operações críticas e proteger endpoints contra uso indevido.  
- **Modelos completos**: preocupação com consultas eficientes e prevenção de erro N+1 (uso de `select_related` e `prefetch_related`).  
- **Tratamento de erros**: respostas padronizadas conforme solicitado (200, 201, 400, 404, 409, 500).  
- **Tests**: pasta `tests/` com três arquivos separados, cobrindo cada model (Customer, Product, Order).  

---

## ⚙️ Fluxo de Dados

1. **Request → View**: a requisição chega ao controller (view).  
2. **View → Service**: a view delega a lógica de negócio para o `services.py`.  
3. **Service → Model/Repository**: o service aplica regras de negócio e interage com os modelos.  
4. **Model → DB**: persistência no MySQL, com Redis usado para idempotência e rate limiting.  
5. **Response → Serializer → Output**: os dados são transformados pelos serializers e retornados ao cliente.  

---

## 📜 Trade-offs

- **Sem autenticação/login**: decisão consciente para focar nas regras de negócio descritas no teste.  
- **Service centralizado**: a lógica mais complexa está em `src/orders/services.py`, o que simplifica manutenção, mas concentra responsabilidade em um único arquivo.  
- **Validações extras**: compensam a ausência de autenticação, garantindo integridade dos dados.  
- **Logs**: aumentam a segurança e rastreabilidade, mas podem gerar overhead em ambientes de alta carga.  

---

## 🧪 Testes

- **Unitários**: cobrindo regras de negócio críticas (estoque, status, idempotência).  
- **Integração**: simulando concorrência, atomicidade e idempotência.  
- **Estrutura**: três arquivos separados dentro de `tests/`, cada um focado em um model.  


## 🔮 Possíveis Evoluções Futuras

- **Autenticação e Autorização**  
  Implementar login com JWT ou OAuth2 para proteger os endpoints e controlar permissões de acesso.

- **CI/CD**  
  Configurar pipelines com GitHub Actions para build, testes e deploy automatizado.

- **Multi-ambiente**  
  Separar configurações para `dev`, `staging` e `prod`, garantindo consistência entre ambientes.

- **Observabilidade avançada**  
  Expandir logs estruturados com correlation IDs e integrar ferramentas de monitoramento (ex.: Prometheus, Grafana).

- **Escalabilidade**  
  Uso de filas (RabbitMQ, Kafka) para processar eventos de domínio em larga escala.