<div align="center">
  <img
    src="https://github.com/user-attachments/assets/86857d1b-7af4-4d56-8c77-2ad2bcb917a3"
    width="672"
    height="448"
    alt="ShiftFlow logo"
  />
</div>

<p align="center">
  <strong>Automated Workforce Scheduling & Shift Coordination Platform</strong><br/>
  <em>Plataforma de Criação Automática de Horários e Coordenação de Turnos Hospitalares</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Frontend-HTML%20%7C%20JS%20%7C%20CSS-0B5FA5" />
  <img src="https://img.shields.io/badge/Backend-Python%20(FastAPI)-0B5FA5?logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Database-SQLite-16B8A6" />
  <img src="https://img.shields.io/badge/Output-Excel%20%7C%20PDF-16B8A6" />
  <img src="https://img.shields.io/badge/License-MIT-6B7280" />
  <img src="https://img.shields.io/badge/Status-Concept%20%2F%20Demo-6B7280" />
</p>

---

<details open>
<summary><strong>🇬🇧 English</strong></summary>

<br/>

> ⚠️ **Disclaimer**
>
> ShiftFlow is a **conceptual / demonstration project**.
> It is designed to support **hospital workforce scheduling and coordination workflows**.
>
> It must **not** be used as a sole operational planning system without appropriate
> validation, legal compliance, and mandatory human oversight.

---

## Overview

**ShiftFlow** is a hospital-focused operational platform that supports the **full lifecycle
of shift planning and coordination**, not just schedule generation.

Designed from a **nursing coordination and clinical operations perspective**, ShiftFlow
reflects the real-world complexity of managing hospital rosters while keeping
human validation at the center of all decisions.

The platform combines **automated scheduling logic** with **coordination workflows**
required for day-to-day hospital operations.

---

## Intended Audience

- Nurse managers and nurse coordinators
- Hospital unit leadership
- Clinical operations and staffing teams
- Workforce planning and health IT professionals

---

## Core Scheduling Capabilities

- **Automated shift generation** based on explicit rules and constraints
- **Labour-rule enforcement** (weekly limits, rest periods, night rules)
- **Balanced distribution** of workload, nights, and weekends
- **Conflict detection** with clear reporting of unmet constraints
- **Template-based schedules** per hospital unit

---

## Extended Operational Capabilities

ShiftFlow goes beyond schedule generation by supporting the surrounding
**coordination and management workflows**, including:

- **Team and role management** per hospital unit
- **Availability, leave, and absence management**
- **Shift swap and change requests** initiated by staff
- **Coordinator review and approval workflows**
- **Contextual communication** (comments or chat linked to schedules or requests)
- **Schedule versioning and traceability** of changes
- **Distribution of final schedules** to staff

All operational actions remain **subject to coordinator validation**.

---

## What ShiftFlow Does NOT Do

- It does not replace human coordination or leadership
- It does not make clinical staffing decisions
- It does not assess professional competencies
- It does not guarantee a solution when constraints are incompatible

---

## Architecture Overview

```
Frontend (HTML / JS / CSS)
        ↓ REST API
Backend (Python / FastAPI)
        ↓ Scheduling Logic / Solver
Database (SQLite)
        ↓
Exports & Coordination Workflows
        ↓
Excel / PDF
```

---

## Design Principles

- Hospital-first design
- Decision-support, not decision replacement
- Explicit and transparent rules
- Human validation at every critical step
- Alignment with nursing coordination practice

---
## Demo Access

The WalkFlow demo environment includes **preconfigured demo accounts** to explore the platform features.

> ⚠️ **Important**
>
> These credentials are **for demonstration purposes only**.
> They do **not** contain real staff data and must **never** be used in production environments.

### Demo Accounts

| Role | Username | Password |
|---|---|---|
| Administrator | `admin` | `123456` |

Role-based access control (RBAC) is enforced, and each profile exposes different operational capabilities.

---

## License

MIT License.  
Free to use, modify, and learn from.  
Not intended for production hospital use without appropriate validation.

</details>

---

<details>
<summary><strong>🇵🇹 Português (Portugal)</strong></summary>

<br/>

> ⚠️ **Aviso Importante**
>
> O ShiftFlow é um **projeto conceptual / de demonstração**.
> Destina-se a apoiar **processos de criação de horários e coordenação de turnos em contexto hospitalar**.
>
> Não deve ser utilizado como sistema único de planeamento real sem validação,
> conformidade legal e supervisão humana obrigatória.

---

## Visão Geral

O **ShiftFlow** é uma plataforma operacional orientada para o **ciclo completo
de planeamento e coordenação de horários hospitalares**, indo além da simples
geração automática de escalas.

Foi concebido a partir da **perspetiva da coordenação de enfermagem e das operações clínicas**,
refletindo a complexidade real da gestão de equipas hospitalares, mantendo sempre
a validação humana como elemento central.

---

## Destinatários

- Enfermeiros coordenadores
- Chefias intermédias de enfermagem
- Direções de unidades hospitalares
- Equipas de operações clínicas e planeamento

---

## Capacidades Principais de Planeamento

- **Criação automática de horários** com base em regras explícitas
- **Cumprimento de regras laborais** (limites, descansos, noites)
- **Distribuição equilibrada** de carga horária, noites e fins de semana
- **Identificação de conflitos** e regras não satisfeitas
- **Modelos de horários reutilizáveis** por unidade hospitalar

---

## Capacidades Operacionais Alargadas

Para além da geração de horários, o ShiftFlow suporta os principais
**fluxos de coordenação hospitalar**, incluindo:

- **Gestão de equipas e perfis funcionais**
- **Registo de disponibilidades, férias e ausências**
- **Pedidos de troca ou alteração de turnos**
- **Fluxos de validação pelo enfermeiro coordenador**
- **Comunicação contextual** associada a horários e pedidos
- **Versionamento e rastreabilidade** das alterações
- **Distribuição dos horários finais** às equipas

Todas as ações estão **dependentes de validação humana**.

---

## O que o ShiftFlow NÃO faz

- Não substitui a coordenação humana
- Não decide adequação clínica de profissionais
- Não elimina conflitos organizacionais
- Não garante solução quando regras são incompatíveis

---

## Princípios de Design

- Pensado exclusivamente para contexto hospitalar
- Apoio à decisão, não substituição
- Transparência total das regras
- Supervisão humana obrigatória
- Alinhamento com práticas reais de coordenação de enfermagem

---

## Acesso Demo

O ambiente de demonstração do WalkFlow inclui **contas de acesso pré-configuradas** para exploração das funcionalidades da plataforma.

> ⚠️ **Aviso Importante**
>
> Estas credenciais destinam-se **exclusivamente a fins de demonstração**.
> Não contêm dados reais de colaboradores e **não devem ser utilizadas em ambiente produtivo**.

### Contas de Demonstração

| Perfil | Utilizador | Palavra-passe |
|---|---|---|
| Administrador | `admin` | `123456` |

O controlo de acessos por perfil (RBAC) encontra-se ativo, estando cada utilizador limitado às permissões do respetivo papel.

---

## Licença

Licença MIT.  
Projeto educativo e conceptual.  
Não destinado a utilização hospitalar em produção sem validação adequada.

</details>

---

## Contact

- **Name:** Nuno da Silva Magalhães  
- **Background:** Nursing & Clinical Operations  
- **GitHub:** https://github.com/NunoSid  
- **LinkedIn:** https://www.linkedin.com/in/nuno-da-silva-magalhães-421253199
