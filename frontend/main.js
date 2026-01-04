const state = {
  month: new Date().getMonth() + 1,
  year: new Date().getFullYear(),
  meta: null,
  serviceMap: {},
  config: null,
  nurses: [],
  requirements: [],
  constraints: [],
  scheduleEntries: [],
  unfilled: [],
  violations: [],
  holidays: [],
  manualHolidays: [],
  adjustments: [],
  scheduleStats: [],
  settings: null,
  user: null,
  token: null,
  users: [],
  adminUsers: [],
  teams: [],
  teamMembers: {},
  services: [],
  shifts: [],
  releases: [],
  chatThreads: [],
  chatMessages: [],
  swaps: [],
  activeChatPeerId: null,
  group: "ENFERMEIRO",
  myAvailabilityRequests: [],
  pendingAvailabilityRequests: [],
  myAvailabilityConstraints: [],
  categoriesAdmin: [],
};

state.lang = localStorage.getItem("shiftflow_lang") || "pt";

const I18N = {
  pt: {
    "lang.pt": "Português",
    "lang.en": "Inglês",
    "app.subtitle": "Gestao de turnos e horarios",
    "action.logout": "Sair",
    "label.month": "Mês",
    "label.year": "Ano",
    "label.team": "Equipa",
    "group.enf": "Enfermagem",
    "group.ao": "Assistentes Operacionais",
    "nav.dashboard": "Dashboard",
    "nav.nurses": "Profissionais",
    "nav.requirements": "Necessidades",
    "nav.constraints": "Disponibilidades",
    "nav.rules": "Regras",
    "nav.teams": "Equipas",
    "nav.services": "Serviços/Turnos",
    "nav.schedule": "Horário",
    "nav.swaps": "Trocas",
    "nav.chat": "Chat",
    "nav.admin": "Admin",
    "dashboard.generate": "Gerar horário",
    "dashboard.export_schedule": "Exportar horário",
    "dashboard.export_constraints": "Exportar disponibilidades",
    "dashboard.needs": "Necessidades",
    "dashboard.assigned": "Turnos atribuídos",
    "dashboard.locks": "Locks ativos",
    "dashboard.alerts": "Alertas",
    "section.dashboard": "Dashboard",
    "section.nurses": "Profissionais",
    "section.requirements": "Necessidades do mês",
    "section.constraints": "Disponibilidades / Pedidos",
    "section.rules": "Regras do Mês",
    "section.schedule": "Horário do mês",
    "section.teams": "Equipas de serviço",
    "section.services": "Serviços e turnos",
    "section.swaps": "Trocas de turno",
    "section.chat": "Chat",
    "section.admin": "Administração",
    "btn.add": "Adicionar",
    "btn.add_professional": "Adicionar profissional",
    "btn.edit": "Editar",
    "btn.save": "Guardar",
    "btn.update": "Atualizar",
    "btn.close": "Fechar",
    "btn.clear": "Limpar",
    "btn.apply": "Aplicar",
    "btn.associate": "Associar",
    "btn.cancel": "Cancelar",
    "btn.delete": "Eliminar",
    "btn.activate": "Ativar",
    "btn.deactivate": "Desativar",
    "btn.archive": "Arquivar",
    "btn.publish": "Publicar",
    "btn.generate": "Gerar horário",
    "btn.export": "Exportar",
    "btn.send": "Enviar",
    "btn.approve": "Aprovar",
    "btn.reject": "Rejeitar",
    "btn.accept": "Aceitar",
    "btn.decline": "Recusar",
    "btn.create_team": "Criar equipa",
    "btn.add_member": "Guardar membros",
    "btn.fill_all": "Preencher tudo com 1",
    "btn.clear_all": "Limpar tudo",
    "btn.save_requirements": "Guardar necessidades",
    "btn.save_constraints": "Guardar marcações",
    "btn.available_all": "Disponível em todos",
    "btn.unavailable_all": "Indisponível em todos",
    "btn.submit_availability": "Enviar para aprovação",
    "btn.save_rules": "Guardar regras",
    "btn.add_holiday": "Adicionar",
    "btn.save_adjustments": "Guardar ajustes",
    "btn.clear_schedule": "Apagar horário selecionado",
    "label.professional": "Profissional",
    "label.edit_professional": "Editar",
    "label.new_professional": "Novo profissional",
    "label.user": "Utilizador",
    "label.services": "Serviços",
    "label.weekly_hours": "Horas semanais",
    "label.balance": "Saldo (h)",
    "label.actions": "Ações",
    "label.order": "Ordem",
    "label.yes": "Sim",
    "label.no": "Não",
    "label.category": "Categoria",
    "label.user_active": "Utilizador ativo",
    "label.category_active": "Ativa",
    "label.action": "Ação",
    "label.participants": "Participantes",
    "label.can_night": "Pode fazer noite?",
    "label.max_nights": "Máx. noites/mês",
    "label.services_allowed": "Serviços permitidos",
    "label.service": "Serviço",
    "label.role": "Perfil",
    "label.status": "Estado",
    "label.code": "Código",
    "label.name": "Nome",
    "label.color": "Cor",
    "label.shift": "Turno",
    "label.shift2": "Turno 2 (opcional)",
    "label.shift3": "Turno 3 (opcional)",
    "label.type": "Tipo",
    "label.start": "Início",
    "label.end": "Fim",
    "label.date": "Dia",
    "label.description": "Descrição",
    "label.manual_holidays": "Feriados manuais",
    "label.holidays": "Feriados do mês",
    "label.adjustments": "Feriados trabalhados / ajustes manuais",
    "label.schedule_stats": "Horas por profissional",
    "label.unfilled": "Cobertura em falta",
    "label.violations": "Violações / Alertas",
    "label.publish_schedule": "Publicar horário",
    "label.schedule_tools": "Gestão de horários",
    "label.export_swaps": "Exportar trocas",
    "label.swap_request": "Pedir troca",
    "label.swap_requests": "Pedidos",
    "label.chat_users": "Utilizadores",
    "label.chat_threads": "Conversas",
    "placeholder.search_user": "Procurar utilizador...",
    "placeholder.role": "Perfil",
    "placeholder.chat_message": "Escreva a mensagem...",
    "placeholder.name": "Nome",
    "placeholder.username": "Username",
    "placeholder.team_name": "Nome da equipa",
    "placeholder.service_code": "Código do serviço",
    "placeholder.shift_code": "Código",
    "placeholder.shift_label": "Etiqueta",
    "placeholder.service_name": "Nome",
    "placeholder.category_name": "Nome da categoria",
    "placeholder.order": "Ordem (opcional)",
    "placeholder.reason_optional": "Motivo (opcional)",
    "placeholder.observations_optional": "Observações (opcional)",
    "placeholder.swap_service": "Serviço atual (opcional)",
    "placeholder.swap_shift": "Turno atual (opcional)",
    "placeholder.swap_desired_service": "Serviço pretendido (opcional)",
    "placeholder.swap_desired_shift": "Turno pretendido (opcional)",
    "placeholder.full_name": "Nome completo",
    "placeholder.password": "Password",
    "placeholder.category_other": "Outra categoria (opcional)",
    "placeholder.new_password_optional": "Nova password (opcional)",
    "placeholder.pdf_footer": "Texto para rodapé dos PDFs",
    "placeholder.app_name": "Nome da plataforma",
    "placeholder.org_name": "Nome da clínica/hospital",
    "label.language": "Idioma",
    "label.me": "Eu",
    "label.availability": "Disponibilidade",
    "label.day": "Dia",
    "label.state": "Estado",
    "label.reason": "Motivo",
    "label.shift_settings": "Horários dos turnos",
    "label.shift_settings_hint": "Ajusta manualmente os horários de início/fim para cada código. Se a hora final for anterior (ou igual) à inicial assume-se que termina no dia seguinte.",
    "label.rules_hint": "Ajusta os limites para o mês selecionado: estes valores controlam o máximo de horas semanais, o alvo médio e o comportamento dos pedidos de folga e penalizações do solver.",
    "label.penalties": "Penalizações",
    "label.penalties_hint": "Valores mais altos tornam a violação mais cara para o solver (por ex.: “Slot vazio” deve ser o maior).",
    "label.adjustments_hint": "Introduz os feriados realizados (cada um desconta 8h ao objetivo) e ajusta horas extra ou reduções para os CONTRATADOS.",
    "label.schedule_hint": "Clique numa célula para editar; use as teclas L para bloquear/desbloquear rapidamente e Delete para limpar.",
    "label.my_availability": "As minhas disponibilidades",
    "label.my_availability_hint": "Preenche apenas o teu próprio mapa e envia para aprovação do coordenador.",
    "label.pending_availability": "Pedidos pendentes de disponibilidades",
    "label.team_members": "Membros da equipa",
    "label.new_team": "Nova equipa",
    "solver.coordinator_excluded": "Coordenador fora do solver",
    "solver.locked_cell": "Célula bloqueada/lock",
    "solver.not_allowed_service": "Serviço/turno não permitido",
    "solver.restriction": "Restrição",
    "solver.unknown_shift": "Turno desconhecido",
    "solver.not_allowed_nights": "Não autorizado para noites",
    "solver.unavailable_shift": "Indisponível para este turno",
    "solver.available_other": "Disponível para outro turno",
    "solver.partial_unavailable": "Parcial sem disponibilidade",
    "solver.request_hard": "Pedido (hard)",
    "solver.no_eligible_hard": "Sem enfermeiros elegíveis (restrições hard)",
    "solver.no_eligible_fallback": "Sem enfermeiros elegíveis (fallback)",
    "solver.global_limits": "Limitações globais",
    "solver.eligible_insufficient": "Elegíveis insuficientes",
    "solver.locked_removed": "turnos bloqueados removidos",
    "solver.no_dayoff_nd": "Sem folga após sequência N+D",
    "label.unit_settings": "Configuração da unidade",
    "label.show_app_logo": "Mostrar logo ShiftFlow",
    "label.show_org_logo": "Mostrar logo da clínica",
    "label.pdf_footer_label": "Texto do rodapé do PDF",
    "label.app_logo": "Logo ShiftFlow",
    "label.org_logo": "Logo da clínica",
    "label.upload_logos": "Carregar logos",
    "label.professional_categories": "Categorias profissionais",
    "label.add_category": "Adicionar categoria",
    "label.users": "Utilizadores",
    "label.new_user": "Novo utilizador",
    "label.create_demos": "Criar demos",
    "label.clear_demos": "Apagar demos",
    "label.services_section": "Serviços",
    "label.shifts_section": "Turnos",
    "label.service_shift_link": "Associação serviço-turno",
    "label.swap_send": "Enviar pedido",
    "label.swap_export_proof": "Exportar comprovativo",
    "label.shift_label": "Etiqueta",
    "label.service_shift": "Serviço / Turno",
    "label.lock": "Lock",
    "label.duration": "Duração",
    "label.total_hours": "Total Horas",
    "label.balance_current": "Saldo atual",
    "label.monthly_hours": "Horas Mensais",
    "label.previous_debit": "Débito anterior",
    "label.assigned_hours": "Horas atribuídas",
    "label.target_hours": "Horas alvo",
    "label.delta_month": "Delta (mês)",
    "label.bank_previous": "Banco anterior",
    "label.bank_current": "Banco atual",
    "label.mornings": "Manhãs",
    "label.afternoons": "Tardes",
    "label.nights": "Noites",
    "label.days_off": "Folgas",
    "label.rests": "Descansos",
    "label.vacations": "Férias",
    "label.worked_holidays": "Feriados trabalhados",
    "label.extra_hours": "Horas extra (+)",
    "label.reduced_hours": "Redução horas (-)",
    "label.rule_max_hours": "Máx. horas/semana (Contratado)",
    "label.rule_target_hours": "Target horas/semana",
    "label.rule_rest_hours": "Horas mínimas de descanso",
    "label.rule_hard_requests": "Pedidos de folga = regra hard",
    "label.rule_prefer_folga_nd": "Privilegiar folga após sequência N + D",
    "label.shift_settings_title": "Horários dos turnos",
    "label.holidays_title": "Feriados do mês",
    "label.manual_holidays_title": "Feriados manuais",
    "label.adjustments_title": "Feriados trabalhados / ajustes manuais",
    "label.schedule_release": "Publicar horário",
    "label.schedule_stats_title": "Horas por profissional",
    "label.unfilled_title": "Cobertura em falta",
    "label.violations_title": "Violações / Alertas",
    "label.swaps_title": "Trocas de turno",
    "label.swap_requests_title": "Pedidos",
    "label.login_title": "Entrar no ShiftFlow",
    "label.login_button": "Entrar",
    "label.login_error": "Credenciais inválidas.",
    "label.export_cancel": "Cancelar",
    "label.export_failed": "Exportação falhou",
    "label.export_title": "Exportar",
    "label.remove_holiday": "Remover este feriado",
    "label.remove": "Remover",
    "label.of": "de",
    "label.active_month": "Mês ativo",
    "label.published": "(publicado)",
    "label.invalid_time": "Indica horas válidas (HH:MM).",
    "label.invalid_shift": "Turno inválido.",
    "label.overlapping_shifts": "Turnos sobrepostos no mesmo dia.",
    "label.delete_failed": "Não foi possível remover.",
    "chat.select_thread": "Seleciona uma conversa.",
    "role.admin_group": "Administração",
    "role.coordinator_group": "Coordenação",
    "role.admin": "Admin",
    "role.coordinator": "Coordenador",
    "role.nurse": "Enfermeiro",
    "role.ao": "Assistente Operacional",
    "role.ao_short": "AO",
    "swap.current": "Atual",
    "swap.desired": "Pretendido",
    "swap.decision": "Decisão",
    "swap.observations": "Observações",
    "swap.select_recipient": "Seleciona o destinatário do pedido.",
    "placeholder.swap_recipient": "Selecionar destinatário",
    "placeholder.select_user": "Selecionar utilizador",
    "confirm.delete_category": "Apagar categoria",
    "confirm.create_demos": "Criar utilizadores e equipas demo?",
    "confirm.clear_demos": "Apagar todos os dados demo?",
    "label.manual_current": "(mês ativo)",
    "label.manual_remove": "[Remoção]",
    "label.manual_add": "[Manual]",
    "label.constraints_invalid": "Existem marcações inválidas (a vermelho). Corrige antes de guardar.",
    "label.availability_invalid": "Existem códigos inválidos. Corrige antes de enviar.",
    "label.availability_sending": "A enviar pedidos...",
    "label.availability_sent": "Pedido enviado para aprovação.",
    "label.same_shift_type": "Não pode combinar turnos do mesmo tipo no mesmo dia.",
    "label.restricted_combo": "AO e Enf. Contratados só podem fazer M+T.",
    "label.save_shift_failed": "Não foi possível guardar o turno.",
    "label.create_service_failed": "Não foi possível criar o serviço.",
    "label.schedule_generating": "A gerar...",
    "label.schedule_updated": "Horário atualizado.",
    "label.reject_reason": "Motivo da rejeição",
    "label.available_short": "Tudo disp.",
    "label.unavailable_short": "Tudo indisp.",
    "label.clear_code": "LIVRE",
    "label.recipients": "Destinatários",
    "label.recipients_users": "Utilizadores",
    "label.recipients_role": "Perfil",
    "chat.send_to_users": "Utilizadores",
    "chat.send_to_role": "Perfil",
    "chat.send_to_all": "Todos",
    "placeholder.select_role": "Selecionar perfil",
    "placeholder.select_users": "Selecionar utilizadores",
    "availability.status.pending": "Pendente",
    "availability.status.approved": "Aprovado",
    "availability.status.rejected": "Rejeitado",
    "penalty.unfilled": "Slot vazio",
    "penalty.pedido": "Pedido de folga violado",
    "penalty.hours_target": "Desvio alvo horas",
    "penalty.night_sequence": "Noites consecutivas",
    "penalty.rest_followup": "Descanso pós-noite",
    "action.move_up": "Subir",
    "action.move_down": "Descer",
    "action.add_update_holiday": "Adicionar/alterar",
    "action.remove_national_holiday": "Remover feriado nacional",
    "chat.none_threads": "Sem conversas.",
    "chat.none_users": "Sem utilizadores.",
    "chat.none_messages": "Sem mensagens.",
    "swaps.none": "Sem pedidos ativos.",
    "teams.none": "Sem equipas",
    "services.none_service": "Sem serviço",
    "holidays.none": "Sem feriados manuais.",
    "availability.pending_none": "Sem pedidos pendentes.",
    "availability.submitted": "Pedido enviado para aprovação.",
    "schedule.updated": "Horário atualizado.",
    "status.active": "Ativo",
    "status.inactive": "Inativo",
    "swap.status.pending_participants": "A aguardar participantes",
    "swap.status.pending_coordinator": "A aguardar coordenador",
    "swap.status.approved": "Aprovado",
    "swap.status.rejected": "Rejeitado",
    "swap.status.rejected_participant": "Recusado por participante",
    "swap.participant.pending": "A aguardar",
    "swap.participant.accepted": "Aceite",
    "swap.participant.rejected": "Recusado",
    "swap.requested_by": "Pedido por",
    "confirm.delete_swap": "Eliminar este pedido de troca?",
    "confirm.delete_user": "Eliminar utilizador",
    "confirm.delete_team": "Eliminar equipa",
    "confirm.delete_service": "Eliminar serviço",
    "confirm.delete_shift": "Eliminar turno",
    "confirm.delete_professional": "Remover profissional?",
    "confirm.clear_schedule": "Apagar horário de",
    "weekdays": ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"],
    "months": [
      "Janeiro",
      "Fevereiro",
      "Março",
      "Abril",
      "Maio",
      "Junho",
      "Julho",
      "Agosto",
      "Setembro",
      "Outubro",
      "Novembro",
      "Dezembro",
    ],
  },
  en: {
    "lang.pt": "Portuguese",
    "lang.en": "English",
    "app.subtitle": "Shift planning and scheduling",
    "action.logout": "Logout",
    "label.month": "Month",
    "label.year": "Year",
    "label.team": "Team",
    "group.enf": "Nursing",
    "group.ao": "Operations Assistants",
    "nav.dashboard": "Dashboard",
    "nav.nurses": "Staff",
    "nav.requirements": "Needs",
    "nav.constraints": "Availability",
    "nav.rules": "Rules",
    "nav.teams": "Teams",
    "nav.services": "Services/Shifts",
    "nav.schedule": "Schedule",
    "nav.swaps": "Swaps",
    "nav.chat": "Chat",
    "nav.admin": "Admin",
    "dashboard.generate": "Generate schedule",
    "dashboard.export_schedule": "Export schedule",
    "dashboard.export_constraints": "Export availability",
    "dashboard.needs": "Needs",
    "dashboard.assigned": "Assigned shifts",
    "dashboard.locks": "Active locks",
    "dashboard.alerts": "Alerts",
    "section.dashboard": "Dashboard",
    "section.nurses": "Staff",
    "section.requirements": "Monthly needs",
    "section.constraints": "Availability / Requests",
    "section.rules": "Monthly rules",
    "section.schedule": "Monthly schedule",
    "section.teams": "Service teams",
    "section.services": "Services and shifts",
    "section.swaps": "Shift swaps",
    "section.chat": "Chat",
    "section.admin": "Administration",
    "btn.add": "Add",
    "btn.add_professional": "Add professional",
    "btn.edit": "Edit",
    "btn.save": "Save",
    "btn.update": "Update",
    "btn.close": "Close",
    "btn.clear": "Clear",
    "btn.apply": "Apply",
    "btn.associate": "Associate",
    "btn.cancel": "Cancel",
    "btn.delete": "Delete",
    "btn.activate": "Activate",
    "btn.deactivate": "Deactivate",
    "btn.archive": "Archive",
    "btn.publish": "Publish",
    "btn.generate": "Generate schedule",
    "btn.export": "Export",
    "btn.send": "Send",
    "btn.approve": "Approve",
    "btn.reject": "Reject",
    "btn.accept": "Accept",
    "btn.decline": "Decline",
    "btn.create_team": "Create team",
    "btn.add_member": "Save members",
    "btn.fill_all": "Fill all with 1",
    "btn.clear_all": "Clear all",
    "btn.save_requirements": "Save needs",
    "btn.save_constraints": "Save marks",
    "btn.available_all": "Available all days",
    "btn.unavailable_all": "Unavailable all days",
    "btn.submit_availability": "Submit for approval",
    "btn.save_rules": "Save rules",
    "btn.add_holiday": "Add",
    "btn.save_adjustments": "Save adjustments",
    "btn.clear_schedule": "Delete selected schedule",
    "label.professional": "Professional",
    "label.edit_professional": "Edit",
    "label.new_professional": "New professional",
    "label.user": "User",
    "label.services": "Services",
    "label.weekly_hours": "Weekly hours",
    "label.balance": "Balance (h)",
    "label.actions": "Actions",
    "label.order": "Order",
    "label.yes": "Yes",
    "label.no": "No",
    "label.category": "Category",
    "label.user_active": "Active user",
    "label.category_active": "Active",
    "label.action": "Action",
    "label.participants": "Participants",
    "label.can_night": "Can work night?",
    "label.max_nights": "Max nights/month",
    "label.services_allowed": "Allowed services",
    "label.service": "Service",
    "label.role": "Role",
    "label.status": "Status",
    "label.code": "Code",
    "label.name": "Name",
    "label.color": "Color",
    "label.shift": "Shift",
    "label.shift2": "Shift 2 (optional)",
    "label.shift3": "Shift 3 (optional)",
    "label.type": "Type",
    "label.start": "Start",
    "label.end": "End",
    "label.date": "Day",
    "label.description": "Description",
    "label.manual_holidays": "Manual holidays",
    "label.holidays": "Month holidays",
    "label.adjustments": "Worked holidays / manual adjustments",
    "label.schedule_stats": "Hours per professional",
    "label.unfilled": "Unfilled coverage",
    "label.violations": "Violations / Alerts",
    "label.publish_schedule": "Publish schedule",
    "label.schedule_tools": "Schedule tools",
    "label.export_swaps": "Export swaps",
    "label.swap_request": "Request swap",
    "label.swap_requests": "Requests",
    "label.chat_users": "Users",
    "label.chat_threads": "Threads",
    "placeholder.search_user": "Search user...",
    "placeholder.role": "Role",
    "placeholder.chat_message": "Type a message...",
    "placeholder.name": "Name",
    "placeholder.username": "Username",
    "placeholder.team_name": "Team name",
    "placeholder.service_code": "Service code",
    "placeholder.shift_code": "Code",
    "placeholder.shift_label": "Label",
    "placeholder.service_name": "Name",
    "placeholder.category_name": "Category name",
    "placeholder.order": "Order (optional)",
    "placeholder.reason_optional": "Reason (optional)",
    "placeholder.observations_optional": "Observations (optional)",
    "placeholder.swap_service": "Current service (optional)",
    "placeholder.swap_shift": "Current shift (optional)",
    "placeholder.swap_desired_service": "Desired service (optional)",
    "placeholder.swap_desired_shift": "Desired shift (optional)",
    "placeholder.full_name": "Full name",
    "placeholder.password": "Password",
    "placeholder.category_other": "Other category (optional)",
    "placeholder.new_password_optional": "New password (optional)",
    "placeholder.pdf_footer": "PDF footer text",
    "placeholder.app_name": "Platform name",
    "placeholder.org_name": "Clinic/hospital name",
    "label.language": "Language",
    "label.me": "Me",
    "label.availability": "Availability",
    "label.day": "Day",
    "label.state": "Status",
    "label.reason": "Reason",
    "label.shift_settings": "Shift times",
    "label.shift_settings_hint": "Adjust start/end times for each code. If the end time is before (or equal to) the start time, it ends the next day.",
    "label.rules_hint": "Adjust limits for the selected month: these values control max weekly hours, the average target, and how leave requests/penalties are handled by the solver.",
    "label.penalties": "Penalties",
    "label.penalties_hint": "Higher values make violations more expensive for the solver (e.g., “Empty slot” should be the highest).",
    "label.adjustments_hint": "Enter worked holidays (each subtracts 8h from the target) and adjust extra or reduced hours for CONTRACT staff.",
    "label.schedule_hint": "Click a cell to edit; use L to lock/unlock quickly and Delete to clear.",
    "label.my_availability": "My availability",
    "label.my_availability_hint": "Fill only your own map and submit for coordinator approval.",
    "label.pending_availability": "Pending availability requests",
    "label.team_members": "Team members",
    "label.new_team": "New team",
    "solver.coordinator_excluded": "Coordinator excluded from solver",
    "solver.locked_cell": "Locked cell",
    "solver.not_allowed_service": "Service/shift not allowed",
    "solver.restriction": "Restriction",
    "solver.unknown_shift": "Unknown shift",
    "solver.not_allowed_nights": "Not authorized for nights",
    "solver.unavailable_shift": "Unavailable for this shift",
    "solver.available_other": "Available for another shift",
    "solver.partial_unavailable": "Partial without availability",
    "solver.request_hard": "Request (hard)",
    "solver.no_eligible_hard": "No eligible nurses (hard constraints)",
    "solver.no_eligible_fallback": "No eligible nurses (fallback)",
    "solver.global_limits": "Global limitations",
    "solver.eligible_insufficient": "Insufficient eligible",
    "solver.locked_removed": "locked shifts removed",
    "solver.no_dayoff_nd": "No day off after N+D sequence",
    "label.unit_settings": "Facility settings",
    "label.show_app_logo": "Show ShiftFlow logo",
    "label.show_org_logo": "Show clinic logo",
    "label.pdf_footer_label": "PDF footer text",
    "label.app_logo": "ShiftFlow logo",
    "label.org_logo": "Clinic logo",
    "label.upload_logos": "Upload logos",
    "label.professional_categories": "Professional categories",
    "label.add_category": "Add category",
    "label.users": "Users",
    "label.new_user": "New user",
    "label.create_demos": "Create demos",
    "label.clear_demos": "Delete demos",
    "label.services_section": "Services",
    "label.shifts_section": "Shifts",
    "label.service_shift_link": "Service-shift link",
    "label.swap_send": "Send request",
    "label.swap_export_proof": "Export proof",
    "label.shift_label": "Label",
    "label.service_shift": "Service / Shift",
    "label.lock": "Lock",
    "label.duration": "Duration",
    "label.total_hours": "Total Hours",
    "label.balance_current": "Current balance",
    "label.monthly_hours": "Monthly Hours",
    "label.previous_debit": "Previous balance",
    "label.assigned_hours": "Assigned hours",
    "label.target_hours": "Target hours",
    "label.delta_month": "Delta (month)",
    "label.bank_previous": "Previous bank",
    "label.bank_current": "Current bank",
    "label.mornings": "Mornings",
    "label.afternoons": "Afternoons",
    "label.nights": "Nights",
    "label.days_off": "Days off",
    "label.rests": "Rests",
    "label.vacations": "Vacations",
    "label.worked_holidays": "Worked holidays",
    "label.extra_hours": "Extra hours (+)",
    "label.reduced_hours": "Reduced hours (-)",
    "label.rule_max_hours": "Max hours/week (Contract)",
    "label.rule_target_hours": "Target hours/week",
    "label.rule_rest_hours": "Minimum rest hours",
    "label.rule_hard_requests": "Leave requests = hard rule",
    "label.rule_prefer_folga_nd": "Prefer rest after N + D sequence",
    "label.shift_settings_title": "Shift times",
    "label.holidays_title": "Month holidays",
    "label.manual_holidays_title": "Manual holidays",
    "label.adjustments_title": "Worked holidays / manual adjustments",
    "label.schedule_release": "Publish schedule",
    "label.schedule_stats_title": "Hours per professional",
    "label.unfilled_title": "Unfilled coverage",
    "label.violations_title": "Violations / Alerts",
    "label.swaps_title": "Shift swaps",
    "label.swap_requests_title": "Requests",
    "label.login_title": "Sign in to ShiftFlow",
    "label.login_button": "Sign in",
    "label.login_error": "Invalid credentials.",
    "label.export_cancel": "Cancel",
    "label.export_failed": "Export failed",
    "label.export_title": "Export",
    "label.remove_holiday": "Remove this holiday",
    "label.remove": "Remove",
    "label.of": "of",
    "label.active_month": "Active month",
    "label.published": "(published)",
    "label.invalid_time": "Provide valid hours (HH:MM).",
    "label.invalid_shift": "Invalid shift.",
    "label.overlapping_shifts": "Overlapping shifts on the same day.",
    "label.delete_failed": "Could not remove.",
    "chat.select_thread": "Select a conversation.",
    "role.admin_group": "Administration",
    "role.coordinator_group": "Coordination",
    "role.admin": "Admin",
    "role.coordinator": "Coordinator",
    "role.nurse": "Nurse",
    "role.ao": "Operations Assistant",
    "role.ao_short": "OA",
    "swap.current": "Current",
    "swap.desired": "Desired",
    "swap.decision": "Decision",
    "swap.observations": "Observations",
    "swap.select_recipient": "Select the recipient for this request.",
    "placeholder.swap_recipient": "Select recipient",
    "placeholder.select_user": "Select user",
    "confirm.delete_category": "Delete category",
    "confirm.create_demos": "Create demo users and teams?",
    "confirm.clear_demos": "Delete all demo data?",
    "label.manual_current": "(active month)",
    "label.manual_remove": "[Removal]",
    "label.manual_add": "[Manual]",
    "label.constraints_invalid": "There are invalid marks (in red). Fix them before saving.",
    "label.availability_invalid": "There are invalid codes. Fix them before submitting.",
    "label.availability_sending": "Submitting requests...",
    "label.availability_sent": "Request sent for approval.",
    "label.same_shift_type": "You cannot combine shifts of the same type on the same day.",
    "label.restricted_combo": "Assistants and contracted nurses can only do M+T.",
    "label.save_shift_failed": "Could not save the shift.",
    "label.create_service_failed": "Could not create the service.",
    "label.schedule_generating": "Generating...",
    "label.schedule_updated": "Schedule updated.",
    "label.reject_reason": "Rejection reason",
    "label.available_short": "All avail.",
    "label.unavailable_short": "All unavail.",
    "label.clear_code": "CLEAR",
    "label.recipients": "Recipients",
    "label.recipients_users": "Users",
    "label.recipients_role": "Role",
    "chat.send_to_users": "Users",
    "chat.send_to_role": "Role",
    "chat.send_to_all": "Everyone",
    "placeholder.select_role": "Select role",
    "placeholder.select_users": "Select users",
    "availability.status.pending": "Pending",
    "availability.status.approved": "Approved",
    "availability.status.rejected": "Rejected",
    "penalty.unfilled": "Empty slot",
    "penalty.pedido": "Leave request violated",
    "penalty.hours_target": "Target hours deviation",
    "penalty.night_sequence": "Consecutive nights",
    "penalty.rest_followup": "Post-night rest",
    "action.move_up": "Move up",
    "action.move_down": "Move down",
    "action.add_update_holiday": "Add/update",
    "action.remove_national_holiday": "Remove national holiday",
    "chat.none_threads": "No conversations.",
    "chat.none_users": "No users.",
    "chat.none_messages": "No messages.",
    "swaps.none": "No active requests.",
    "teams.none": "No teams",
    "services.none_service": "No service",
    "holidays.none": "No manual holidays.",
    "availability.pending_none": "No pending requests.",
    "availability.submitted": "Request sent for approval.",
    "schedule.updated": "Schedule updated.",
    "status.active": "Active",
    "status.inactive": "Inactive",
    "swap.status.pending_participants": "Waiting for participants",
    "swap.status.pending_coordinator": "Waiting for coordinator",
    "swap.status.approved": "Approved",
    "swap.status.rejected": "Rejected",
    "swap.status.rejected_participant": "Rejected by participant",
    "swap.participant.pending": "Pending",
    "swap.participant.accepted": "Accepted",
    "swap.participant.rejected": "Rejected",
    "swap.requested_by": "Requested by",
    "confirm.delete_swap": "Delete this swap request?",
    "confirm.delete_user": "Delete user",
    "confirm.delete_team": "Delete team",
    "confirm.delete_service": "Delete service",
    "confirm.delete_shift": "Delete shift",
    "confirm.delete_professional": "Remove professional?",
    "confirm.clear_schedule": "Delete schedule for",
    "weekdays": ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
    "months": [
      "January",
      "February",
      "March",
      "April",
      "May",
      "June",
      "July",
      "August",
      "September",
      "October",
      "November",
      "December",
    ],
  },
};

let monthNames = I18N.pt.months;
let weekdayLabels = I18N.pt.weekdays;

function t(key, fallback) {
  return I18N[state.lang]?.[key] ?? fallback ?? key;
}
const constraintComboOrder = [
  "M",
  "T",
  "L",
  "N",
  "MT",
  "ML",
  "MN",
  "TL",
  "TN",
  "LN",
  "MTL",
  "MTN",
  "MLN",
  "TLN",
  "MTLN",
];
const categoryLabels = {
  COORDENADOR: "Enfermeiro Coordenador",
  CONTRATADO: "Enfermeiro Contratado",
  CONTRATADO_TEMPO_PARCIAL: "Contratado Tempo Parcial (18h)",
  RV_TEMPO_INTEIRO: "RV Tempo Inteiro",
  RV_TEMPO_PARCIAL: "RV Tempo Parcial",
  ASSISTENTE_OPERACIONAL: "Assistente Operacional",
};
const categoryPriority = {
  COORDENADOR: 0,
  CONTRATADO: 1,
  CONTRATADO_TEMPO_PARCIAL: 2,
  RV_TEMPO_INTEIRO: 3,
  RV_TEMPO_PARCIAL: 4,
  ASSISTENTE_OPERACIONAL: 5,
};

let editingNurseId = null;
let cellEditorContext = null;
let nurseFormAnchor = null;
let editingUserId = null;
let editingTeamId = null;
let editingCategoryId = null;

function isAdmin() {
  return state.user?.role === "ADMIN";
}

function isCoordinator() {
  return state.user?.role === "COORDENADOR";
}

function canEditSchedule() {
  return isAdmin() || isCoordinator();
}

function currentGroupRole() {
  return state.group;
}

function groupQuery() {
  return `group=${encodeURIComponent(state.group || "")}`;
}

function groupLabel() {
  if (!state.group) return "";
  if (state.group === "ASSISTENTE_OPERACIONAL") {
    return t("group.ao", "Assistentes Operacionais");
  }
  if (state.group === "ENFERMEIRO") {
    return t("group.enf", "Enfermagem");
  }
  return state.group;
}

function formatRole(role) {
  const roleMap = {
    ADMIN: t("role.admin", "Admin"),
    COORDENADOR: t("role.coordinator", "Coordenador"),
    ENFERMEIRO: t("role.nurse", "Enfermeiro"),
    ASSISTENTE_OPERACIONAL: t("role.ao", "Assistente Operacional"),
  };
  return roleMap[role] || role || "";
}

function availableRoles() {
  return (state.meta?.roles && state.meta.roles.length)
    ? state.meta.roles
    : ["ENFERMEIRO", "ASSISTENTE_OPERACIONAL"];
}

function populateRoleSelect(select, roles, options = {}) {
  if (!select) return;
  const includeAdmin = options.includeAdmin || false;
  const includeCoordinator = options.includeCoordinator || false;
  const keepValue = options.keepValue || false;
  const previous = keepValue ? select.value : "";
  select.innerHTML = "";
  if (includeAdmin) {
    const adminOpt = document.createElement("option");
    adminOpt.value = "ADMIN";
    adminOpt.textContent = formatRole("ADMIN");
    select.appendChild(adminOpt);
  }
  if (includeCoordinator) {
    const coordOpt = document.createElement("option");
    coordOpt.value = "COORDENADOR";
    coordOpt.textContent = formatRole("COORDENADOR");
    select.appendChild(coordOpt);
  }
  roles.forEach((role) => {
    const option = document.createElement("option");
    option.value = role;
    option.textContent = formatRole(role);
    select.appendChild(option);
  });
  if (keepValue && previous) {
    select.value = previous;
  }
  if (!select.value && select.options.length) {
    select.value = select.options[0].value;
  }
}

function populateRoleOptionsList(roles) {
  const datalist = document.getElementById("roleOptionsList");
  if (!datalist) return;
  datalist.innerHTML = "";
  roles.forEach((role) => {
    const option = document.createElement("option");
    option.value = role;
    datalist.appendChild(option);
  });
}

function populateRoleSelects() {
  const roles = availableRoles();
  populateRoleSelect(document.getElementById("groupSelect"), roles, { keepValue: true });
  populateRoleSelect(document.getElementById("teamRole"), roles, { keepValue: true });
  populateRoleSelect(document.getElementById("serviceRole"), roles, { keepValue: true });
  populateRoleSelect(document.getElementById("teamEditRole"), roles, { keepValue: true });
  populateRoleSelect(document.getElementById("userRole"), roles, {
    includeAdmin: true,
    includeCoordinator: true,
    keepValue: true,
  });
  populateRoleOptionsList(roles);
}

function syncGroupSelects() {
  const teamRole = document.getElementById("teamRole");
  const serviceRole = document.getElementById("serviceRole");
  const role = currentGroupRole();
  if (teamRole) {
    teamRole.value = role;
  }
  if (serviceRole) {
    serviceRole.value = role;
  }
}

function minutesToTime(totalMinutes) {
  if (totalMinutes == null) return "00:00";
  const minutesPerDay = 24 * 60;
  const normalized =
    ((Number(totalMinutes) % minutesPerDay) + minutesPerDay) % minutesPerDay;
  const hours = Math.floor(normalized / 60)
    .toString()
    .padStart(2, "0");
  const mins = (normalized % 60).toString().padStart(2, "0");
  return `${hours}:${mins}`;
}

function formatDuration(minutes) {
  if (!minutes) return "0h";
  return `${(minutes / 60).toFixed(1)}h`;
}

function weekdayLabel(day) {
  const jsDate = new Date(state.year, state.month - 1, day);
  return weekdayLabels[jsDate.getDay()];
}

function isWeekend(day) {
  const jsDate = new Date(state.year, state.month - 1, day);
  const weekday = jsDate.getDay();
  return weekday === 0 || weekday === 6;
}

function createDayHeader(day, isHoliday) {
  const wrapper = document.createElement("div");
  wrapper.className = "day-header";
  if (isHoliday) wrapper.classList.add("holiday");
  if (isWeekend(day)) wrapper.classList.add("weekend");
  const dayEl = document.createElement("span");
  dayEl.textContent = day;
  const weekdayEl = document.createElement("small");
  weekdayEl.textContent = weekdayLabel(day);
  wrapper.appendChild(dayEl);
  wrapper.appendChild(weekdayEl);
  return wrapper;
}

function buildConstraintOptions() {
  if (!state.meta) return [];
  const entries = Object.entries(state.meta.constraint_codes || {});
  const rank = (code) => {
    if (code === "") return 0;
    if (code === "FERIAS") return 1;
    if (code === "DISPENSA") return 2;
    if (code === "FERIADO") return 3;
    if (code === "FERIADO_TRAB") return 4;
    if (code === "PEDIDO_FOLGA") return 5;
    if (code === "INDISPONIVEL") return 6;
    if (code === "DISPONIVEL") return 7;
    const suffix = code.split("_")[1] || "";
    const idx = constraintComboOrder.indexOf(suffix);
    if (code.startsWith("DISPONIVEL_")) {
      return 10 + (idx >= 0 ? idx : 50);
    }
    if (code.startsWith("INDISPONIVEL_")) {
      return 20 + (idx >= 0 ? idx : 50);
    }
    return 30;
  };
  return entries
    .sort((a, b) => rank(a[0]) - rank(b[0]))
    .map(([code, label]) => ({ code, label }));
}

function getSortedNurses() {
  return [...state.nurses].sort((a, b) => {
    const orderMap = state.meta?.category_order || {};
    const ca = orderMap[a.category] ?? categoryPriority[a.category] ?? 99;
    const cb = orderMap[b.category] ?? categoryPriority[b.category] ?? 99;
    if (ca !== cb) return ca - cb;
    const orderA = a.display_order ?? 0;
    const orderB = b.display_order ?? 0;
    if (orderA !== orderB) return orderA - orderB;
    return a.name.localeCompare(b.name);
  });
}

function ensureShiftLookup() {
  if (!state.meta || state.meta.shiftLookup) return;
  const lookup = {};
  state.meta.service_shifts.forEach((shift) => {
    lookup[shift.code] = shift;
  });
  state.meta.shiftLookup = lookup;
}

function getShiftMeta(code) {
  ensureShiftLookup();
  return state.meta?.shiftLookup?.[code] || null;
}

function minutesToHoursText(minutes) {
  if (!minutes) return "0";
  return (minutes / 60).toFixed(2);
}

function minutesToHoursValue(minutes) {
  if (!minutes) return "0";
  return (minutes / 60).toFixed(2);
}

function translateSolverReason(reason) {
  if (!reason) return reason;
  const trimmed = reason.trim();
  const directMap = {
    "Coordenador fora do solver": t("solver.coordinator_excluded", trimmed),
    "Célula bloqueada/lock": t("solver.locked_cell", trimmed),
    "Serviço/turno não permitido": t("solver.not_allowed_service", trimmed),
    "Turno desconhecido": t("solver.unknown_shift", trimmed),
    "Não autorizado para noites": t("solver.not_allowed_nights", trimmed),
    "Indisponível para este turno": t("solver.unavailable_shift", trimmed),
    "Disponível para outro turno": t("solver.available_other", trimmed),
    "Parcial sem disponibilidade": t("solver.partial_unavailable", trimmed),
    "Pedido (hard)": t("solver.request_hard", trimmed),
    "Sem enfermeiros elegíveis (restrições hard)": t("solver.no_eligible_hard", trimmed),
    "Sem enfermeiros elegíveis (fallback)": t("solver.no_eligible_fallback", trimmed),
    "Limitações globais": t("solver.global_limits", trimmed),
  };
  if (directMap[trimmed]) return directMap[trimmed];
  if (trimmed.startsWith("Restrição ")) {
    const suffix = trimmed.slice("Restrição ".length);
    return `${t("solver.restriction", "Restriction")} ${suffix}`.trim();
  }
  if (trimmed.startsWith("Elegíveis insuficientes")) {
    const suffix = trimmed.slice("Elegíveis insuficientes".length);
    return `${t("solver.eligible_insufficient", "Insufficient eligible")}${suffix}`;
  }
  return trimmed;
}

function translateSolverViolation(text) {
  if (!text) return text;
  const trimmed = text.trim();
  if (trimmed.startsWith("Sem folga após sequência N+D")) {
    const match = trimmed.match(/Sem folga após sequência N\\+D \\(dia (\\d+)\\):\\s*(.+)$/);
    if (match) {
      return `${t("solver.no_dayoff_nd", "No day off after N+D sequence")} (${t("label.day", "Day")} ${match[1]}): ${match[2]}`;
    }
    return t("solver.no_dayoff_nd", trimmed);
  }
  if (trimmed.startsWith("Dia ")) {
    const rest = trimmed.slice(4);
    const firstSpace = rest.indexOf(" ");
    if (firstSpace !== -1) {
      const day = rest.slice(0, firstSpace);
      const remaining = rest.slice(firstSpace + 1);
      const colonIndex = remaining.lastIndexOf(":");
      if (colonIndex !== -1) {
        const left = remaining.slice(0, colonIndex).trim();
        const reason = remaining.slice(colonIndex + 1).trim();
        return `${t("label.day", "Day")} ${day} ${left}: ${translateSolverReason(reason)}`;
      }
      return `${t("label.day", "Day")} ${day} ${remaining}`;
    }
  }
  return translateSolverReason(trimmed);
}

function hoursToMinutes(value) {
  const number = Number(value);
  if (Number.isNaN(number)) {
    return 0;
  }
  return Math.round(number * 60);
}

function applyBranding(settings) {
  if (!settings) return;
  state.settings = settings;
  const titleEl = document.getElementById("brandTitle");
  const subtitleEl = document.getElementById("brandSubtitle");
  const appLogoEl = document.getElementById("brandAppLogo");
  const orgLogoEl = document.getElementById("brandOrgLogo");

  if (titleEl && settings.app_name) {
    titleEl.textContent = settings.app_name;
    document.title = settings.app_name;
  }
  if (subtitleEl) {
    subtitleEl.textContent = settings.org_name || t("app.subtitle", "Gestao de turnos e horarios");
  }
  if (appLogoEl) {
    if (settings.app_logo_url && settings.show_app_logo !== false) {
      appLogoEl.src = settings.app_logo_url;
      appLogoEl.style.display = "block";
      if (titleEl) titleEl.style.display = "none";
    } else {
      appLogoEl.style.display = "none";
      if (titleEl) titleEl.style.display = "";
    }
  }
  if (orgLogoEl) {
    if (settings.org_logo_url && settings.show_org_logo !== false) {
      orgLogoEl.src = settings.org_logo_url;
      orgLogoEl.style.display = "block";
    } else {
      orgLogoEl.style.display = "none";
    }
  }

  const root = document.documentElement;
  if (settings.primary_color) {
    root.style.setProperty("--flow-primary", settings.primary_color);
  }
  if (settings.accent_color) {
    root.style.setProperty("--flow-accent", settings.accent_color);
  }
  if (settings.background) {
    root.style.setProperty("--flow-bg", settings.background);
  }
}

function populateSettingsForm() {
  if (!isAdmin() || !state.settings) return;
  document.getElementById("settingsAppName").value =
    state.settings.app_name || "";
  document.getElementById("settingsOrgName").value =
    state.settings.org_name || "";
  document.getElementById("settingsShowAppLogo").checked =
    state.settings.show_app_logo !== false;
  document.getElementById("settingsShowOrgLogo").checked =
    state.settings.show_org_logo !== false;
  document.getElementById("settingsPrimaryColor").value =
    state.settings.primary_color || "#1b3a57";
  document.getElementById("settingsAccentColor").value =
    state.settings.accent_color || "#4b89dc";
  document.getElementById("settingsBackground").value =
    state.settings.background || "#f5f9ff";
  document.getElementById("settingsPdfInfo").value =
    state.settings.pdf_info_text || "";
}

function setSession(token, user) {
  state.token = token;
  state.user = user;
  if (token) {
    localStorage.setItem("shiftflow_token", token);
  }
  if (user) {
    localStorage.setItem("shiftflow_user", JSON.stringify(user));
  }
  applyGroupPermissions();
  updateUserBadge();
  applyRoleAccess();
}

function clearSession() {
  state.token = null;
  state.user = null;
  state.users = [];
  state.adminUsers = [];
  state.teams = [];
  state.services = [];
  state.shifts = [];
  state.chatThreads = [];
  state.chatMessages = [];
  state.swaps = [];
  state.activeChatPeerId = null;
  localStorage.removeItem("shiftflow_token");
  localStorage.removeItem("shiftflow_user");
  updateUserBadge();
  applyRoleAccess();
}

function updateUserBadge() {
  const badge = document.getElementById("userBadge");
  const logoutBtn = document.getElementById("logoutBtn");
  if (!badge) return;
  if (!state.user) {
    badge.textContent = "";
    if (logoutBtn) logoutBtn.style.display = "none";
    return;
  }
  badge.textContent = `${state.user.full_name} (${formatRole(state.user.role)})`;
  if (logoutBtn) logoutBtn.style.display = "inline-flex";
}

function setBadge(id, count) {
  const badge = document.getElementById(id);
  if (!badge) return;
  if (!count) {
    badge.textContent = "";
    badge.classList.add("hidden");
    return;
  }
  badge.textContent = count > 99 ? "99+" : String(count);
  badge.classList.remove("hidden");
}

function applyRoleAccess() {
  const role = state.user?.role || "";
  document.body.classList.toggle("readonly", !canEditSchedule());
  document.body.classList.toggle("admin", isAdmin());
  applyGroupPermissions();
  document.querySelectorAll("[data-roles]").forEach((el) => {
    const roles = (el.dataset.roles || "").split(",").map((item) => item.trim());
    if (!roles.length || roles.includes("ALL") || roles.includes(role)) {
      el.style.display = "";
    } else {
      el.style.display = "none";
    }
  });
  ensureVisibleSection();
}

function ensureVisibleSection() {
  const active = document.querySelector("nav button.active");
  if (active && active.style.display !== "none") return;
  const firstVisible = Array.from(document.querySelectorAll("nav button")).find(
    (button) => button.style.display !== "none"
  );
  if (!firstVisible) return;
  firstVisible.click();
}

function applyGroupPermissions() {
  const isEditor = state.user && ["ADMIN", "COORDENADOR"].includes(state.user.role);
  if (state.user && !isEditor) {
    state.group = state.user.role;
  }
  const groupSelect = document.getElementById("groupSelect");
  if (!groupSelect) {
    updateCurrentPeriodLabel();
    return;
  }
  if (!state.user) {
    groupSelect.disabled = false;
    return;
  }
  if (!isEditor) {
    groupSelect.value = state.group;
    groupSelect.disabled = true;
  } else {
    groupSelect.disabled = false;
  }
  syncGroupSelects();
  updateCurrentPeriodLabel();
}

async function restoreSession() {
  const token = localStorage.getItem("shiftflow_token");
  if (!token) return false;
  state.token = token;
  try {
    const response = await apiFetch("/api/auth/me");
    if (!response.ok) throw new Error("Sessao expirada");
    const user = await response.json();
    setSession(token, user);
    return true;
  } catch (error) {
    clearSession();
    return false;
  }
}

function setupAuthControls() {
  const logoutBtn = document.getElementById("logoutBtn");
  if (logoutBtn) {
    logoutBtn.addEventListener("click", () => {
      clearSession();
      window.location.href = "/login";
    });
  }
}

async function safeCall(task) {
  try {
    await task();
  } catch (error) {
    console.warn("ShiftFlow: falha ao carregar dados.", error);
  }
}

async function bootstrapApp() {
  if (!state.user) return;
  await safeCall(loadSettings);
  await safeCall(loadMeta);
  await safeCall(loadNurses);
  await safeCall(refreshMonthData);
  await safeCall(loadUsers);
  await safeCall(loadTeams);
  await safeCall(loadServices);
  await safeCall(loadReleases);
  await safeCall(loadChatThreads);
  await safeCall(loadSwaps);
  await safeCall(loadAdminUsers);
  await safeCall(loadCategories);
}

async function loadSettings() {
  try {
    const response = await apiFetch("/api/settings");
    if (!response.ok) return;
    const data = await response.json();
    applyBranding(data);
    populateSettingsForm();
  } catch (e) {
    console.warn("Nao foi possivel carregar configuracoes.", e);
  }
}
function normalizeLetters(raw) {
  if (!raw) return "";
  const allowed = ["M", "T", "L", "N"];
  const letters = new Set();
  raw.split("").forEach((letter) => {
    if (allowed.includes(letter)) {
      letters.add(letter);
    }
  });
  return allowed.filter((letter) => letters.has(letter)).join("");
}

function parseConstraintText(value) {
  if (value == null) return "";
  const normalized = value
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/\s+/g, "")
    .toUpperCase();
  if (!normalized) return "";
  const mapping = {
    FERIAS: "FERIAS",
    FER: "FERIADO",
    FERIADO: "FERIADO",
    DS: "DISPENSA",
    DESCANSO: "DISPENSA",
    V: "DISPONIVEL",
    DISP: "DISPONIVEL",
    I: "INDISPONIVEL",
    INDISP: "INDISPONIVEL",
    P: "PEDIDO_FOLGA",
    F: "PEDIDO_FOLGA",
    D: "PEDIDO_DESCANSO",
    DF: "PEDIDO_DESCANSO_FOLGA",
    "D/F": "PEDIDO_DESCANSO_FOLGA",
  };
  if (mapping[normalized]) {
    return mapping[normalized];
  }
  const combo = normalized.match(/^(I)?([A-Z]+)$/);
  if (combo) {
    const lettersRaw = combo[2].replace(/S/g, "");
    if (!lettersRaw || /[^MTLN]/.test(lettersRaw)) {
      return "";
    }
    const letters = normalizeLetters(lettersRaw);
    if (!letters) return "";
    const prefix = combo[1] ? "INDISPONIVEL" : "DISPONIVEL";
    return `${prefix}_${letters}`;
  }
  return "";
}

function constraintCodeToInput(code) {
  if (!code) return "";
  const map = {
    FERIAS: "FERIAS",
    DISPENSA: "DS",
    FERIADO: "FER",
    PEDIDO_FOLGA: "F",
    PEDIDO_DESCANSO: "D",
    PEDIDO_DESCANSO_FOLGA: "D/F",
    INDISPONIVEL: "I",
    DISPONIVEL: "V",
  };
  if (map[code]) return map[code];
  if (code.startsWith("DISPONIVEL_")) {
    return code.split("_")[1];
  }
  if (code.startsWith("INDISPONIVEL_")) {
    return `I${code.split("_")[1]}`;
  }
  return code.slice(0, 4);
}

function normalizeConstraintInputEl(input) {
  const parsed = parseConstraintText(input.value);
  if (!parsed) {
    if (input.value.trim()) {
      input.classList.add("invalid");
    } else {
      input.classList.remove("invalid");
    }
    input.dataset.code = "";
    return "";
  }
  input.value = constraintCodeToInput(parsed);
  input.dataset.code = parsed;
  input.classList.remove("invalid");
  return parsed;
}

function setupConstraintDatalist() {
  const datalist = document.getElementById("constraintCodesList");
  if (!datalist) return;
  const baseEntries = [
    "FERIAS",
    "FER",
    "DS",
    "F",
    "D",
    "D/F",
    "V",
    "I",
  ];
  const combos = constraintComboOrder.flatMap((combo) => [combo, `I${combo}`]);
  const aliasCombos = ["LS", "TLS"];
  aliasCombos.forEach((alias) => {
    combos.push(alias, `I${alias}`);
  });
  datalist.innerHTML = "";
  const seen = new Set();
  [...baseEntries, ...combos].forEach((entry) => {
    if (seen.has(entry)) return;
    seen.add(entry);
    const option = document.createElement("option");
    option.value = entry;
    datalist.appendChild(option);
  });
}

function updateManualHolidayLabelState() {
  const select = document.getElementById("manualHolidayAction");
  const labelInput = document.getElementById("manualHolidayLabel");
  if (!select || !labelInput) return;
  const isRemove = select.value === "REMOVE";
  labelInput.required = !isRemove;
  labelInput.disabled = isRemove;
  labelInput.placeholder = isRemove
    ? t("placeholder.reason_optional", "Motivo (opcional)")
    : t("label.description", "Descrição");
  if (isRemove) {
    labelInput.value = "";
  }
}

document.addEventListener("DOMContentLoaded", async () => {
  setupLanguageControls();
  setupNavigation();
  bindActions();
  setupClearScheduleForm();
  initCellEditor();
  resetNurseForm();
  setupConstraintDatalist();
  setupAuthControls();
  await loadSettings();
  setLanguage(state.lang);
  const restored = await restoreSession();
  if (restored) {
    await bootstrapApp();
  } else {
    window.location.href = "/login";
  }
});

function setupLanguageControls() {
  const selector = document.getElementById("langSelect");
  if (!selector) return;
  selector.innerHTML = "";
  const pt = document.createElement("option");
  pt.value = "pt";
  pt.textContent = t("lang.pt", "Português");
  const en = document.createElement("option");
  en.value = "en";
  en.textContent = t("lang.en", "Inglês");
  selector.appendChild(pt);
  selector.appendChild(en);
  selector.value = state.lang;
  selector.onchange = () => {
    setLanguage(selector.value);
  };
}

function setLanguage(lang) {
  state.lang = lang === "en" ? "en" : "pt";
  localStorage.setItem("shiftflow_lang", state.lang);
  document.documentElement.lang = state.lang;
  monthNames = I18N[state.lang].months;
  weekdayLabels = I18N[state.lang].weekdays;
  setupLanguageControls();
  applyTranslations();
  setupSelectors();
  setupClearScheduleForm();
  renderScheduleTable();
  renderScheduleStats();
  renderSwaps();
  renderChatThreads();
  renderChatUsers();
  renderChatRecipientControls();
  renderChatRecipientOptions();
  renderSwapParticipants();
  renderUnfilledList();
  renderViolationsList();
  renderMyConstraintsTable();
  renderMyAvailabilityList();
  renderPendingAvailabilityList();
  updateDashboard();
}

function replaceLabelText(label, text) {
  if (!label) return;
  Array.from(label.childNodes).forEach((node) => {
    if (node.nodeType === Node.TEXT_NODE) {
      label.removeChild(node);
    }
  });
  label.appendChild(document.createTextNode(` ${text} `));
}

function setLabelByControl(controlId, key) {
  const control = document.getElementById(controlId);
  if (!control) return;
  const label = control.closest("label");
  if (!label) return;
  replaceLabelText(label, t(key, label.textContent.trim()));
}

function setPlaceholder(id, key) {
  const el = document.getElementById(id);
  if (!el) return;
  el.placeholder = t(key, el.placeholder || "");
}

function applyTranslations() {
  document.querySelectorAll("[data-i18n]").forEach((el) => {
    const key = el.dataset.i18n;
    if (key) {
      el.textContent = t(key, el.textContent);
    }
  });
  document.querySelectorAll("#chatRecipientMode option[data-i18n]").forEach((el) => {
    const key = el.dataset.i18n;
    if (key) {
      el.textContent = t(key, el.textContent);
    }
  });
  document.querySelectorAll("[data-i18n-placeholder]").forEach((el) => {
    const key = el.dataset.i18nPlaceholder;
    if (key) {
      el.placeholder = t(key, el.placeholder || "");
    }
  });

  const navMap = {
    dashboard: "nav.dashboard",
    nurses: "nav.nurses",
    requirements: "nav.requirements",
    constraints: "nav.constraints",
    rules: "nav.rules",
    teams: "nav.teams",
    services: "nav.services",
    schedule: "nav.schedule",
    swaps: "nav.swaps",
    chat: "nav.chat",
    admin: "nav.admin",
  };
  Object.keys(navMap).forEach((section) => {
    const btn = document.querySelector(`nav button[data-section='${section}']`);
    if (btn) btn.textContent = t(navMap[section], btn.textContent);
  });

  const setText = (selector, key) => {
    const el = document.querySelector(selector);
    if (el) el.textContent = t(key, el.textContent);
  };

  setText("#brandSubtitle", "app.subtitle");
  setText("#logoutBtn", "action.logout");
  setText("#dashboard h2", "section.dashboard");
  setText("#nurses h2", "section.nurses");
  setText("#requirements h2", "section.requirements");
  setText("#constraints h2", "section.constraints");
  setText("#rules h2", "section.rules");
  setText("#schedule h2", "section.schedule");
  setText("#teams h2", "section.teams");
  setText("#services h2", "section.services");
  setText("#swaps h2", "section.swaps");
  setText("#chat h2", "section.chat");
  setText("#admin h2", "section.admin");
  setText("#generateBtn", "dashboard.generate");
  setText("#exportScheduleBtn", "dashboard.export_schedule");
  setText("#exportScheduleBtnMenu", "dashboard.export_schedule");
  setText("#exportConstraintsBtn", "dashboard.export_constraints");
  setText("#statNeeds + small", "dashboard.needs");
  setText("#statAssigned + small", "dashboard.assigned");
  setText("#statLocks + small", "dashboard.locks");
  setText("#statViolations + small", "dashboard.alerts");
  setText("#addNurseBtn", "btn.add_professional");
  setText("#saveRequirementsBtn", "btn.save_requirements");
  setText("#fillRequirementsOnesBtn", "btn.fill_all");
  setText("#clearRequirementsBtn", "btn.clear_all");
  setText("#saveConstraintsBtn", "btn.save_constraints");
  setText("#fillMyAvailableBtn", "btn.available_all");
  setText("#fillMyUnavailableBtn", "btn.unavailable_all");
  setText("#submitAvailabilityBtn", "btn.submit_availability");
  setText("#rulesForm button[type='submit']", "btn.save_rules");
  setText("#manualHolidayForm button[type='submit']", "btn.add_holiday");
  setText("#adjustmentsForm button[type='submit']", "btn.save_adjustments");
  setText("#releaseForm button[type='submit']", "btn.publish");
  setText("#clearScheduleForm button[type='submit']", "btn.clear_schedule");
  setText("#exportSwapsBtn", "label.export_swaps");
  setText("#swapForm button[type='submit']", "label.swap_send");
  setText("#chatForm button[type='submit']", "btn.send");
  setText("#settingsForm button[type='submit']", "btn.save");
  setText("#logoUploadForm button[type='submit']", "label.upload_logos");
  setText("#categoryForm button[type='submit']", "label.add_category");
  setText("#openUserModalBtn", "label.new_user");
  setText("#seedDemoBtn", "label.create_demos");
  setText("#clearDemoBtn", "label.clear_demos");
  setText("#userModalSubmit", "btn.save");
  setText("#userModalCancel", "btn.cancel");
  setText("#teamModalCancel", "btn.cancel");
  setText("#cellEditorSave", "btn.apply");
  setText("#cellEditorClear", "btn.clear");
  setText("#cellEditorCancel", "btn.cancel");
  setText("#chatUsers + h4", "label.chat_threads");

  setLabelByControl("monthSelect", "label.month");
  setLabelByControl("yearSelect", "label.year");
  setLabelByControl("groupSelect", "label.team");
  setLabelByControl("clearScheduleMonth", "label.month");
  setLabelByControl("clearScheduleYear", "label.year");
  setLabelByControl("releaseTeam", "label.team");
  setLabelByControl("manualHolidayDay", "label.date");
  setLabelByControl("manualHolidayAction", "label.action");
  setLabelByControl("serviceShiftService", "label.service");
  setLabelByControl("serviceShiftShift", "label.shift");
  setLabelByControl("swapParticipants", "label.participants");
  setLabelByControl("nurseNight", "label.can_night");
  setLabelByControl("nurseMaxNight", "label.max_nights");
  setLabelByControl("nurseWeeklyHours", "label.weekly_hours");

  setPlaceholder("nurseName", "placeholder.name");
  setPlaceholder("nurseCategoryCustom", "placeholder.category_other");
  setPlaceholder("teamName", "placeholder.team_name");
  setPlaceholder("teamService", "placeholder.service_code");
  setPlaceholder("serviceCode", "placeholder.service_code");
  setPlaceholder("serviceName", "placeholder.service_name");
  setPlaceholder("shiftCode", "placeholder.shift_code");
  setPlaceholder("shiftLabel", "placeholder.shift_label");
  setPlaceholder("swapService", "placeholder.swap_service");
  setPlaceholder("swapShift", "placeholder.swap_shift");
  setPlaceholder("swapDesiredService", "placeholder.swap_desired_service");
  setPlaceholder("swapDesiredShift", "placeholder.swap_desired_shift");
  setPlaceholder("swapReason", "placeholder.reason_optional");
  setPlaceholder("swapObservations", "placeholder.observations_optional");
  setPlaceholder("chatUserSearch", "placeholder.search_user");
  setPlaceholder("chatMessageInput", "placeholder.chat_message");
  setPlaceholder("chatRecipientUsers", "placeholder.select_users");
  setPlaceholder("chatRecipientRole", "placeholder.select_role");
  setPlaceholder("settingsAppName", "placeholder.app_name");
  setPlaceholder("settingsOrgName", "placeholder.org_name");
  setPlaceholder("categoryName", "placeholder.category_name");
  setPlaceholder("categoryOrder", "placeholder.order");
  setPlaceholder("userUsername", "placeholder.username");
  setPlaceholder("userFullName", "placeholder.full_name");
  setPlaceholder("userPassword", "placeholder.password");
  setPlaceholder("manualHolidayLabel", "label.description");
  setPlaceholder("settingsPdfInfo", "placeholder.pdf_footer");

  if (state.meta) {
    populateRoleSelects();
  }
}

function setupSelectors() {
  const monthSelect = document.getElementById("monthSelect");
  monthSelect.innerHTML = "";
  monthNames.forEach((name, idx) => {
    const option = document.createElement("option");
    option.value = idx + 1;
    option.textContent = name;
    if (idx + 1 === state.month) option.selected = true;
    monthSelect.appendChild(option);
  });

  const yearSelect = document.getElementById("yearSelect");
  yearSelect.innerHTML = "";
  const currentYear = new Date().getFullYear();
  const maxYear = currentYear + 15;
  for (let y = currentYear - 1; y <= maxYear; y += 1) {
    const option = document.createElement("option");
    option.value = y;
    option.textContent = y;
    if (y === state.year) option.selected = true;
    yearSelect.appendChild(option);
  }

  monthSelect.onchange = () => {
    state.month = Number(monthSelect.value);
    refreshMonthData();
    if (canEditSchedule()) {
      loadReleases();
    }
  };
  yearSelect.onchange = () => {
    state.year = Number(yearSelect.value);
    refreshMonthData();
    if (canEditSchedule()) {
      loadReleases();
    }
  };

  const groupSelect = document.getElementById("groupSelect");
  if (groupSelect) {
    groupSelect.value = state.group;
    groupSelect.onchange = () => {
      state.group = groupSelect.value;
      if (state.meta) {
        populateMetaSelectors();
        populateCellEditorOptions();
        renderShiftSettings();
        renderServiceShiftMap();
      }
      syncGroupSelects();
      refreshMonthData();
      loadNurses();
      loadTeams();
      loadServices();
    };
    syncGroupSelects();
  }
}

function populateMonthOptions(select, selected) {
  if (!select) return;
  select.innerHTML = "";
  monthNames.forEach((name, idx) => {
    const option = document.createElement("option");
    option.value = idx + 1;
    option.textContent = name;
    if (selected === idx + 1) option.selected = true;
    select.appendChild(option);
  });
}

function populateYearOptions(select, selected) {
  if (!select) return;
  select.innerHTML = "";
  const currentYear = new Date().getFullYear();
  const maxYear = currentYear + 15;
  for (let y = currentYear - 1; y <= maxYear; y += 1) {
    const option = document.createElement("option");
    option.value = y;
    option.textContent = y;
    if (selected === y) option.selected = true;
    select.appendChild(option);
  }
}

function setupClearScheduleForm() {
  const monthSelect = document.getElementById("clearScheduleMonth");
  const yearSelect = document.getElementById("clearScheduleYear");
  const form = document.getElementById("clearScheduleForm");
  if (!monthSelect || !yearSelect || !form) return;
  populateMonthOptions(monthSelect, state.month);
  populateYearOptions(yearSelect, state.year);
  form.onsubmit = handleClearSchedule;
}

function syncClearScheduleSelectors() {
  const monthSelect = document.getElementById("clearScheduleMonth");
  const yearSelect = document.getElementById("clearScheduleYear");
  if (monthSelect) monthSelect.value = state.month;
  if (yearSelect) yearSelect.value = state.year;
}

function setupNavigation() {
  const buttons = document.querySelectorAll("nav button");
  buttons.forEach((button) => {
    button.addEventListener("click", () => {
      buttons.forEach((btn) => btn.classList.remove("active"));
      button.classList.add("active");
      const sectionId = button.getAttribute("data-section");
      document
        .querySelectorAll("main section")
        .forEach((section) => section.classList.remove("visible"));
      document.getElementById(sectionId).classList.add("visible");
    });
  });
}

function bindActions() {
  document
    .getElementById("nurseForm")
    .addEventListener("submit", handleNurseSubmit);
  document
    .getElementById("cancelEditNurse")
    .addEventListener("click", () => resetNurseForm());
  document.getElementById("addNurseBtn")?.addEventListener("click", (event) => {
    startNurseCreate(event.currentTarget);
  });
  document
    .getElementById("saveRequirementsBtn")
    .addEventListener("click", saveRequirements);
  document
    .getElementById("fillRequirementsOnesBtn")
    ?.addEventListener("click", () => fillRequirementsGrid("1"));
  document
    .getElementById("clearRequirementsBtn")
    ?.addEventListener("click", () => fillRequirementsGrid("0"));
  document
    .getElementById("saveConstraintsBtn")
    .addEventListener("click", saveConstraints);
  document
    .getElementById("submitAvailabilityBtn")
    ?.addEventListener("click", submitAvailabilityRequest);
  document
    .getElementById("fillMyAvailableBtn")
    ?.addEventListener("click", () => fillMyAvailability("DISPONIVEL"));
  document
    .getElementById("fillMyUnavailableBtn")
    ?.addEventListener("click", () => fillMyAvailability("INDISPONIVEL"));
  document.getElementById("generateBtn").addEventListener("click", generate);
  const handleScheduleExport = async () => {
    const format = await chooseExportFormat();
    if (!format) return;
    downloadFile(
      `/api/export/schedule?year=${state.year}&month=${state.month}&${groupQuery()}&format=${format}&lang=${state.lang}`,
      format,
      "schedule"
    );
  };
  const handleConstraintsExport = async () => {
    const format = await chooseExportFormat();
    if (!format) return;
    downloadFile(
      `/api/export/constraints?year=${state.year}&month=${state.month}&${groupQuery()}&format=${format}&lang=${state.lang}`,
      format,
      "constraints"
    );
  };
  document.getElementById("exportScheduleBtn").addEventListener("click", handleScheduleExport);
  document
    .getElementById("exportScheduleBtnMenu")
    ?.addEventListener("click", handleScheduleExport);
  document
    .getElementById("exportConstraintsBtn")
    .addEventListener("click", handleConstraintsExport);
  document
    .getElementById("rulesForm")
    .addEventListener("submit", saveRulesConfig);
  document
    .getElementById("seedDemoBtn")
    ?.addEventListener("click", seedDemoData);
  document
    .getElementById("clearDemoBtn")
    ?.addEventListener("click", clearDemoData);
  document
    .getElementById("manualHolidayForm")
    .addEventListener("submit", handleManualHolidaySubmit);
  const manualAction = document.getElementById("manualHolidayAction");
  if (manualAction) {
    manualAction.addEventListener("change", updateManualHolidayLabelState);
    updateManualHolidayLabelState();
  }
  document
    .getElementById("adjustmentsForm")
    .addEventListener("submit", saveAdjustments);
  const nurseCategorySelect = document.getElementById("nurseCategory");
  if (nurseCategorySelect) {
    nurseCategorySelect.addEventListener("change", () => {
      updateWeeklyHoursVisibility();
      updateServiceMapForCategory(
        nurseCategorySelect.value,
        gatherCodesFromChecklist()
      );
    });
  }
  const nurseCategoryCustom = document.getElementById("nurseCategoryCustom");
  if (nurseCategoryCustom) {
    nurseCategoryCustom.addEventListener("input", () => {
      const value = nurseCategoryCustom.value.trim() || nurseCategorySelect?.value;
      updateServiceMapForCategory(value || "", gatherCodesFromChecklist());
    });
  }
  const repositionPanel = () => {
    const panel = document.getElementById("nurseFormPanel");
    if (
      panel &&
      !panel.classList.contains("hidden") &&
      nurseFormAnchor &&
      document.body.contains(nurseFormAnchor)
    ) {
      positionNurseForm(nurseFormAnchor);
    }
  };
  window.addEventListener("resize", repositionPanel);
  window.addEventListener("scroll", repositionPanel, { passive: true });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      closeCellEditor();
      resetNurseForm();
    }
  });

  document.addEventListener("mousedown", (event) => {
    const editor = document.getElementById("cellEditor");
    if (
      !(editor.classList.contains("hidden") ||
        editor.contains(event.target) ||
        event.target.closest("#scheduleTable"))
    ) {
      closeCellEditor();
    }
    const nursePanel = document.getElementById("nurseFormPanel");
    if (
      nursePanel &&
      !nursePanel.classList.contains("hidden") &&
      !nursePanel.contains(event.target) &&
      !event.target.closest("#nurseTable") &&
      event.target.id !== "addNurseBtn"
    ) {
      resetNurseForm();
    }
  });

  document
    .getElementById("teamForm")
    ?.addEventListener("submit", handleTeamSubmit);
  document
    .getElementById("teamMembersForm")
    ?.addEventListener("submit", saveTeamMembers);
  document
    .getElementById("serviceForm")
    ?.addEventListener("submit", handleServiceSubmit);
  document
    .getElementById("shiftForm")
    ?.addEventListener("submit", handleShiftSubmit);
  document
    .getElementById("serviceShiftForm")
    ?.addEventListener("submit", handleServiceShiftSubmit);
  document
    .getElementById("releaseForm")
    ?.addEventListener("submit", handleReleaseSubmit);
  document
    .getElementById("swapForm")
    ?.addEventListener("submit", handleSwapSubmit);
  document
    .getElementById("exportSwapsBtn")
    ?.addEventListener("click", () =>
      downloadFile(`/api/export/swaps?lang=${state.lang}`, "xlsx", "swaps")
    );
  document
    .getElementById("chatForm")
    ?.addEventListener("submit", handleChatSubmit);
  document
    .getElementById("chatUserSearch")
    ?.addEventListener("input", renderChatUsers);
  document
    .getElementById("chatRecipientMode")
    ?.addEventListener("change", renderChatRecipientControls);
  document
    .getElementById("settingsForm")
    ?.addEventListener("submit", handleSettingsSubmit);
  document
    .getElementById("logoUploadForm")
    ?.addEventListener("submit", handleLogoUpload);
  document
    .getElementById("userForm")
    ?.addEventListener("submit", handleUserSubmit);
  document
    .getElementById("openUserModalBtn")
    ?.addEventListener("click", () => openUserModal());
  document
    .getElementById("userModalCancel")
    ?.addEventListener("click", () => closeUserModal());
  document.getElementById("userModal")?.addEventListener("click", (event) => {
    if (event.target.id === "userModal") closeUserModal();
  });
  document
    .getElementById("categoryForm")
    ?.addEventListener("submit", handleCategorySubmit);
  document
    .getElementById("teamEditForm")
    ?.addEventListener("submit", handleTeamEditSubmit);
  document
    .getElementById("teamModalCancel")
    ?.addEventListener("click", () => closeTeamModal());
  document
    .getElementById("teamModal")
    ?.addEventListener("click", (event) => {
      if (event.target.id === "teamModal") closeTeamModal();
    });
  document
    .getElementById("categoryEditForm")
    ?.addEventListener("submit", handleCategoryEditSubmit);
  document
    .getElementById("categoryModalCancel")
    ?.addEventListener("click", () => closeCategoryModal());
  document
    .getElementById("categoryModal")
    ?.addEventListener("click", (event) => {
      if (event.target.id === "categoryModal") closeCategoryModal();
    });
}

function initCellEditor() {
  const saveBtn = document.getElementById("cellEditorSave");
  const clearBtn = document.getElementById("cellEditorClear");
  const cancelBtn = document.getElementById("cellEditorCancel");
  saveBtn.addEventListener("click", async () => {
    if (!cellEditorContext) return;
    const select = document.getElementById("cellEditorSelect");
    const select2 = document.getElementById("cellEditorSelect2");
    const select3 = document.getElementById("cellEditorSelect3");
    const lock = document.getElementById("cellEditorLock").checked;
    const codes = [select.value, select2.value, select3.value].filter(Boolean);
    const uniqueCodes = [...new Set(codes)];
    if (uniqueCodes.length > 1) {
      const nurse = state.nurses.find(
        (item) => item.id === cellEditorContext.nurseId
      );
      const isRestricted =
        nurse?.category === "ASSISTENTE_OPERACIONAL" ||
        (nurse?.category || "").startsWith("CONTRATADO");
      const typeSet = new Set();
      for (const code of uniqueCodes) {
        const meta = getShiftMeta(code);
        if (meta?.shift_type) {
          if (typeSet.has(meta.shift_type)) {
            alert(t("label.same_shift_type", "Não pode combinar turnos do mesmo tipo no mesmo dia."));
            return;
          }
          typeSet.add(meta.shift_type);
        } else {
          alert(t("label.invalid_shift", "Turno inválido."));
          return;
        }
      }
      if (isRestricted) {
        const pair = [...typeSet].sort().join("");
        if (pair !== "MT") {
          alert(t("label.restricted_combo", "AO e Enf. Contratados só podem fazer M+T."));
          return;
        }
      }
      const overlaps = (a, b) => {
        const intervals = (meta) => {
          if (!meta) return [];
          if (meta.end_minute > meta.start_minute) {
            return [[meta.start_minute, meta.end_minute]];
          }
          return [
            [meta.start_minute, 24 * 60],
            [0, meta.end_minute],
          ];
        };
        const aIntervals = intervals(a);
        const bIntervals = intervals(b);
        return aIntervals.some(
          ([sa, ea]) =>
            bIntervals.some(([sb, eb]) => sa < eb && sb < ea)
        );
      };
      for (let i = 0; i < uniqueCodes.length; i += 1) {
        for (let j = i + 1; j < uniqueCodes.length; j += 1) {
          const a = getShiftMeta(uniqueCodes[i]);
          const b = getShiftMeta(uniqueCodes[j]);
          if (overlaps(a, b)) {
            alert(
              t("label.overlapping_shifts", "Turnos sobrepostos no mesmo dia.")
            );
            return;
          }
        }
      }
    }
    const sortedCodes = uniqueCodes.sort((a, b) => {
      const aMeta = getShiftMeta(a);
      const bMeta = getShiftMeta(b);
      const aStart = aMeta?.start_minute ?? 9999;
      const bStart = bMeta?.start_minute ?? 9999;
      if (aStart !== bStart) return aStart - bStart;
      return a.localeCompare(b);
    });
    try {
      await updateScheduleCell({
        nurse_id: cellEditorContext.nurseId,
        day: cellEditorContext.day,
        shift_codes: sortedCodes,
        locked: lock,
      });
      closeCellEditor();
    } catch (error) {
      alert(error?.message || t("label.save_shift_failed", "Não foi possível guardar o turno."));
    }
  });
  clearBtn.addEventListener("click", async () => {
    if (!cellEditorContext) return;
    await updateScheduleCell({
      nurse_id: cellEditorContext.nurseId,
      day: cellEditorContext.day,
      shift_code: null,
      locked: null,
    });
    closeCellEditor();
  });
  cancelBtn.addEventListener("click", () => closeCellEditor());
}

function openCellEditor(cell) {
  const nurseId = Number(cell.dataset.nurse);
  const day = Number(cell.dataset.day);
  const entry = cell.dataset.entry ? JSON.parse(cell.dataset.entry) : null;
  const codes = cell.dataset.codes ? JSON.parse(cell.dataset.codes) : [];
  const editor = document.getElementById("cellEditor");
  const select = document.getElementById("cellEditorSelect");
  const select2 = document.getElementById("cellEditorSelect2");
  const select3 = document.getElementById("cellEditorSelect3");
  const lock = document.getElementById("cellEditorLock");

  populateCellEditorOptions();
  select.value = codes[0] || (entry ? entry.shift_code : "");
  select2.value = codes[1] || "";
  select3.value = codes[2] || "";
  lock.checked = entry ? entry.locked : false;
  cellEditorContext = { nurseId, day };

  const rect = cell.getBoundingClientRect();
  editor.style.top = `${window.scrollY + rect.top + rect.height + 6}px`;
  editor.style.left = `${window.scrollX + rect.left}px`;
  editor.classList.remove("hidden");
  select.focus();
}

function closeCellEditor() {
  const editor = document.getElementById("cellEditor");
  editor.classList.add("hidden");
  cellEditorContext = null;
}

async function updateScheduleCell(payload) {
  if (!canEditSchedule()) return;
  await httpJson(
    `/api/schedule/cell?year=${state.year}&month=${state.month}`,
    {
      method: "PUT",
      body: JSON.stringify(payload),
    }
  );
  await loadSchedule();
}

async function apiFetch(url, options = {}) {
  const headers = new Headers(options.headers || {});
  if (state.token) {
    headers.set("Authorization", `Bearer ${state.token}`);
  }
  return fetch(url, { ...options, headers });
}

async function httpJson(url, options = {}) {
  const headers = new Headers(options.headers || {});
  if (!(options.body instanceof FormData)) {
    headers.set("Content-Type", "application/json");
  }
  const response = await apiFetch(url, {
    ...options,
    headers,
  });
  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || "Erro inesperado");
  }
  if (response.status === 204) return null;
  return response.json();
}

async function loadMeta() {
  const meta = await httpJson("/api/meta");
  state.meta = meta;
  populateRoleSelects();
  populateMetaSelectors();
  populateCellEditorOptions();
  renderShiftSettings();
  renderServiceShiftMap();
}

function populateMetaSelectors() {
  const categorySelect = document.getElementById("nurseCategory");
  const previousCategory = categorySelect.value;
  categorySelect.innerHTML = "";
  const role = currentGroupRole();
  const categories =
    state.meta.category_map?.[role] || state.meta.categories || [];
  categories.forEach((category) => {
    const option = document.createElement("option");
    option.value = category;
    option.textContent = category;
    categorySelect.appendChild(option);
  });
  if (previousCategory && categories.includes(previousCategory)) {
    categorySelect.value = previousCategory;
  }
  if (!categories.includes(previousCategory)) {
    const customInput = document.getElementById("nurseCategoryCustom");
    if (customInput && previousCategory) {
      customInput.value = previousCategory;
    }
  }

  const servicesSelect = document.getElementById("nurseServices");
  const previousServices = Array.from(servicesSelect.selectedOptions || []).map(
    (opt) => opt.value
  );
  servicesSelect.innerHTML = "";
  state.meta.service_shifts.forEach((shift) => {
    if (shift.service_role && shift.service_role !== role) {
      return;
    }
    const option = document.createElement("option");
    option.value = shift.code;
    option.textContent = shift.label;
    servicesSelect.appendChild(option);
  });
  previousServices.forEach((code) => {
    const option = Array.from(servicesSelect.options).find(
      (opt) => opt.value === code
    );
    if (option) option.selected = true;
  });

  updateServiceMapForCategory(categorySelect.value, previousServices);
  renderConstraintsLegend();
  updateWeeklyHoursVisibility();
}

function resolveRoleForCategory(category) {
  const normalized = (category || "").toLowerCase();
  const map = state.meta?.category_map || {};
  for (const role of Object.keys(map)) {
    const items = map[role] || [];
    if (items.some((item) => item.toLowerCase() === normalized)) {
      return role;
    }
  }
  return category || "ENFERMEIRO";
}

function buildServiceMap(roleOverride) {
  const map = {};
  const role = roleOverride || currentGroupRole();
  state.meta.service_shifts.forEach((shift) => {
    if (shift.service_role && shift.service_role !== role) {
      return;
    }
    if (!map[shift.service]) {
      map[shift.service] = [];
    }
    map[shift.service].push(shift.code);
  });
  state.serviceMap = map;
}

function updateServiceMapForCategory(category, selectedCodes = []) {
  if (!state.meta) return;
  const role = resolveRoleForCategory(category);
  buildServiceMap(role);
  renderServiceChecklist(selectedCodes);
}

function renderServiceChecklist(selectedCodes = []) {
  const container = document.getElementById("serviceChecklist");
  if (!container) return;
  container.innerHTML = "";
  const selectedSet = new Set(selectedCodes);
  Object.keys(state.serviceMap)
    .sort()
    .forEach((service) => {
      const label = document.createElement("label");
      label.className = "service-item";
      const checkbox = document.createElement("input");
      checkbox.type = "checkbox";
      checkbox.value = service;
      const codes = state.serviceMap[service];
      checkbox.checked = codes.every((code) => selectedSet.has(code));
      checkbox.addEventListener("change", () => {
        const codesFromChecklist = gatherCodesFromChecklist();
        syncServiceSelect(codesFromChecklist);
      });
      const text = document.createElement("span");
      text.textContent = service;
      label.appendChild(checkbox);
      label.appendChild(text);
      container.appendChild(label);
    });
  syncServiceSelect(selectedCodes);
}

function gatherCodesFromChecklist() {
  const codes = new Set();
  document
    .querySelectorAll("#serviceChecklist input[type='checkbox']:checked")
    .forEach((checkbox) => {
      (state.serviceMap[checkbox.value] || []).forEach((code) => {
        codes.add(code);
      });
    });
  return Array.from(codes);
}

function syncServiceSelect(codes) {
  const select = document.getElementById("nurseServices");
  const codeSet = new Set(codes);
  Array.from(select.options).forEach((option) => {
    option.selected = codeSet.has(option.value);
  });
}

function updateWeeklyHoursVisibility() {
  const select = document.getElementById("nurseCategory");
  const wrapper = document.getElementById("weeklyHoursWrapper");
  const input = document.getElementById("nurseWeeklyHours");
  if (!select || !wrapper || !input) return;
  wrapper.style.display = "flex";
  input.disabled = false;
  if (!editingNurseId && !input.value) {
    input.value = 40;
  }
}

function populateCellEditorOptions() {
  if (!state.meta) return;
  const select = document.getElementById("cellEditorSelect");
  const select2 = document.getElementById("cellEditorSelect2");
  const select3 = document.getElementById("cellEditorSelect3");
  const buildOptions = (target) => {
    target.innerHTML = "";
    const blank = document.createElement("option");
    blank.value = "";
    blank.textContent = "—";
    target.appendChild(blank);
    const role = currentGroupRole();
    state.meta.service_shifts.forEach((shift) => {
      if (shift.service_role && shift.service_role !== role) {
        return;
      }
      const option = document.createElement("option");
      option.value = shift.code;
      option.textContent = shift.label;
      target.appendChild(option);
    });
  };
  buildOptions(select);
  buildOptions(select2);
  buildOptions(select3);
  ["D", "F"].forEach((code) => {
    const option = document.createElement("option");
    option.value = code;
    option.textContent = code;
    select.appendChild(option);
    select2.appendChild(option.cloneNode(true));
    select3.appendChild(option.cloneNode(true));
  });
}

function renderConstraintsLegend() {
  if (!state.meta) return;
  const legend = document.getElementById("constraintsLegend");
  legend.innerHTML = "";
  const options = buildConstraintOptions().filter(
    ({ code }) => code !== "FERIADO_TRAB"
  );
  if (!options.length) {
    options.push({ code: "", label: "Livre" });
  }
  const baseOptions = options.filter(
    ({ code }) =>
      !code.startsWith("DISPONIVEL_") && !code.startsWith("INDISPONIVEL_")
  );
  baseOptions.forEach(({ code, label }) => {
    const tag = document.createElement("span");
    tag.textContent = `${code || "Livre"} - ${label}`;
    tag.className = "legend-tag";
    legend.appendChild(tag);
  });
  const comboTitle = document.createElement("p");
  comboTitle.className = "hint";
  comboTitle.textContent =
    "Escreve combinações com M, T, L, N (ex.: MTLN, TL, L, MT); prefixa com I (ex.: IMN) para indisponibilidades. As variantes Ls/TLs também são aceites. Deixa vazio para seguir a regra da categoria.";
  legend.appendChild(comboTitle);
  const tip = document.createElement("p");
  tip.className = "hint";
  tip.textContent =
    "F = pedido de folga, D = pedido de descanso, D/F = descanso ou folga, FERIAS = marca férias, DS = descanso/dispensa obrigatório.";
  legend.appendChild(tip);
}

async function loadNurses() {
  state.nurses = await httpJson(`/api/nurses?${groupQuery()}`);
  renderNurses();
  if (canEditSchedule()) {
    renderConstraintsGrid();
  }
  renderScheduleTable();
}

function renderNurses() {
  const tbody = document.querySelector("#nurseTable tbody");
  tbody.innerHTML = "";
  const editable = canEditSchedule();
  getSortedNurses().forEach((nurse) => {
    const row = document.createElement("tr");
    const balanceHours = formatHours(nurse.hour_balance_minutes || 0);
    const linkedUser = state.users.find((user) => user.id === nurse.user_id);
    const userLabel = linkedUser
      ? `${linkedUser.full_name} (${linkedUser.username})`
      : "-";
    row.innerHTML = `
      <td>${nurse.name}</td>
      <td>${userLabel}</td>
      <td>${nurse.services_permitted.join(", ")}</td>
      <td>${nurse.weekly_hours || 0}</td>
      <td>${balanceHours}</td>
      <td>
        ${editable
          ? `<button type="button" data-action="edit" data-id="${nurse.id}">${t("btn.edit", "Editar")}</button>
        <button type="button" data-action="delete" data-id="${nurse.id}">${t("btn.delete", "Eliminar")}</button>`
          : "-"}
      </td>
    `;
    tbody.appendChild(row);
  });
  if (!editable) return;
  tbody.querySelectorAll("button[data-action]").forEach((button) => {
    button.addEventListener("click", (event) => {
      const id = Number(event.currentTarget.getAttribute("data-id"));
      const action = event.currentTarget.getAttribute("data-action");
      const nurse = state.nurses.find((n) => n.id === id);
      if (!nurse) return;
      if (action === "edit") {
        startNurseEdit(nurse, event.currentTarget);
      } else if (action === "delete") {
        deleteNurse(nurse);
      }
    });
  });
}

function renderNurseUserOptions(selectedId) {
  const select = document.getElementById("nurseUser");
  if (!select) return;
  select.innerHTML = "";
  const role = currentGroupRole();
  const allowedRoles =
    role === "ENFERMEIRO" ? ["ENFERMEIRO", "COORDENADOR"] : [role];
  const usedUserIds = new Set(
    state.nurses.filter((nurse) => nurse.user_id).map((nurse) => nurse.user_id)
  );
  const placeholder = document.createElement("option");
  placeholder.value = "";
  placeholder.textContent = t("placeholder.select_user", "Selecionar utilizador");
  select.appendChild(placeholder);
  state.users
    .filter((user) => allowedRoles.includes(user.role))
    .filter((user) => !usedUserIds.has(user.id) || user.id === selectedId)
    .forEach((user) => {
      const option = document.createElement("option");
      option.value = user.id;
      option.textContent = `${user.full_name} (${user.username})`;
      if (selectedId && user.id === selectedId) option.selected = true;
      select.appendChild(option);
    });
}

async function loadUsers() {
  if (!state.user) return;
  try {
    state.users = await httpJson("/api/users");
  } catch (error) {
    state.users = [];
  }
  if (!state.group && state.user?.role) {
    state.group = state.user.role;
  }
  renderNurseUserOptions();
  renderNurses();
  renderTeamMemberSelector();
  renderSwapParticipants();
  renderChatUsers();
  renderChatRecipientOptions();
}

async function loadAdminUsers() {
  if (!isAdmin()) return;
  state.adminUsers = await httpJson("/api/auth/users");
  renderAdminUsers();
}

async function loadCategories() {
  if (!isAdmin() && !isCoordinator()) return;
  state.categoriesAdmin = await httpJson("/api/categories");
  renderCategories();
}

function renderCategories() {
  const tbody = document.querySelector("#categoryTable tbody");
  if (!tbody) return;
  tbody.innerHTML = "";
  state.categoriesAdmin.forEach((category) => {
    const roleLabel = formatRole(category.role);
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${category.name}</td>
      <td>${roleLabel}</td>
      <td>${category.sort_order}</td>
      <td>${category.is_active ? t("label.yes", "Sim") : t("label.no", "Não")}</td>
      <td>
        <button type="button" data-action="toggle" data-id="${category.id}">
          ${category.is_active ? t("btn.deactivate", "Desativar") : t("btn.activate", "Ativar")}
        </button>
        <button type="button" data-action="edit" data-id="${category.id}">${t("btn.edit", "Editar")}</button>
        <button type="button" data-action="delete" data-id="${category.id}">${t("btn.delete", "Eliminar")}</button>
      </td>
    `;
    tbody.appendChild(row);
  });
  tbody.querySelectorAll("button[data-action]").forEach((button) => {
    button.addEventListener("click", async (event) => {
      const id = Number(event.currentTarget.dataset.id);
      const action = event.currentTarget.dataset.action;
      const category = state.categoriesAdmin.find((item) => item.id === id);
      if (!category) return;
      if (action === "toggle") {
        await httpJson(`/api/categories/${id}`, {
          method: "PUT",
          body: JSON.stringify({ is_active: !category.is_active }),
        });
        await loadCategories();
        await loadMeta();
        return;
      }
      if (action === "edit") {
        openCategoryModal(category);
        return;
      }
      if (action === "delete") {
        if (
          !confirm(
            `${t("confirm.delete_category", "Apagar categoria")} ${category.name}?`
          )
        )
          return;
        await httpJson(`/api/categories/${id}`, { method: "DELETE" });
        await loadCategories();
        await loadMeta();
      }
    });
  });
}

async function handleCategorySubmit(event) {
  event.preventDefault();
  const name = document.getElementById("categoryName").value.trim();
  const role = document.getElementById("categoryRole").value.trim();
  const orderValue = document.getElementById("categoryOrder").value;
  if (!name || !role) return;
  await httpJson("/api/categories", {
    method: "POST",
    body: JSON.stringify({
      name,
      role,
      sort_order: orderValue ? Number(orderValue) : 0,
      is_active: true,
    }),
  });
  event.target.reset();
  await loadCategories();
  await loadMeta();
}

function openUserModal(user) {
  const modal = document.getElementById("userModal");
  if (!modal) return;
  editingUserId = user ? user.id : null;
  document.getElementById("userModalTitle").textContent = user
    ? `${t("btn.edit", "Editar")} ${user.username}`
    : t("label.new_user", "Novo utilizador");
  const usernameInput = document.getElementById("userUsername");
  const nameInput = document.getElementById("userFullName");
  const roleSelect = document.getElementById("userRole");
  const passwordInput = document.getElementById("userPassword");
  const activeInput = document.getElementById("userActive");
  usernameInput.value = user?.username || "";
  usernameInput.disabled = Boolean(user);
  nameInput.value = user?.full_name || "";
  roleSelect.value = user?.role || "ENFERMEIRO";
  passwordInput.value = "";
  passwordInput.placeholder = user
    ? t("placeholder.new_password_optional", "Nova password (opcional)")
    : t("placeholder.password", "Password");
  activeInput.checked = user ? user.is_active : true;
  modal.classList.remove("hidden");
}

function closeUserModal() {
  const modal = document.getElementById("userModal");
  if (!modal) return;
  modal.classList.add("hidden");
  editingUserId = null;
}

function openCategoryModal(category) {
  const modal = document.getElementById("categoryModal");
  if (!modal) return;
  editingCategoryId = category?.id || null;
  document.getElementById("categoryModalTitle").textContent = category
    ? `${t("btn.edit", "Editar")} ${category.name}`
    : t("label.category", "Categoria");
  document.getElementById("categoryEditName").value = category?.name || "";
  document.getElementById("categoryEditRole").value =
    category?.role || "ENFERMEIRO";
  document.getElementById("categoryEditOrder").value =
    category?.sort_order ?? 0;
  document.getElementById("categoryEditActive").checked =
    category?.is_active ?? true;
  modal.classList.remove("hidden");
}

function closeCategoryModal() {
  const modal = document.getElementById("categoryModal");
  if (!modal) return;
  modal.classList.add("hidden");
  editingCategoryId = null;
}

async function handleCategoryEditSubmit(event) {
  event.preventDefault();
  if (!editingCategoryId) return;
  const name = document.getElementById("categoryEditName").value.trim();
  const role = document.getElementById("categoryEditRole").value.trim();
  const orderValue = document.getElementById("categoryEditOrder").value;
  const isActive = document.getElementById("categoryEditActive").checked;
  if (!name || !role) return;
  await httpJson(`/api/categories/${editingCategoryId}`, {
    method: "PUT",
    body: JSON.stringify({
      name,
      role,
      sort_order: orderValue ? Number(orderValue) : 0,
      is_active: isActive,
    }),
  });
  closeCategoryModal();
  await loadCategories();
  await loadMeta();
}

function renderAdminUsers() {
  const tbody = document.querySelector("#userTable tbody");
  if (!tbody) return;
  tbody.innerHTML = "";
  state.adminUsers.forEach((user) => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${user.username}</td>
      <td>${user.full_name}</td>
      <td>${formatRole(user.role)}</td>
      <td>${user.is_active ? t("status.active", "Ativo") : t("status.inactive", "Inativo")}</td>
      <td>
        <button type="button" data-action="edit" data-id="${user.id}">${t("btn.edit", "Editar")}</button>
        <button type="button" data-action="delete" data-id="${user.id}">${t("btn.delete", "Eliminar")}</button>
      </td>
    `;
    tbody.appendChild(row);
  });
  tbody.querySelectorAll("button[data-action]").forEach((button) => {
    button.addEventListener("click", async (event) => {
      const id = Number(event.currentTarget.dataset.id);
      const action = event.currentTarget.dataset.action;
      const user = state.adminUsers.find((item) => item.id === id);
      if (!user) return;
      if (action === "delete") {
        if (!confirm(`${t("confirm.delete_user", "Eliminar utilizador")} ${user.username}?`)) return;
        await httpJson(`/api/auth/users/${id}`, { method: "DELETE" });
        await loadAdminUsers();
        await loadUsers();
        return;
      }
      if (action === "edit") {
        openUserModal(user);
      }
    });
  });
}

async function loadTeams() {
  if (!isAdmin() && !isCoordinator()) return;
  state.teams = await httpJson(`/api/teams?${groupQuery()}`);
  renderTeams();
  renderReleaseTeamSelect();
  renderTeamMemberSelector();
}

function renderTeams() {
  const tbody = document.querySelector("#teamTable tbody");
  if (!tbody) return;
  tbody.innerHTML = "";
  state.teams.forEach((team) => {
    const row = document.createElement("tr");
    const roleLabel = formatRole(team.role);
    row.innerHTML = `
      <td>${team.name}</td>
      <td>${team.service_code || "-"}</td>
      <td>${roleLabel}</td>
      <td>${team.is_active ? t("status.active", "Ativa") : t("status.inactive", "Inativa")}</td>
      <td>
        <button type="button" data-action="edit" data-id="${team.id}">${t("btn.edit", "Editar")}</button>
        <button type="button" data-action="delete" data-id="${team.id}">${t("btn.delete", "Eliminar")}</button>
      </td>
    `;
    tbody.appendChild(row);
  });
  tbody.querySelectorAll("button[data-action]").forEach((button) => {
    button.addEventListener("click", async (event) => {
      const id = Number(event.currentTarget.dataset.id);
      const action = event.currentTarget.dataset.action;
      const team = state.teams.find((item) => item.id === id);
      if (!team) return;
      if (action === "delete") {
        if (!confirm(`${t("confirm.delete_team", "Eliminar equipa")} ${team.name}?`)) return;
        await httpJson(`/api/teams/${id}`, { method: "DELETE" });
        await loadTeams();
        return;
      }
      if (action === "edit") {
        openTeamModal(team);
      }
    });
  });
}

function openTeamModal(team) {
  const modal = document.getElementById("teamModal");
  if (!modal) return;
  editingTeamId = team?.id || null;
  document.getElementById("teamModalTitle").textContent = team
    ? `${t("btn.edit", "Editar")} ${team.name}`
    : t("label.new_team", "Nova equipa");
  const nameInput = document.getElementById("teamEditName");
  const roleSelect = document.getElementById("teamEditRole");
  const serviceSelect = document.getElementById("teamEditService");
  nameInput.value = team?.name || "";
  roleSelect.value = team?.role || currentGroupRole();
  populateTeamServiceOptions(roleSelect.value, team?.service_code || "");
  roleSelect.onchange = () => {
    populateTeamServiceOptions(roleSelect.value, serviceSelect.value);
  };
  modal.classList.remove("hidden");
}

function populateTeamServiceOptions(role, selected) {
  const serviceSelect = document.getElementById("teamEditService");
  if (!serviceSelect) return;
  const previous = selected || "";
  serviceSelect.innerHTML = `<option value="">${t("services.none_service", "Sem serviço")}</option>`;
  state.services
    .filter((service) => !role || service.role === role)
    .forEach((service) => {
      const option = document.createElement("option");
      option.value = service.code;
      option.textContent = `${service.name} (${service.code})`;
      if (option.value === previous) option.selected = true;
      serviceSelect.appendChild(option);
    });
}

function closeTeamModal() {
  const modal = document.getElementById("teamModal");
  if (!modal) return;
  modal.classList.add("hidden");
  editingTeamId = null;
}

async function handleTeamEditSubmit(event) {
  event.preventDefault();
  const name = document.getElementById("teamEditName").value.trim();
  const role = document.getElementById("teamEditRole").value;
  const serviceCode = document.getElementById("teamEditService").value.trim();
  if (!editingTeamId || !name) return;
  await httpJson(`/api/teams/${editingTeamId}`, {
    method: "PUT",
    body: JSON.stringify({
      name,
      role,
      service_code: serviceCode || null,
    }),
  });
  closeTeamModal();
  await loadTeams();
}

function renderTeamMemberSelector() {
  const select = document.getElementById("teamMembersSelect");
  if (!select) return;
  select.innerHTML = "";
  const list = document.getElementById("teamMembersList");
  if (list) list.innerHTML = "";
  const role = currentGroupRole();
  state.teams
    .filter((team) => team.role === role)
    .forEach((team) => {
    const option = document.createElement("option");
    option.value = team.id;
    option.textContent = team.name;
    select.appendChild(option);
  });
  select.onchange = () => loadTeamMembers(select.value);
  if (select.options.length) {
    loadTeamMembers(select.value);
  }
}

async function loadTeamMembers(teamId) {
  const list = document.getElementById("teamMembersList");
  if (!list) return;
  list.innerHTML = "";
  const team = state.teams.find((item) => item.id === Number(teamId));
  const roleFilter = team?.role;
  const members = await httpJson(`/api/teams/${teamId}/members`);
  const memberIds = new Set(members.map((item) => item.id));
  state.users
    .filter((user) => {
      if (!roleFilter) return true;
      if (roleFilter === "ENFERMEIRO") {
        return ["ENFERMEIRO", "COORDENADOR"].includes(user.role);
      }
      return user.role === roleFilter;
    })
    .forEach((user) => {
    const label = document.createElement("label");
    label.className = "service-item";
    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.value = user.id;
    checkbox.checked = memberIds.has(user.id);
    const text = document.createElement("span");
    text.textContent = `${user.full_name} (${formatRole(user.role)})`;
    label.appendChild(checkbox);
    label.appendChild(text);
    list.appendChild(label);
  });
}

async function saveTeamMembers(event) {
  event.preventDefault();
  const select = document.getElementById("teamMembersSelect");
  if (!select) return;
  const teamId = Number(select.value);
  const userIds = Array.from(
    document.querySelectorAll("#teamMembersList input:checked")
  ).map((input) => Number(input.value));
  await httpJson(`/api/teams/${teamId}/members`, {
    method: "PUT",
    body: JSON.stringify({ user_ids: userIds }),
  });
}

async function loadServices() {
  if (!isAdmin() && !isCoordinator()) return;
  state.services = await httpJson(`/api/services?${groupQuery()}`);
  state.shifts = await httpJson("/api/shifts/catalog");
  renderServices();
  renderShifts();
  renderServiceShiftMap();
}

function renderServices() {
  const tbody = document.querySelector("#serviceTable tbody");
  if (!tbody) return;
  tbody.innerHTML = "";
  const role = currentGroupRole();
  state.services
    .filter((service) => service.role === role)
    .forEach((service) => {
      const row = document.createElement("tr");
      const roleLabel = formatRole(service.role);
      row.innerHTML = `
        <td>${service.code}</td>
        <td>${service.name}</td>
        <td>${roleLabel}</td>
        <td><span class="color-dot" style="background:${service.color}"></span></td>
        <td>
          <button type="button" data-action="delete" data-code="${service.code}">${t("btn.delete", "Eliminar")}</button>
        </td>
      `;
      tbody.appendChild(row);
    });
  tbody.querySelectorAll("button[data-action]").forEach((button) => {
    button.addEventListener("click", async (event) => {
      const code = event.currentTarget.dataset.code;
      if (!confirm(`${t("confirm.delete_service", "Eliminar serviço")} ${code}?`)) return;
      await httpJson(`/api/services/${code}`, { method: "DELETE" });
      await loadServices();
      await loadMeta();
    });
  });
}

function renderShifts() {
  const tbody = document.querySelector("#shiftTable tbody");
  if (!tbody) return;
  tbody.innerHTML = "";
  state.shifts.forEach((shift) => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${shift.code}</td>
      <td>${shift.label}</td>
      <td>${shift.shift_type}</td>
      <td>${minutesToTime(shift.start_minute)}</td>
      <td>${minutesToTime(shift.end_minute)}</td>
      <td>
        <button type="button" data-action="delete" data-code="${shift.code}">${t("btn.delete", "Eliminar")}</button>
      </td>
    `;
    tbody.appendChild(row);
  });
  tbody.querySelectorAll("button[data-action]").forEach((button) => {
    button.addEventListener("click", async (event) => {
      const code = event.currentTarget.dataset.code;
      if (!confirm(`${t("confirm.delete_shift", "Eliminar turno")} ${code}?`)) return;
      await httpJson(`/api/shifts/catalog/${code}`, { method: "DELETE" });
      await loadServices();
      await loadMeta();
    });
  });
  const serviceSelect = document.getElementById("serviceShiftService");
  const shiftSelect = document.getElementById("serviceShiftShift");
  if (serviceSelect) {
    serviceSelect.innerHTML = "";
    const role = currentGroupRole();
    state.services
      .filter((service) => service.role === role)
      .forEach((service) => {
      const option = document.createElement("option");
      option.value = service.code;
      option.textContent = `${service.code} - ${service.name}`;
      serviceSelect.appendChild(option);
    });
  }
  if (shiftSelect) {
    shiftSelect.innerHTML = "";
    state.shifts.forEach((shift) => {
      const option = document.createElement("option");
      option.value = shift.code;
      option.textContent = `${shift.code} - ${shift.label}`;
      shiftSelect.appendChild(option);
    });
  }
}

function renderServiceShiftMap() {
  const tbody = document.querySelector("#serviceShiftTable tbody");
  if (!tbody || !state.meta) return;
  tbody.innerHTML = "";
  const role = currentGroupRole();
  state.meta.service_shifts
    .filter((item) => !item.service_role || item.service_role === role)
    .forEach((item) => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${item.service}</td>
      <td>${item.code}</td>
      <td>
        <button type="button" data-action="delete" data-service="${item.service_code}" data-shift="${item.code}">${t("btn.delete", "Eliminar")}</button>
      </td>
    `;
    tbody.appendChild(row);
  });
  tbody.querySelectorAll("button[data-action]").forEach((button) => {
    button.addEventListener("click", async (event) => {
      const serviceCode = event.currentTarget.dataset.service;
      const shiftCode = event.currentTarget.dataset.shift;
      await httpJson(
        `/api/service-shifts?service_code=${serviceCode}&shift_code=${shiftCode}`,
        { method: "DELETE" }
      );
      await loadMeta();
      await loadServices();
    });
  });
}

async function loadReleases() {
  if (!isAdmin() && !isCoordinator()) return;
  state.releases = await httpJson(
    `/api/releases?year=${state.year}&month=${state.month}`
  );
  renderReleaseTeamSelect();
}

function renderReleaseTeamSelect() {
  const select = document.getElementById("releaseTeam");
  if (!select) return;
  select.innerHTML = "";
  const role = currentGroupRole();
  const teams = state.teams.filter((team) => team.role === role);
  if (!teams.length) {
    const option = document.createElement("option");
    option.textContent = t("teams.none", "Sem equipas");
    option.value = "";
    select.appendChild(option);
    return;
  }
  const releasedIds = new Set(state.releases.map((item) => item.team_id));
  teams.forEach((team) => {
    const option = document.createElement("option");
    option.value = team.id;
    option.textContent = team.name;
    if (releasedIds.has(team.id)) {
      option.textContent = `${team.name} ${t("label.published", "(publicado)")}`;
      option.disabled = true;
    }
    select.appendChild(option);
  });
}

async function loadChatThreads() {
  if (!state.user) return;
  state.chatThreads = await httpJson("/api/chat/threads");
  renderChatThreads();
}

function renderChatThreads() {
  const container = document.getElementById("chatThreads");
  if (!container) return;
  container.innerHTML = "";
  const unreadTotal = state.chatThreads.reduce(
    (sum, thread) => sum + (thread.unread_count || 0),
    0
  );
  setBadge("chatBadge", unreadTotal);
  if (!state.chatThreads.length) {
    container.textContent = t("chat.none_threads", "Sem conversas.");
    return;
  }
  const roleOrder = [
    "ADMIN",
    "COORDENADOR",
    ...availableRoles(),
  ];
  const grouped = {};
  state.chatThreads.forEach((thread) => {
    const role = thread.peer_role || "OUTROS";
    if (!grouped[role]) grouped[role] = [];
    grouped[role].push(thread);
  });
  Object.keys(grouped)
    .sort((a, b) => {
      const ia = roleOrder.includes(a) ? roleOrder.indexOf(a) : 999;
      const ib = roleOrder.includes(b) ? roleOrder.indexOf(b) : 999;
      return ia - ib || a.localeCompare(b);
    })
    .forEach((role) => {
      const group = document.createElement("div");
      group.className = "chat-group";
      const title = document.createElement("div");
      title.className = "chat-group-title";
      title.textContent = formatRole(role);
      group.appendChild(title);
      grouped[role].forEach((thread) => {
        const item = document.createElement("div");
        item.className = "chat-thread";
        item.dataset.peerId = thread.peer_id;
        if (thread.peer_id === state.activeChatPeerId) {
          item.classList.add("active");
        }
        item.innerHTML = `
          <div class="chat-thread-header">
            <strong>${thread.peer_name}</strong>
            ${thread.unread_count ? `<span class="badge">${thread.unread_count}</span>` : ""}
          </div>
          <small>${formatRole(thread.peer_role)}</small>
          <p>${thread.last_message || ""}</p>
        `;
        item.addEventListener("click", () => openChat(thread.peer_id));
        const actions = document.createElement("div");
        actions.className = "thread-actions";
        const archiveBtn = document.createElement("button");
        archiveBtn.type = "button";
        archiveBtn.className = "secondary";
        archiveBtn.textContent = t("btn.archive", "Arquivar");
        archiveBtn.addEventListener("click", async (event) => {
          event.stopPropagation();
          await httpJson(`/api/chat/threads/${thread.peer_id}`, {
            method: "PUT",
            body: JSON.stringify({ is_archived: true }),
          });
          await loadChatThreads();
        });
        const deleteBtn = document.createElement("button");
        deleteBtn.type = "button";
        deleteBtn.className = "secondary";
        deleteBtn.textContent = t("btn.delete", "Eliminar");
        deleteBtn.addEventListener("click", async (event) => {
          event.stopPropagation();
          await httpJson(`/api/chat/threads/${thread.peer_id}`, {
            method: "PUT",
            body: JSON.stringify({ is_deleted: true }),
          });
          await loadChatThreads();
        });
        actions.appendChild(archiveBtn);
        actions.appendChild(deleteBtn);
        item.appendChild(actions);
        group.appendChild(item);
      });
      container.appendChild(group);
    });
}

function renderChatUsers() {
  const container = document.getElementById("chatUsers");
  if (!container) return;
  const search = document.getElementById("chatUserSearch");
  const query = (search?.value || "").toLowerCase();
  container.innerHTML = "";
  const roleOrder = [
    "ADMIN",
    "COORDENADOR",
    ...availableRoles(),
  ];
  const users = state.users
    .filter((user) => user.id !== state.user?.id)
    .filter((user) =>
      `${user.full_name} ${user.username}`.toLowerCase().includes(query)
    )
    .sort((a, b) => a.full_name.localeCompare(b.full_name));
  if (!users.length) {
    container.textContent = t("chat.none_users", "Sem utilizadores.");
    return;
  }
  const grouped = {};
  users.forEach((user) => {
    const role = user.role || "OUTROS";
    if (!grouped[role]) grouped[role] = [];
    grouped[role].push(user);
  });
  Object.keys(grouped)
    .sort((a, b) => {
      const ia = roleOrder.includes(a) ? roleOrder.indexOf(a) : 999;
      const ib = roleOrder.includes(b) ? roleOrder.indexOf(b) : 999;
      return ia - ib || a.localeCompare(b);
    })
    .forEach((role) => {
      const group = document.createElement("div");
      group.className = "chat-group";
      const title = document.createElement("div");
      title.className = "chat-group-title";
      title.textContent = formatRole(role);
      group.appendChild(title);
      grouped[role].forEach((user) => {
        const item = document.createElement("div");
        item.className = "chat-user";
        item.innerHTML = `<strong>${user.full_name}</strong><small>${user.username}</small>`;
        item.addEventListener("click", () => openChat(user.id));
        group.appendChild(item);
      });
      container.appendChild(group);
    });
}

function renderChatRecipientOptions() {
  const usersSelect = document.getElementById("chatRecipientUsers");
  const roleSelect = document.getElementById("chatRecipientRole");
  if (!usersSelect || !roleSelect) return;
  usersSelect.innerHTML = "";
  roleSelect.innerHTML = "";
  const placeholderUsers = document.createElement("option");
  placeholderUsers.value = "";
  placeholderUsers.disabled = true;
  placeholderUsers.textContent = t("placeholder.select_users", "Selecionar utilizadores");
  usersSelect.appendChild(placeholderUsers);
  state.users
    .filter((user) => user.id !== state.user?.id)
    .sort((a, b) => a.full_name.localeCompare(b.full_name))
    .forEach((user) => {
      const option = document.createElement("option");
      option.value = user.id;
      option.textContent = `${user.full_name} (${formatRole(user.role)})`;
      usersSelect.appendChild(option);
    });
  const placeholderRole = document.createElement("option");
  placeholderRole.value = "";
  placeholderRole.textContent = t("placeholder.select_role", "Selecionar perfil");
  roleSelect.appendChild(placeholderRole);
  const roleOptions = ["ADMIN", "COORDENADOR", ...availableRoles()];
  roleOptions.forEach((role) => {
    const option = document.createElement("option");
    option.value = role;
    option.textContent = formatRole(role);
    roleSelect.appendChild(option);
  });
}

function renderChatRecipientControls() {
  const modeSelect = document.getElementById("chatRecipientMode");
  const usersWrap = document.getElementById("chatRecipientUsersWrap");
  const roleWrap = document.getElementById("chatRecipientRoleWrap");
  if (!modeSelect || !usersWrap || !roleWrap) return;
  const mode = modeSelect.value;
  usersWrap.classList.toggle("hidden", mode !== "users");
  roleWrap.classList.toggle("hidden", mode !== "role");
}

async function openChat(peerId) {
  state.activeChatPeerId = peerId;
  const modeSelect = document.getElementById("chatRecipientMode");
  const usersSelect = document.getElementById("chatRecipientUsers");
  if (modeSelect) {
    modeSelect.value = "users";
    renderChatRecipientControls();
  }
  if (usersSelect) {
    Array.from(usersSelect.options).forEach((opt) => {
      opt.selected = Number(opt.value) === peerId;
    });
  }
  await loadChatMessages(peerId);
  await loadChatThreads();
  const header = document.getElementById("chatHeader");
  const user = state.users.find((item) => item.id === peerId);
  if (header) {
    header.textContent = user
      ? `${user.full_name} (${formatRole(user.role)})`
      : "";
  }
}

async function loadChatMessages(peerId) {
  state.chatMessages = await httpJson(`/api/chat/messages?peer_id=${peerId}`);
  renderChatMessages();
}

function renderChatMessages() {
  const container = document.getElementById("chatMessages");
  if (!container) return;
  container.innerHTML = "";
  if (!state.activeChatPeerId) {
    container.textContent = t("chat.select_thread", "Seleciona uma conversa.");
    return;
  }
  if (!state.chatMessages.length) {
    container.textContent = t("chat.none_messages", "Sem mensagens.");
    return;
  }
  state.chatMessages.forEach((message) => {
    const bubble = document.createElement("div");
    bubble.className =
      "chat-message" +
      (message.from_user_id === state.user?.id ? " self" : "");
    const match = message.message.match(/\[SWAP_ID=(\d+)\]/);
    const cleanText = message.message.replace(/\s*\[SWAP_ID=\d+\]/, "");
    const text = document.createElement("span");
    text.textContent = cleanText;
    bubble.appendChild(text);
    if (match) {
      const actions = document.createElement("div");
      actions.className = "chat-message-actions";
      const exportBtn = document.createElement("button");
      exportBtn.type = "button";
      exportBtn.textContent = t(
        "label.swap_export_proof",
        "Exportar comprovativo"
      );
      exportBtn.addEventListener("click", () => {
        downloadFile(
          `/api/swaps/${match[1]}/export?format=pdf&lang=${state.lang}`,
          "pdf",
          "swap-proof",
          `swap_${match[1]}.pdf`
        );
      });
      actions.appendChild(exportBtn);
      bubble.appendChild(actions);
    }
    container.appendChild(bubble);
  });
  container.scrollTop = container.scrollHeight;
}

async function loadSwaps() {
  if (!state.user) return;
  state.swaps = await httpJson("/api/swaps");
  renderSwaps();
}

function renderSwaps() {
  const container = document.getElementById("swapList");
  if (!container) return;
  container.innerHTML = "";
  const pendingCount = state.swaps.reduce((sum, swap) => {
    if (!state.user) return sum;
    if (swap.status === "PENDING_COORDINATOR" && canEditSchedule()) {
      return sum + 1;
    }
    if (swap.status === "PENDING_PARTICIPANTS") {
      const pending = swap.participants?.find(
        (item) => item.user_id === state.user.id && item.status === "PENDING"
      );
      if (pending) return sum + 1;
    }
    return sum;
  }, 0);
  setBadge("swapsBadge", pendingCount);
  if (!state.swaps.length) {
    container.textContent = t("swaps.none", "Sem pedidos ativos.");
    return;
  }
  const statusLabels = {
    PENDING_PARTICIPANTS: t(
      "swap.status.pending_participants",
      "A aguardar participantes"
    ),
    PENDING_COORDINATOR: t(
      "swap.status.pending_coordinator",
      "A aguardar coordenador"
    ),
    APPROVED: t("swap.status.approved", "Aprovado"),
    REJECTED: t("swap.status.rejected", "Rejeitado"),
    REJECTED_BY_PARTICIPANT: t(
      "swap.status.rejected_participant",
      "Recusado por participante"
    ),
  };
  const participantLabels = {
    PENDING: t("swap.participant.pending", "A aguardar"),
    ACCEPTED: t("swap.participant.accepted", "Aceite"),
    REJECTED: t("swap.participant.rejected", "Recusado"),
  };
  state.swaps.forEach((swap) => {
    const wrapper = document.createElement("div");
    wrapper.className = "swap-item";
    const participants = swap.participants
      .map((p) => {
        const user = state.users.find((u) => u.id === p.user_id);
        const label = participantLabels[p.status] || p.status;
        return `${user ? user.full_name : p.user_id}: ${label}`;
      })
      .join(" | ");
    const shiftText =
      swap.shift_code || swap.service_code || swap.desired_shift_code || swap.desired_service_code
        ? `${t("swap.current", "Atual")}: ${swap.service_code || "-"} / ${
            swap.shift_code || "-"
          } · ${t("swap.desired", "Pretendido")}: ${
            swap.desired_service_code || "-"
          } / ${swap.desired_shift_code || "-"}`
        : "";
    const requester = state.users.find((user) => user.id === swap.requester_id);
    const requesterName = requester ? requester.full_name : swap.requester_id;
    const statusLabel = statusLabels[swap.status] || swap.status;
    const decisionText = swap.decision
      ? (() => {
          const coordinator = state.users.find(
            (user) => user.id === swap.decision.coordinator_id
          );
          const coordinatorName = coordinator
            ? coordinator.full_name
            : t("role.coordinator", "Coordenador");
          const reason = swap.decision.reason ? ` (${swap.decision.reason})` : "";
          const decisionLabel = statusLabels[swap.decision.status] || swap.decision.status;
          return `${t("swap.decision", "Decisão")}: ${decisionLabel}${reason} · ${coordinatorName}`;
        })()
      : "";
    const reasonText = swap.reason
      ? `${t("label.reason", "Motivo")}: ${swap.reason}`
      : "";
    const observationsText = swap.observations
      ? `${t("swap.observations", "Observações")}: ${swap.observations}`
      : "";
    const details = `
      <div class="swap-header">
        <strong>${swap.day}/${swap.month}/${swap.year}</strong>
        <span class="swap-status">${statusLabel}</span>
      </div>
      <div class="swap-meta">${t("swap.requested_by", "Pedido por")}: ${requesterName}</div>
      <div>${shiftText}</div>
      <div>${participants}</div>
      <div>${reasonText}</div>
      <div>${observationsText}</div>
      <div>${decisionText}</div>
    `;
    wrapper.innerHTML = details;
    const actions = document.createElement("div");
    actions.className = "swap-actions";
    const participant = swap.participants.find(
      (p) => p.user_id === state.user?.id
    );
    if (participant && participant.status === "PENDING") {
      const acceptBtn = document.createElement("button");
      acceptBtn.textContent = t("btn.accept", "Aceitar");
      acceptBtn.addEventListener("click", async () => {
        await httpJson(`/api/swaps/${swap.id}/participants/me`, {
          method: "PUT",
          body: JSON.stringify({ status: "ACCEPTED" }),
        });
        await loadSwaps();
      });
      const rejectBtn = document.createElement("button");
      rejectBtn.textContent = t("btn.decline", "Recusar");
      rejectBtn.className = "secondary";
      rejectBtn.addEventListener("click", async () => {
        await httpJson(`/api/swaps/${swap.id}/participants/me`, {
          method: "PUT",
          body: JSON.stringify({ status: "REJECTED" }),
        });
        await loadSwaps();
      });
      actions.appendChild(acceptBtn);
      actions.appendChild(rejectBtn);
    }
    const canExport =
      canEditSchedule() ||
      swap.requester_id === state.user?.id ||
      swap.participants.some((p) => p.user_id === state.user?.id);
    if (canExport) {
      const exportBtn = document.createElement("button");
      exportBtn.textContent = t(
        "label.swap_export_proof",
        "Exportar comprovativo"
      );
      exportBtn.addEventListener("click", () => {
        downloadFile(
          `/api/swaps/${swap.id}/export?format=pdf&lang=${state.lang}`,
          "pdf",
          "swap-proof",
          `swap_${swap.id}.pdf`
        );
      });
      actions.appendChild(exportBtn);
    }
    if (isCoordinator() && swap.status === "PENDING_COORDINATOR") {
      const approveBtn = document.createElement("button");
      approveBtn.textContent = t("btn.approve", "Aprovar");
      approveBtn.addEventListener("click", async () => {
        await httpJson(`/api/swaps/${swap.id}/decision`, {
          method: "PUT",
          body: JSON.stringify({ status: "APPROVED" }),
        });
        await loadSwaps();
      });
      const rejectBtn = document.createElement("button");
      rejectBtn.textContent = t("btn.reject", "Rejeitar");
      rejectBtn.className = "secondary";
      rejectBtn.addEventListener("click", async () => {
        const reason =
          prompt(t("label.reject_reason", "Motivo da rejeição"), "") || "";
        await httpJson(`/api/swaps/${swap.id}/decision`, {
          method: "PUT",
          body: JSON.stringify({ status: "REJECTED", reason }),
        });
        await loadSwaps();
      });
      actions.appendChild(approveBtn);
      actions.appendChild(rejectBtn);
    }
    const canDelete =
      isAdmin() ||
      isCoordinator() ||
      (swap.requester_id === state.user?.id && swap.status !== "APPROVED");
    if (canDelete) {
      const deleteBtn = document.createElement("button");
      deleteBtn.textContent = t("btn.delete", "Eliminar");
      deleteBtn.className = "secondary";
      deleteBtn.addEventListener("click", async () => {
        if (!confirm(t("confirm.delete_swap", "Eliminar este pedido de troca?")))
          return;
        await httpJson(`/api/swaps/${swap.id}`, { method: "DELETE" });
        await loadSwaps();
      });
      actions.appendChild(deleteBtn);
    }
    wrapper.appendChild(actions);
    container.appendChild(wrapper);
  });
}

function renderSwapParticipants() {
  const select = document.getElementById("swapParticipants");
  if (!select) return;
  select.innerHTML = "";
  const role = currentGroupRole() || state.user?.role || "";
  let users = state.users
    .filter((user) => user.id !== state.user?.id)
    .filter((user) => (!role ? true : user.role === role))
    .sort((a, b) => a.full_name.localeCompare(b.full_name));
  if (!users.length) {
    users = state.users
      .filter((user) => user.id !== state.user?.id)
      .sort((a, b) => a.full_name.localeCompare(b.full_name));
  }
  const placeholder = document.createElement("option");
  placeholder.value = "";
  placeholder.textContent = t(
    "placeholder.swap_recipient",
    "Selecionar destinatário"
  );
  select.appendChild(placeholder);
  users.forEach((user) => {
      const option = document.createElement("option");
      option.value = user.id;
      option.textContent = `${user.full_name} (${formatRole(user.role)})`;
      select.appendChild(option);
    });
}

async function handleTeamSubmit(event) {
  event.preventDefault();
  const name = document.getElementById("teamName").value.trim();
  const serviceCode = document.getElementById("teamService").value.trim();
  const role = document.getElementById("teamRole").value;
  if (!name) return;
  await httpJson("/api/teams", {
    method: "POST",
    body: JSON.stringify({
      name,
      service_code: serviceCode || null,
      role,
    }),
  });
  event.target.reset();
  await loadTeams();
}

async function handleServiceSubmit(event) {
  event.preventDefault();
  const code = document.getElementById("serviceCode").value.trim();
  const name = document.getElementById("serviceName").value.trim();
  const role = document.getElementById("serviceRole").value;
  const color = document.getElementById("serviceColor").value;
  if (!code || !name) return;
  try {
    await httpJson("/api/services", {
      method: "POST",
      body: JSON.stringify({ code, name, color, role }),
    });
    event.target.reset();
    await loadServices();
    await loadMeta();
  } catch (error) {
    alert(error?.message || t("label.create_service_failed", "Não foi possível criar o serviço."));
  }
}

async function handleShiftSubmit(event) {
  event.preventDefault();
  const code = document.getElementById("shiftCode").value.trim();
  const label = document.getElementById("shiftLabel").value.trim();
  const shiftType = document.getElementById("shiftType").value;
  const start = document.getElementById("shiftStart").value;
  const end = document.getElementById("shiftEnd").value;
  if (!code || !label) return;
  await httpJson("/api/shifts/catalog", {
    method: "POST",
    body: JSON.stringify({
      code,
      label,
      shift_type: shiftType,
      start_time: start,
      end_time: end,
    }),
  });
  event.target.reset();
  await loadServices();
  await loadMeta();
}

async function handleServiceShiftSubmit(event) {
  event.preventDefault();
  const serviceCode = document.getElementById("serviceShiftService").value;
  const shiftCode = document.getElementById("serviceShiftShift").value;
  await httpJson("/api/service-shifts", {
    method: "POST",
    body: JSON.stringify({ service_code: serviceCode, shift_code: shiftCode }),
  });
  await loadMeta();
  await loadServices();
}

async function handleReleaseSubmit(event) {
  event.preventDefault();
  const teamId = Number(document.getElementById("releaseTeam").value);
  if (!teamId) return;
  await httpJson("/api/releases", {
    method: "POST",
    body: JSON.stringify({
      year: state.year,
      month: state.month,
      team_id: teamId,
    }),
  });
  await loadReleases();
}

async function handleSwapSubmit(event) {
  event.preventDefault();
  const dateValue = document.getElementById("swapDate").value;
  if (!dateValue) return;
  const date = new Date(dateValue);
  const participantId = Number(
    document.getElementById("swapParticipants").value
  );
  if (!participantId) {
    alert(t("swap.select_recipient", "Seleciona o destinatário do pedido."));
    return;
  }
  await httpJson("/api/swaps", {
    method: "POST",
    body: JSON.stringify({
      year: date.getFullYear(),
      month: date.getMonth() + 1,
      day: date.getDate(),
      service_code: document.getElementById("swapService").value.trim() || null,
      shift_code: document.getElementById("swapShift").value.trim() || null,
      desired_service_code:
        document.getElementById("swapDesiredService").value.trim() || null,
      desired_shift_code:
        document.getElementById("swapDesiredShift").value.trim() || null,
      reason: document.getElementById("swapReason").value.trim() || null,
      observations: document.getElementById("swapObservations").value.trim() || null,
      participant_ids: [participantId],
    }),
  });
  event.target.reset();
  await loadSwaps();
}

async function handleChatSubmit(event) {
  event.preventDefault();
  const input = document.getElementById("chatMessageInput");
  const message = input.value.trim();
  if (!message) return;
  const mode = document.getElementById("chatRecipientMode")?.value || "users";
  const usersSelect = document.getElementById("chatRecipientUsers");
  const roleSelect = document.getElementById("chatRecipientRole");
  const selectedUsers = usersSelect
    ? Array.from(usersSelect.selectedOptions)
        .map((opt) => Number(opt.value))
        .filter((value) => !Number.isNaN(value))
    : [];
  let payload = null;
  if (mode === "all") {
    payload = { to_all: true, message };
  } else if (mode === "role") {
    const role = roleSelect?.value || "";
    if (!role) return;
    payload = { to_role: role, message };
  } else {
    if (selectedUsers.length > 1) {
      payload = { to_user_ids: selectedUsers, message };
    } else if (selectedUsers.length === 1) {
      payload = { to_user_id: selectedUsers[0], message };
    } else if (state.activeChatPeerId) {
      payload = { to_user_id: state.activeChatPeerId, message };
    } else {
      return;
    }
  }
  await httpJson("/api/chat/messages", {
    method: "POST",
    body: JSON.stringify(payload),
  });
  input.value = "";
  if (state.activeChatPeerId && mode === "users" && selectedUsers.length <= 1) {
    await loadChatMessages(state.activeChatPeerId);
  }
  await loadChatThreads();
}

async function handleSettingsSubmit(event) {
  event.preventDefault();
  await httpJson("/api/settings", {
    method: "PUT",
    body: JSON.stringify({
      app_name: document.getElementById("settingsAppName").value.trim() || null,
      org_name: document.getElementById("settingsOrgName").value.trim() || null,
      show_app_logo: document.getElementById("settingsShowAppLogo").checked,
      show_org_logo: document.getElementById("settingsShowOrgLogo").checked,
      primary_color: document.getElementById("settingsPrimaryColor").value,
      accent_color: document.getElementById("settingsAccentColor").value,
      background: document.getElementById("settingsBackground").value,
      pdf_info_text: document.getElementById("settingsPdfInfo").value || null,
    }),
  });
  await loadSettings();
}

async function handleLogoUpload(event) {
  event.preventDefault();
  const appFile = document.getElementById("logoAppFile").files[0];
  const orgFile = document.getElementById("logoOrgFile").files[0];
  if (appFile) {
    const data = new FormData();
    data.append("target", "app");
    data.append("file", appFile);
    await httpJson("/api/settings/logo", { method: "POST", body: data });
  }
  if (orgFile) {
    const data = new FormData();
    data.append("target", "org");
    data.append("file", orgFile);
    await httpJson("/api/settings/logo", { method: "POST", body: data });
  }
  await loadSettings();
}

async function handleUserSubmit(event) {
  event.preventDefault();
  const username = document.getElementById("userUsername").value.trim();
  const fullName = document.getElementById("userFullName").value.trim();
  const role = document.getElementById("userRole").value;
  const password = document.getElementById("userPassword").value;
  const isActive = document.getElementById("userActive").checked;
  if (!username || !fullName) return;
  if (editingUserId) {
    await httpJson(`/api/auth/users/${editingUserId}`, {
      method: "PUT",
      body: JSON.stringify({
        full_name: fullName,
        role,
        password: password || undefined,
        is_active: isActive,
      }),
    });
  } else {
    if (!password) return;
    await httpJson("/api/auth/users", {
      method: "POST",
      body: JSON.stringify({
        username,
        full_name: fullName,
        role,
        password,
      }),
    });
  }
  event.target.reset();
  closeUserModal();
  await loadAdminUsers();
  await loadUsers();
  await loadNurses();
}

async function seedDemoData() {
  if (!confirm(t("confirm.create_demos", "Criar utilizadores e equipas demo?")))
    return;
  await httpJson("/api/demo/seed", { method: "POST" });
  await loadAdminUsers();
  await loadUsers();
  await loadNurses();
  await loadTeams();
}

async function clearDemoData() {
  if (!confirm(t("confirm.clear_demos", "Apagar todos os dados demo?"))) return;
  await httpJson("/api/demo", { method: "DELETE" });
  await loadAdminUsers();
  await loadUsers();
  await loadNurses();
  await loadTeams();
}

function positionNurseForm(anchorEl) {
  const panel = document.getElementById("nurseFormPanel");
  if (!panel || !anchorEl) return;
  const rect = anchorEl.getBoundingClientRect();
  const viewportWidth = document.documentElement.clientWidth;
  const panelWidth = panel.offsetWidth || 320;
  let left = window.scrollX + rect.left;
  if (left + panelWidth > window.scrollX + viewportWidth - 16) {
    left = window.scrollX + viewportWidth - panelWidth - 16;
  }
  if (left < 8) left = 8;
  const top = window.scrollY + rect.bottom + 8;
  panel.style.left = `${left}px`;
  panel.style.top = `${top}px`;
}

function openNurseForm(anchorEl, title) {
  const panel = document.getElementById("nurseFormPanel");
  if (!panel) return;
  nurseFormAnchor = anchorEl;
  const heading = document.getElementById("nurseFormTitle");
  if (heading) heading.textContent = title;
  panel.classList.remove("hidden");
  positionNurseForm(anchorEl);
}

function startNurseEdit(nurse, anchorEl) {
  editingNurseId = nurse.id;
  document.getElementById("nurseName").value = nurse.name;
  document.getElementById("nurseCategory").value = nurse.category;
  const customCategory = document.getElementById("nurseCategoryCustom");
  if (customCategory) {
    customCategory.value = "";
    if (
      !Array.from(document.getElementById("nurseCategory").options).some(
        (opt) => opt.value === nurse.category
      )
    ) {
      customCategory.value = nurse.category;
    }
  }
  document.getElementById("nurseWeeklyHours").value = nurse.weekly_hours ?? 0;
  renderNurseUserOptions(nurse.user_id);
  document.getElementById("nurseUser").value = nurse.user_id || "";
  document.getElementById("nurseUser").disabled = !isAdmin();
  updateWeeklyHoursVisibility();
  updateServiceMapForCategory(nurse.category, nurse.services_permitted);
  document.getElementById("nurseNight").checked = nurse.can_work_night;
  document.getElementById("nurseMaxNight").value = nurse.max_noites_mes || "";
  document.querySelector("#nurseForm button[type='submit']").textContent =
    t("btn.update", "Atualizar");
  openNurseForm(anchorEl, `${t("label.edit_professional", "Editar")} ${nurse.name}`);
}

function startNurseCreate(anchorEl) {
  resetNurseForm();
  openNurseForm(anchorEl, t("label.new_professional", "Novo profissional"));
}

function resetNurseForm() {
  editingNurseId = null;
  document.getElementById("nurseForm").reset();
  renderNurseUserOptions();
  const customCategory = document.getElementById("nurseCategoryCustom");
  if (customCategory) customCategory.value = "";
  document.getElementById("nurseUser").disabled = !isAdmin();
  document.getElementById("nurseNight").checked = true;
  document.getElementById("nurseMaxNight").value = "";
  document.getElementById("nurseWeeklyHours").value = 40;
  updateWeeklyHoursVisibility();
  updateServiceMapForCategory(
    document.getElementById("nurseCategory").value,
    []
  );
  document.querySelector("#nurseForm button[type='submit']").textContent =
    t("btn.save", "Guardar");
  const panel = document.getElementById("nurseFormPanel");
  if (panel) panel.classList.add("hidden");
}

async function handleNurseSubmit(event) {
  event.preventDefault();
  const name = document.getElementById("nurseName").value.trim();
  const customCategory = document.getElementById("nurseCategoryCustom").value.trim();
  const category = customCategory || document.getElementById("nurseCategory").value;
  const userId = Number(document.getElementById("nurseUser").value);
  const services = gatherCodesFromChecklist();
  const canWorkNight = document.getElementById("nurseNight").checked;
  const maxNight = document.getElementById("nurseMaxNight").value;
  const weeklyRaw = document.getElementById("nurseWeeklyHours").value;
  const weeklyHours = weeklyRaw === "" ? 0 : Number(weeklyRaw);
  if (!name || !userId) return;
  const payload = {
    name,
    category,
    services_permitted: services,
    can_work_night: canWorkNight,
    max_noites_mes: maxNight ? Number(maxNight) : null,
    weekly_hours: weeklyHours,
    user_id: userId,
  };
  if (editingNurseId) {
    await httpJson(`/api/nurses/${editingNurseId}`, {
      method: "PUT",
      body: JSON.stringify(payload),
    });
  } else {
    await httpJson("/api/nurses", {
      method: "POST",
      body: JSON.stringify(payload),
    });
  }
  resetNurseForm();
  await loadNurses();
}

async function deleteNurse(nurse) {
  if (!nurse) return;
  if (!confirm(t("confirm.delete_professional", "Remover profissional?"))) return;
  const adminDeletesUser = isAdmin() && nurse.user_id;
  const endpoint = adminDeletesUser
    ? `/api/auth/users/${nurse.user_id}`
    : `/api/nurses/${nurse.id}`;
  const response = await apiFetch(endpoint, { method: "DELETE" });
  if (!response.ok) {
    const text = await response.text();
    alert(text || t("label.delete_failed", "Não foi possível remover."));
    return;
  }
  if (editingNurseId === nurse.id) {
    resetNurseForm();
  }
  if (adminDeletesUser) {
    await loadAdminUsers();
  }
  await loadNurses();
}

function getDaysInMonth(year, month) {
  return new Date(year, month, 0).getDate();
}

async function loadRequirements() {
  const url = `/api/requirements?year=${state.year}&month=${state.month}&${groupQuery()}`;
  state.requirements = await httpJson(url);
  renderRequirementsGrid();
}

function renderRequirementsGrid() {
  if (!state.meta) return;
  const table = document.getElementById("requirementsTable");
  const days = getDaysInMonth(state.year, state.month);
  const holidaySet = new Set(state.holidays.map((item) => item.day));
  const headerRow = document.createElement("tr");
  const firstTh = document.createElement("th");
  firstTh.textContent = t("label.service_shift", "Serviço / Turno");
  headerRow.appendChild(firstTh);
  for (let day = 1; day <= days; day += 1) {
    const th = document.createElement("th");
    if (holidaySet.has(day)) {
      th.classList.add("holiday-cell");
    }
    if (isWeekend(day)) {
      th.classList.add("weekend-cell");
    }
    th.appendChild(createDayHeader(day, holidaySet.has(day)));
    headerRow.appendChild(th);
  }
  table.innerHTML = "";
  table.appendChild(headerRow);

  const requirementMap = new Map();
  state.requirements.forEach((item) => {
    const key = `${item.service_code}_${item.shift_code}_${item.day}`;
    requirementMap.set(key, item.required_count);
  });

  const typeOrder = { M: 0, T: 1, L: 2, N: 3 };
  const role = currentGroupRole();
  const sortedShifts = state.meta.service_shifts
    .filter((shift) => !shift.service_role || shift.service_role === role)
    .sort((a, b) => {
    if (a.service !== b.service) return a.service.localeCompare(b.service);
    const diff =
      (typeOrder[a.shift_type] ?? 10) - (typeOrder[b.shift_type] ?? 10);
    if (diff !== 0) return diff;
    return a.code.localeCompare(b.code);
  });

  sortedShifts.forEach((shift, rowIdx) => {
    const row = document.createElement("tr");
    const labelCell = document.createElement("td");
    labelCell.className = "req-label";
    const labelWrapper = document.createElement("div");
    const titleLine = document.createElement("div");
    titleLine.className = "req-title";
    const colorDot = document.createElement("span");
    colorDot.className = "color-dot";
    const serviceColor = state.meta?.service_colors?.[shift.service_code];
    if (serviceColor) colorDot.style.background = serviceColor;
    const serviceName = document.createElement("strong");
    serviceName.textContent = shift.service;
    titleLine.appendChild(colorDot);
    titleLine.appendChild(serviceName);
    const codeLine = document.createElement("span");
    codeLine.textContent = shift.code;
    labelWrapper.appendChild(titleLine);
    labelWrapper.appendChild(codeLine);
    labelCell.appendChild(labelWrapper);
    row.appendChild(labelCell);
    for (let day = 1; day <= days; day += 1) {
      const cell = document.createElement("td");
      if (holidaySet.has(day)) cell.classList.add("holiday-cell");
      if (isWeekend(day)) cell.classList.add("weekend-cell");
      const input = document.createElement("input");
      input.type = "number";
      input.min = "0";
      input.value =
        requirementMap.get(`${shift.service_code}_${shift.code}_${day}`) || 0;
      input.dataset.service = shift.service_code;
      input.dataset.shift = shift.code;
      input.dataset.day = day;
      input.dataset.row = rowIdx;
      input.dataset.col = day;
      input.addEventListener("keydown", handleRequirementKeyNav);
      cell.appendChild(input);
      row.appendChild(cell);
    }
    table.appendChild(row);
  });
}

function handleRequirementKeyNav(event) {
  const input = event.target;
  const row = Number(input.dataset.row);
  const col = Number(input.dataset.col);
  let target;
  switch (event.key) {
    case "ArrowRight":
      target = document.querySelector(
        `#requirementsTable input[data-row='${row}'][data-col='${col + 1}']`
      );
      break;
    case "ArrowLeft":
      target = document.querySelector(
        `#requirementsTable input[data-row='${row}'][data-col='${col - 1}']`
      );
      break;
    case "ArrowDown":
      target = document.querySelector(
        `#requirementsTable input[data-row='${row + 1}'][data-col='${col}']`
      );
      break;
    case "ArrowUp":
      target = document.querySelector(
        `#requirementsTable input[data-row='${row - 1}'][data-col='${col}']`
      );
      break;
    default:
      return;
  }
  if (target) {
    event.preventDefault();
    target.focus();
  }
}

async function saveRequirements() {
  const inputs = document.querySelectorAll("#requirementsTable input");
  const items = [];
  inputs.forEach((input) => {
    const value = Number(input.value);
    if (value > 0) {
      items.push({
        day: Number(input.dataset.day),
        service_code: input.dataset.service,
        shift_code: input.dataset.shift,
        required_count: value,
      });
    }
  });
  await httpJson("/api/requirements/bulk", {
    method: "POST",
    body: JSON.stringify({
      year: state.year,
      month: state.month,
      items,
      group: state.group,
    }),
  });
  await loadRequirements();
  updateDashboard();
}

async function loadConstraints() {
  const url = `/api/constraints?year=${state.year}&month=${state.month}&${groupQuery()}`;
  state.constraints = await httpJson(url);
  renderConstraintsGrid();
}

function renderConstraintsGrid() {
  if (!state.meta) return;
  const table = document.getElementById("constraintsTable");
  const days = getDaysInMonth(state.year, state.month);
  const holidaySet = new Set(state.holidays.map((item) => item.day));
  table.innerHTML = "";
  const headerRow = document.createElement("tr");
  const firstTh = document.createElement("th");
  firstTh.textContent = t("label.professional", "Profissional");
  headerRow.appendChild(firstTh);
  for (let day = 1; day <= days; day += 1) {
    const th = document.createElement("th");
    if (holidaySet.has(day)) th.classList.add("holiday-cell");
    if (isWeekend(day)) th.classList.add("weekend-cell");
    th.appendChild(createDayHeader(day, holidaySet.has(day)));
    headerRow.appendChild(th);
  }
  table.appendChild(headerRow);

  const constraintMap = new Map(
    state.constraints.map((item) => [`${item.nurse_id}_${item.day}`, item.code])
  );

  getSortedNurses().forEach((nurse, rowIdx) => {
    const row = document.createElement("tr");
    const labelCell = document.createElement("td");
    labelCell.textContent = nurse.name;
    const actions = document.createElement("div");
    actions.className = "row-actions";
    const availableBtn = document.createElement("button");
    availableBtn.type = "button";
    availableBtn.textContent = t("label.available_short", "Tudo disp.");
    availableBtn.addEventListener("click", () =>
      setConstraintsRow(rowIdx, "DISPONIVEL")
    );
    const unavailableBtn = document.createElement("button");
    unavailableBtn.type = "button";
    unavailableBtn.className = "secondary";
    unavailableBtn.textContent = t("label.unavailable_short", "Tudo indisp.");
    unavailableBtn.addEventListener("click", () =>
      setConstraintsRow(rowIdx, "INDISPONIVEL")
    );
    actions.appendChild(availableBtn);
    actions.appendChild(unavailableBtn);
    labelCell.appendChild(actions);
    row.appendChild(labelCell);
    for (let day = 1; day <= days; day += 1) {
      const cell = document.createElement("td");
      if (holidaySet.has(day)) cell.classList.add("holiday-cell");
      const input = document.createElement("input");
      input.type = "text";
      input.className = "constraint-input";
      input.autocomplete = "off";
      input.spellcheck = false;
      input.maxLength = 6;
      input.setAttribute("list", "constraintCodesList");
      const code = constraintMap.get(`${nurse.id}_${day}`) || "";
      input.value = constraintCodeToInput(code);
      input.dataset.code = code;
      input.dataset.nurse = nurse.id;
      input.dataset.day = day;
      input.dataset.row = rowIdx;
      input.dataset.col = day;
      input.addEventListener("blur", () => normalizeConstraintInputEl(input));
      input.addEventListener("change", () => normalizeConstraintInputEl(input));
      input.addEventListener("keydown", (event) =>
        handleConstraintKeyNav(event, input)
      );
      cell.appendChild(input);
      row.appendChild(cell);
    }
    table.appendChild(row);
  });
}

function fillRequirementsGrid(value) {
  document
    .querySelectorAll("#requirementsTable input[type='number']")
    .forEach((input) => {
      input.value = value;
    });
}

function handleConstraintKeyNav(event, input) {
  const row = Number(input.dataset.row);
  const col = Number(input.dataset.col);
  const moveFocus = (targetRow, targetCol) => {
    const target = document.querySelector(
      `#constraintsTable input[data-row='${targetRow}'][data-col='${targetCol}']`
    );
    if (target) {
      target.focus();
      target.select();
    }
  };
  if (event.key === "Enter") {
    event.preventDefault();
    moveFocus(row + 1, col);
    return;
  }
  if (event.key === "ArrowUp") {
    event.preventDefault();
    moveFocus(row - 1, col);
    return;
  }
  if (event.key === "ArrowDown") {
    event.preventDefault();
    moveFocus(row + 1, col);
    return;
  }
  if (event.key === "ArrowLeft") {
    if (input.selectionStart === 0 && input.selectionEnd === 0) {
      event.preventDefault();
      moveFocus(row, col - 1);
    }
    return;
  }
  if (event.key === "ArrowRight") {
    if (
      input.selectionStart === input.value.length &&
      input.selectionEnd === input.value.length
    ) {
      event.preventDefault();
      moveFocus(row, col + 1);
    }
  }
}

function setConstraintsRow(row, code) {
  const inputs = document.querySelectorAll(
    `#constraintsTable input[data-row='${row}']`
  );
  inputs.forEach((input) => {
    input.value = constraintCodeToInput(code);
    input.dataset.code = code;
    input.classList.remove("invalid");
  });
}

async function saveConstraints() {
  const inputs = document.querySelectorAll("#constraintsTable input");
  const items = [];
  let hasInvalid = false;
  inputs.forEach((input) => {
    const code = normalizeConstraintInputEl(input);
    if (input.value.trim() && !code) {
      hasInvalid = true;
      return;
    }
    if (code) {
      items.push({
        nurse_id: Number(input.dataset.nurse),
        day: Number(input.dataset.day),
        code,
      });
    }
  });
  if (hasInvalid) {
    alert(
      t(
        "label.constraints_invalid",
        "Existem marcações inválidas (a vermelho). Corrige antes de guardar."
      )
    );
    return;
  }
  await httpJson("/api/constraints/bulk", {
    method: "POST",
    body: JSON.stringify({
      year: state.year,
      month: state.month,
      items,
    }),
  });
  await loadConstraints();
}

function parseAvailabilityInput(value) {
  const raw = value.trim();
  if (!raw) return "";
  const normalized = raw.toUpperCase();
  if (["LIVRE", "CLEAR", "REMOVER"].includes(normalized)) {
    return "__CLEAR__";
  }
  return parseConstraintText(raw);
}

async function loadMyAvailabilityRequests() {
  if (canEditSchedule()) return;
  const params = `year=${state.year}&month=${state.month}`;
  const status = document.getElementById("myAvailabilityStatus");
  try {
    state.myAvailabilityRequests = await httpJson(
      `/api/availability/requests?${params}`
    );
    state.myAvailabilityConstraints = await httpJson(
      `/api/availability/current?${params}`
    );
    if (status) status.textContent = "";
    renderMyConstraintsTable();
    renderMyAvailabilityList();
  } catch (error) {
    if (status) status.textContent = error.message;
  }
}

function renderMyConstraintsTable() {
  const table = document.getElementById("myConstraintsTable");
  if (!table) return;
  const days = getDaysInMonth(state.year, state.month);
  const holidaySet = new Set(state.holidays.map((item) => item.day));
  table.innerHTML = "";
  const headerRow = document.createElement("tr");
  const firstTh = document.createElement("th");
  firstTh.textContent = t("label.me", "Eu");
  headerRow.appendChild(firstTh);
  for (let day = 1; day <= days; day += 1) {
    const th = document.createElement("th");
    if (holidaySet.has(day)) th.classList.add("holiday-cell");
    if (isWeekend(day)) th.classList.add("weekend-cell");
    th.appendChild(createDayHeader(day, holidaySet.has(day)));
    headerRow.appendChild(th);
  }
  table.appendChild(headerRow);

  const constraintMap = new Map(
    state.myAvailabilityConstraints.map((item) => [`${item.day}`, item.code])
  );

  const row = document.createElement("tr");
  const labelCell = document.createElement("td");
  labelCell.textContent = t("label.availability", "Disponibilidade");
  row.appendChild(labelCell);
    for (let day = 1; day <= days; day += 1) {
      const cell = document.createElement("td");
      if (holidaySet.has(day)) cell.classList.add("holiday-cell");
      if (isWeekend(day)) cell.classList.add("weekend-cell");
      const input = document.createElement("input");
    input.type = "text";
    input.className = "constraint-input";
    input.autocomplete = "off";
    input.spellcheck = false;
    input.maxLength = 10;
    input.setAttribute("list", "constraintCodesList");
    input.value = constraintCodeToInput(constraintMap.get(`${day}`) || "");
    input.dataset.day = day;
    cell.appendChild(input);
    row.appendChild(cell);
  }
  table.appendChild(row);
}

function fillMyAvailability(code) {
  const inputs = document.querySelectorAll("#myConstraintsTable input");
  inputs.forEach((input) => {
    input.value = constraintCodeToInput(code);
  });
}

function renderMyAvailabilityList() {
  const container = document.getElementById("myAvailabilityList");
  if (!container) return;
  container.innerHTML = "";
  if (!state.myAvailabilityRequests.length) {
    container.textContent = t("availability.pending_none", "Sem pedidos pendentes.");
    return;
  }
  state.myAvailabilityRequests.forEach((req) => {
    const displayCode =
      req.code === "__CLEAR__" ? t("label.clear_code", "LIVRE") : req.code;
    const statusText =
      t(`availability.status.${req.status?.toLowerCase?.()}`, req.status) ||
      req.status;
    const item = document.createElement("div");
    item.className = "availability-item";
    item.innerHTML = `
      <strong>${t("label.day", "Dia")} ${req.day}</strong>
      <span>${t("label.state", "Estado")}: ${statusText}</span>
      <span>${t("label.code", "Código")}: ${displayCode}</span>
      ${
        req.reason
          ? `<small>${t("label.reason", "Motivo")}: ${req.reason}</small>`
          : ""
      }
    `;
    container.appendChild(item);
  });
}

async function submitAvailabilityRequest() {
  const status = document.getElementById("myAvailabilityStatus");
  const inputs = document.querySelectorAll("#myConstraintsTable input");
  const items = [];
  let hasInvalid = false;
  inputs.forEach((input) => {
    const raw = input.value.trim();
    if (!raw) return;
    const code = parseAvailabilityInput(raw);
    if (!code) {
      hasInvalid = true;
      input.classList.add("invalid");
      return;
    }
    input.classList.remove("invalid");
    items.push({ day: Number(input.dataset.day), code });
  });
  if (hasInvalid) {
    if (status) {
      status.textContent = t(
        "label.availability_invalid",
        "Existem códigos inválidos. Corrige antes de enviar."
      );
    }
    return;
  }
  if (status) status.textContent = t("label.availability_sending", "A enviar pedidos...");
  await httpJson("/api/availability/requests/bulk", {
    method: "POST",
    body: JSON.stringify({ year: state.year, month: state.month, items }),
  });
  if (status) status.textContent = t("label.availability_sent", "Pedido enviado para aprovação.");
  await loadMyAvailabilityRequests();
}

async function loadPendingAvailabilityRequests() {
  if (!canEditSchedule()) return;
  const params = `year=${state.year}&month=${state.month}&${groupQuery()}`;
  state.pendingAvailabilityRequests = await httpJson(
    `/api/availability/requests/pending?${params}`
  );
  renderPendingAvailabilityList();
}

function renderPendingAvailabilityList() {
  const container = document.getElementById("pendingAvailabilityList");
  if (!container) return;
  container.innerHTML = "";
  if (!state.pendingAvailabilityRequests.length) {
    container.textContent = t("availability.pending_none", "Sem pedidos pendentes.");
    return;
  }
  state.pendingAvailabilityRequests.forEach((req) => {
    const displayCode =
      req.code === "__CLEAR__" ? t("label.clear_code", "LIVRE") : req.code;
    const item = document.createElement("div");
    item.className = "availability-item";
    item.innerHTML = `
      <strong>${req.user_name}</strong>
      <span>${t("label.day", "Dia")} ${req.day} · ${t("label.code", "Código")} ${displayCode}</span>
    `;
    const actions = document.createElement("div");
    actions.className = "availability-actions";
    const approveBtn = document.createElement("button");
    approveBtn.textContent = t("btn.approve", "Aprovar");
    approveBtn.addEventListener("click", async () => {
      await httpJson(`/api/availability/requests/${req.id}/decision`, {
        method: "PUT",
        body: JSON.stringify({ status: "APPROVED" }),
      });
      await loadPendingAvailabilityRequests();
      await loadConstraints();
    });
    const rejectBtn = document.createElement("button");
    rejectBtn.textContent = t("btn.reject", "Rejeitar");
    rejectBtn.className = "secondary";
    rejectBtn.addEventListener("click", async () => {
      const reason =
        prompt(t("label.reject_reason", "Motivo da rejeição"), "") || "";
      await httpJson(`/api/availability/requests/${req.id}/decision`, {
        method: "PUT",
        body: JSON.stringify({ status: "REJECTED", reason }),
      });
      await loadPendingAvailabilityRequests();
    });
    actions.appendChild(approveBtn);
    actions.appendChild(rejectBtn);
    item.appendChild(actions);
    container.appendChild(item);
  });
}

async function loadMonthConfig() {
  const config = await httpJson(
    `/api/config/month?year=${state.year}&month=${state.month}`
  );
  state.config = config;
  renderRulesForm();
}

function renderRulesForm() {
  if (!state.config) return;
  document.getElementById("configMaxHoras").value =
    state.config.max_hours_week_contratado;
  document.getElementById("configTargetHoras").value =
    state.config.target_hours_week;
  document.getElementById("configRestHours").value =
    state.config.min_rest_hours ?? 11;
  document.getElementById("configPedidosHard").checked =
    state.config.pedidos_folga_hard;
  document.getElementById("configPreferFolgaND").checked =
    state.config.prefer_folga_after_nd;
  const container = document.getElementById("penaltiesContainer");
  container.innerHTML = "";
  const friendlyNames = {
    unfilled: t("penalty.unfilled", "Slot vazio"),
    pedido: t("penalty.pedido", "Pedido de folga violado"),
    hours_target: t("penalty.hours_target", "Desvio alvo horas"),
    night_sequence: t("penalty.night_sequence", "Noites consecutivas"),
    rest_followup: t("penalty.rest_followup", "Descanso pós-noite"),
  };
  Object.entries(state.config.penalty_weights).forEach(([key, value]) => {
    const wrapper = document.createElement("label");
    wrapper.textContent = friendlyNames[key] || `${t("label.penalties", "Penalizações")} ${key}`;
    const input = document.createElement("input");
    input.type = "number";
    input.value = value;
    input.min = "0";
    input.dataset.penalty = key;
    wrapper.appendChild(input);
    container.appendChild(wrapper);
  });
}

async function saveRulesConfig(event) {
  event.preventDefault();
  if (!state.config) return;
  const penalties = {};
  document
    .querySelectorAll("#penaltiesContainer input")
    .forEach((input) => {
      penalties[input.dataset.penalty] = Number(input.value);
    });
  await httpJson("/api/config/month", {
    method: "PUT",
    body: JSON.stringify({
      year: state.year,
      month: state.month,
      max_hours_week_contratado: Number(
        document.getElementById("configMaxHoras").value
      ),
      target_hours_week: Number(
        document.getElementById("configTargetHoras").value
      ),
      min_rest_hours: Number(document.getElementById("configRestHours").value),
      pedidos_folga_hard: document.getElementById("configPedidosHard").checked,
      prefer_folga_after_nd: document.getElementById("configPreferFolgaND").checked,
      penalty_weights: penalties,
    }),
  });
  await loadMonthConfig();
}

async function loadHolidays() {
  state.holidays = await httpJson(
    `/api/holidays?year=${state.year}&month=${state.month}`
  );
  renderHolidayList();
  renderRequirementsGrid();
  renderConstraintsGrid();
  renderScheduleTable();
}

function renderHolidayList() {
  const list = document.getElementById("holidayList");
  list.innerHTML = "";
  state.holidays.forEach((holiday) => {
    const item = document.createElement("li");
    item.textContent = `${t("label.day", "Dia")} ${holiday.day}: ${holiday.label} (${holiday.type})`;
    if (holiday.type === "NACIONAL") {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.textContent = t("label.remove_holiday", "Remover este feriado");
      btn.addEventListener("click", () => createHolidayRemoval(holiday.day));
      item.appendChild(btn);
    }
    list.appendChild(item);
  });
}

async function loadManualHolidays() {
  state.manualHolidays = await httpJson("/api/holidays/manual");
  renderManualHolidayList();
}

async function loadAdjustments() {
  state.adjustments = await httpJson(
    `/api/adjustments?year=${state.year}&month=${state.month}&${groupQuery()}`
  );
  renderAdjustmentsTable();
  renderScheduleStats();
}

function renderManualHolidayList() {
  const list = document.getElementById("manualHolidayList");
  list.innerHTML = "";
  if (!state.manualHolidays.length) {
    const empty = document.createElement("li");
    empty.className = "hint";
    empty.textContent = t("holidays.none", "Sem feriados manuais.");
    list.appendChild(empty);
    return;
  }
  const sorted = [...state.manualHolidays].sort((a, b) => {
    if (a.year !== b.year) return a.year - b.year;
    if (a.month !== b.month) return a.month - b.month;
    return a.day - b.day;
  });
  sorted.forEach((holiday) => {
    const li = document.createElement("li");
    const monthLabel = monthNames[holiday.month - 1] || holiday.month;
    const prefix =
      holiday.year === state.year && holiday.month === state.month
        ? ` ${t("label.manual_current", "(mês ativo)")}`
        : "";
    const actionLabel =
      holiday.action === "REMOVE"
        ? t("label.manual_remove", "[Remoção]")
        : t("label.manual_add", "[Manual]");
    li.textContent = `${actionLabel} ${t("label.day", "Dia")} ${
      holiday.day
    } ${t("label.of", "de")} ${monthLabel}/${holiday.year}: ${holiday.label}${prefix}`;
    if (holiday.year === state.year && holiday.month === state.month) {
      li.classList.add("manual-holiday-current");
    }
    const btn = document.createElement("button");
    btn.type = "button";
    btn.textContent = t("label.remove", "Remover");
    btn.addEventListener("click", () => deleteManualHoliday(holiday.id));
    li.appendChild(btn);
    list.appendChild(li);
  });
}

async function handleManualHolidaySubmit(event) {
  event.preventDefault();
  const day = Number(document.getElementById("manualHolidayDay").value);
  const action = document.getElementById("manualHolidayAction").value;
  const labelInput = document.getElementById("manualHolidayLabel");
  const label = labelInput.value.trim();
  if (!day) return;
  if (action === "ADD" && !label) return;
  await httpJson("/api/holidays/manual", {
    method: "POST",
    body: JSON.stringify({
      year: state.year,
      month: state.month,
      day,
      label: label || "",
      action,
    }),
  });
  event.target.reset();
  updateManualHolidayLabelState();
  await loadManualHolidays();
  await loadHolidays();
}

async function deleteManualHoliday(id) {
  await httpJson(`/api/holidays/manual/${id}`, { method: "DELETE" });
  await loadManualHolidays();
  await loadHolidays();
}

async function createHolidayRemoval(day) {
  await httpJson("/api/holidays/manual", {
    method: "POST",
    body: JSON.stringify({
      year: state.year,
      month: state.month,
      day,
      action: "REMOVE",
      label: t("action.remove_national_holiday", "Remover feriado nacional"),
    }),
  });
  await loadManualHolidays();
  await loadHolidays();
}

function renderAdjustmentsTable() {
  const table = document.getElementById("adjustmentsTable");
  if (!table) return;
  table.innerHTML = "";
  if (!state.nurses.length) return;
  const thead = document.createElement("thead");
  thead.innerHTML = `
    <tr>
      <th>${t("label.professional", "Profissional")}</th>
      <th>${t("label.worked_holidays", "Feriados trabalhados")}</th>
      <th>${t("label.extra_hours", "Horas extra (+)")}</th>
      <th>${t("label.reduced_hours", "Redução horas (-)")}</th>
    </tr>
  `;
  table.appendChild(thead);
  const tbody = document.createElement("tbody");
  const adjustmentMap = new Map(
    state.adjustments.map((item) => [item.nurse_id, item])
  );
  getSortedNurses().forEach((nurse) => {
    const adjustment = adjustmentMap.get(nurse.id) || {};
    const row = document.createElement("tr");
    row.dataset.nurse = nurse.id;
    const ferInput = document.createElement("input");
    ferInput.type = "number";
    ferInput.min = "0";
    ferInput.step = "1";
    ferInput.value = adjustment.feriados_trabalhados ?? 0;
    ferInput.dataset.field = "feriados";
    const extraInput = document.createElement("input");
    extraInput.type = "number";
    extraInput.step = "0.25";
    extraInput.min = "0";
    extraInput.value = minutesToHoursText(adjustment.extra_minutes || 0);
    extraInput.dataset.field = "extra";
    const reducedInput = document.createElement("input");
    reducedInput.type = "number";
    reducedInput.step = "0.25";
    reducedInput.min = "0";
    reducedInput.value = minutesToHoursText(adjustment.reduced_minutes || 0);
    reducedInput.dataset.field = "reduced";
    const nameCell = document.createElement("td");
    nameCell.textContent = nurse.name;
    const ferCell = document.createElement("td");
    ferCell.appendChild(ferInput);
    const extraCell = document.createElement("td");
    extraCell.appendChild(extraInput);
    const reducedCell = document.createElement("td");
    reducedCell.appendChild(reducedInput);
    row.appendChild(nameCell);
    row.appendChild(ferCell);
    row.appendChild(extraCell);
    row.appendChild(reducedCell);
    tbody.appendChild(row);
  });
  table.appendChild(tbody);
}

function renderShiftSettings() {
  const table = document.getElementById("shiftSettingsTable");
  if (!table || !state.meta) return;
  table.innerHTML = "";
  if (!state.meta.service_shifts.length) return;
  const header = document.createElement("tr");
  header.innerHTML = `
    <th>${t("label.service", "Serviço")}</th>
    <th>${t("label.code", "Código")}</th>
    <th>${t("label.start", "Início")}</th>
    <th>${t("label.end", "Fim")}</th>
    <th>${t("label.duration", "Duração")}</th>
    <th></th>
  `;
  table.appendChild(header);
  const typeOrder = { M: 0, T: 1, L: 2, N: 3 };
  const role = currentGroupRole();
  const shifts = state.meta.service_shifts
    .filter((shift) => !shift.service_role || shift.service_role === role)
    .sort((a, b) => {
    if (a.service !== b.service) return a.service.localeCompare(b.service);
    const diff =
      (typeOrder[a.shift_type] ?? 10) - (typeOrder[b.shift_type] ?? 10);
    if (diff !== 0) return diff;
    return a.code.localeCompare(b.code);
  });
  shifts.forEach((shift) => {
    const row = document.createElement("tr");
    row.innerHTML = `<td>${shift.service}</td><td>${shift.code}</td>`;
    const startCell = document.createElement("td");
    const startInput = document.createElement("input");
    startInput.type = "time";
    startInput.value = minutesToTime(shift.start_minute);
    startInput.required = true;
    startCell.appendChild(startInput);
    row.appendChild(startCell);
    const endCell = document.createElement("td");
    const endInput = document.createElement("input");
    endInput.type = "time";
    endInput.value = minutesToTime(shift.end_minute);
    endInput.required = true;
    endCell.appendChild(endInput);
    row.appendChild(endCell);
    const durationCell = document.createElement("td");
    durationCell.textContent = formatDuration(shift.minutes);
    row.appendChild(durationCell);
    const actionCell = document.createElement("td");
    const saveBtn = document.createElement("button");
    saveBtn.type = "button";
    saveBtn.textContent = t("btn.save", "Guardar");
    saveBtn.addEventListener("click", () => {
      if (!startInput.value || !endInput.value) {
        alert(t("label.invalid_time", "Indica horas válidas (HH:MM)."));
        return;
      }
      saveShiftSetting(shift.code, startInput.value, endInput.value);
    });
    actionCell.appendChild(saveBtn);
    row.appendChild(actionCell);
    table.appendChild(row);
  });
}

async function saveShiftSetting(code, startTime, endTime) {
  await httpJson(`/api/shifts/${code}`, {
    method: "PUT",
    body: JSON.stringify({
      start_time: startTime,
      end_time: endTime,
    }),
  });
  await loadMeta();
  renderRequirementsGrid();
  renderConstraintsGrid();
  renderScheduleTable();
  renderScheduleStats();
}

async function saveAdjustments(event) {
  event.preventDefault();
  const rows = document.querySelectorAll("#adjustmentsTable tbody tr");
  const items = [];
  rows.forEach((row) => {
    const nurseId = Number(row.dataset.nurse);
    const fer = Number(
      row.querySelector("input[data-field='feriados']").value || 0
    );
    const extraHours = Number(
      row.querySelector("input[data-field='extra']").value || 0
    );
    const reducedHours = Number(
      row.querySelector("input[data-field='reduced']").value || 0
    );
    if (fer || extraHours || reducedHours) {
      items.push({
        nurse_id: nurseId,
        feriados_trabalhados: fer,
        extra_minutes: Math.round(extraHours * 60),
        reduced_minutes: Math.round(reducedHours * 60),
      });
    }
  });
  await httpJson("/api/adjustments/bulk", {
    method: "POST",
    body: JSON.stringify({
      year: state.year,
      month: state.month,
      items,
    }),
  });
  await loadAdjustments();
}

async function handleClearSchedule(event) {
  event.preventDefault();
  if (!canEditSchedule()) return;
  const month = Number(document.getElementById("clearScheduleMonth").value);
  const year = Number(document.getElementById("clearScheduleYear").value);
  if (!Number.isFinite(month) || !Number.isFinite(year)) return;
  const message = `${t("confirm.clear_schedule", "Apagar horário de")} ${monthNames[month - 1]} ${year}?`;
  if (!window.confirm(message)) return;
  await httpJson(`/api/schedule?year=${year}&month=${month}&${groupQuery()}`, {
    method: "DELETE",
  });
  if (year === state.year && month === state.month) {
    await loadSchedule();
    await loadAdjustments();
  }
}

async function loadSchedule() {
  const url = `/api/schedule?year=${state.year}&month=${state.month}&${groupQuery()}`;
  const result = await httpJson(url);
  state.scheduleEntries = result.entries;
  state.unfilled = result.unfilled || [];
  state.violations = result.violations || [];
  state.scheduleStats = result.stats || [];
  renderScheduleTable();
  renderUnfilledList();
  renderViolationsList();
  updateDashboard();
}

function renderScheduleTable() {
  if (!state.nurses.length) return;
  const table = document.getElementById("scheduleTable");
  const days = getDaysInMonth(state.year, state.month);
  const holidaySet = new Set(state.holidays.map((item) => item.day));
  const editable = canEditSchedule();
  table.innerHTML = "";
  const headerRow = document.createElement("tr");
  const titleTh = document.createElement("th");
  titleTh.textContent = t("label.professional", "Profissional");
  headerRow.appendChild(titleTh);
  const debitTh = document.createElement("th");
  debitTh.textContent = t("label.previous_debit", "Débito anterior");
  headerRow.appendChild(debitTh);
  for (let day = 1; day <= days; day += 1) {
    const th = document.createElement("th");
    if (holidaySet.has(day)) th.classList.add("holiday-cell");
    th.appendChild(createDayHeader(day, holidaySet.has(day)));
    headerRow.appendChild(th);
  }
  [
    t("label.total_hours", "Total Horas"),
    t("label.balance_current", "Saldo atual"),
    t("label.monthly_hours", "Horas Mensais"),
  ].forEach((label) => {
    const th = document.createElement("th");
    th.textContent = label;
    headerRow.appendChild(th);
  });
  table.appendChild(headerRow);

  const assignmentMap = new Map();
  state.scheduleEntries.forEach((entry) => {
    const key = `${entry.nurse_id}_${entry.day}`;
    if (!assignmentMap.has(key)) {
      assignmentMap.set(key, []);
    }
    assignmentMap.get(key).push(entry);
  });
  const statsMap = new Map(state.scheduleStats.map((item) => [item.nurse_id, item]));

  getSortedNurses().forEach((nurse) => {
    const row = document.createElement("tr");
    const labelCell = document.createElement("td");
    const labelWrapper = document.createElement("div");
    labelWrapper.className = "schedule-name-cell";
    const nameSpan = document.createElement("span");
    nameSpan.textContent = nurse.name;
    labelWrapper.appendChild(nameSpan);
    if (editable) {
      const controls = document.createElement("div");
      controls.className = "reorder-controls";
      const upBtn = document.createElement("button");
      upBtn.type = "button";
      upBtn.className = "reorder-btn";
      upBtn.textContent = "▲";
      upBtn.title = t("action.move_up", "Subir");
      upBtn.addEventListener("click", (event) => {
        event.stopPropagation();
        moveNurseRow(nurse.id, "up");
      });
      const downBtn = document.createElement("button");
      downBtn.type = "button";
      downBtn.className = "reorder-btn";
      downBtn.textContent = "▼";
      downBtn.title = t("action.move_down", "Descer");
      downBtn.addEventListener("click", (event) => {
        event.stopPropagation();
        moveNurseRow(nurse.id, "down");
      });
      controls.appendChild(upBtn);
      controls.appendChild(downBtn);
      labelWrapper.appendChild(controls);
    }
    labelCell.appendChild(labelWrapper);
    row.appendChild(labelCell);

    const stat = statsMap.get(nurse.id);
    const debitCell = document.createElement("td");
    const previousMinutes =
      stat && typeof stat.previous_bank_minutes === "number"
        ? stat.previous_bank_minutes
        : nurse.hour_balance_minutes || 0;
    if (editable) {
      const debitInput = document.createElement("input");
      debitInput.type = "number";
      debitInput.step = "0.25";
      debitInput.className = "constraint-input";
      debitInput.value = minutesToHoursValue(previousMinutes);
      debitInput.addEventListener("change", () =>
        handleDebitChange(nurse, stat, debitInput)
      );
      debitCell.appendChild(debitInput);
    } else {
      debitCell.textContent = minutesToHoursValue(previousMinutes);
    }
    row.appendChild(debitCell);

    for (let day = 1; day <= days; day += 1) {
      const cell = document.createElement("td");
      cell.dataset.nurse = nurse.id;
      cell.dataset.day = day;
      if (editable) cell.tabIndex = 0;
      if (holidaySet.has(day)) cell.classList.add("holiday-cell");
      if (isWeekend(day)) cell.classList.add("weekend-cell");
      const entries = assignmentMap.get(`${nurse.id}_${day}`) || [];
      if (entries.length) {
        const sortedCodes = entries
          .map((item) => item.shift_code)
          .sort((a, b) => {
            const aMeta = getShiftMeta(a);
            const bMeta = getShiftMeta(b);
            const aStart = aMeta?.start_minute ?? 9999;
            const bStart = bMeta?.start_minute ?? 9999;
            if (aStart !== bStart) return aStart - bStart;
            return a.localeCompare(b);
          });
        cell.textContent = sortedCodes.join("");
        if (entries.some((item) => item.locked)) cell.classList.add("cell-locked");
        cell.dataset.entry = JSON.stringify(entries[0]);
        cell.dataset.codes = JSON.stringify(sortedCodes);
        if (sortedCodes.length === 1) {
          const shiftMeta = getShiftMeta(sortedCodes[0]);
          if (shiftMeta) {
            const color = state.meta?.service_colors?.[shiftMeta.service];
            if (color) {
              cell.style.backgroundColor = color;
              cell.style.backgroundImage = "";
              cell.classList.add("service-colored");
            } else {
              cell.style.backgroundColor = "";
              cell.style.backgroundImage = "";
              cell.classList.remove("service-colored");
            }
            const start = minutesToTime(shiftMeta.start_minute);
            const end = minutesToTime(shiftMeta.end_minute);
            cell.title = `${shiftMeta.service} • ${shiftMeta.label} (${start}–${end})`;
          } else {
            cell.style.backgroundColor = "";
            cell.style.backgroundImage = "";
            cell.classList.remove("service-colored");
            cell.removeAttribute("title");
          }
        } else {
          const colors = sortedCodes
            .map((code) => {
              const meta = getShiftMeta(code);
              if (!meta) return null;
              return state.meta?.service_colors?.[meta.service] || null;
            })
            .filter(Boolean);
          if (colors.length >= 2) {
          if (colors.length >= 3) {
            cell.style.backgroundImage = `linear-gradient(90deg, ${colors[0]} 0%, ${colors[0]} 33.33%, ${colors[1]} 33.33%, ${colors[1]} 66.66%, ${colors[2]} 66.66%, ${colors[2]} 100%)`;
          } else {
            cell.style.backgroundImage = `linear-gradient(90deg, ${colors[0]} 0%, ${colors[0]} 50%, ${colors[1]} 50%, ${colors[1]} 100%)`;
          }
            cell.style.backgroundColor = "";
          } else {
            cell.style.backgroundImage = "";
            cell.style.backgroundColor = "";
          }
          cell.classList.remove("service-colored");
          const tooltip = sortedCodes
            .map((code) => {
              const meta = getShiftMeta(code);
              if (!meta) return code;
              const start = minutesToTime(meta.start_minute);
              const end = minutesToTime(meta.end_minute);
              return `${meta.service} • ${meta.label} (${start}–${end})`;
            })
            .join(" | ");
          cell.title = tooltip;
        }
      } else {
        cell.textContent = "";
        cell.dataset.entry = "";
        cell.dataset.codes = "";
        cell.style.backgroundColor = "";
        cell.style.backgroundImage = "";
        cell.classList.remove("service-colored");
        cell.removeAttribute("title");
      }
      row.appendChild(cell);
    }
    const totalCell = document.createElement("td");
    totalCell.textContent = formatHours(stat?.actual_minutes || 0);
    row.appendChild(totalCell);

    const saldoCell = document.createElement("td");
    const baseBank =
      stat && typeof stat.previous_bank_minutes === "number"
        ? stat.previous_bank_minutes
        : nurse.hour_balance_minutes || 0;
    const saldoMinutes =
      (stat?.actual_minutes || 0) + baseBank - (stat?.target_minutes || 0);
    saldoCell.textContent = formatHours(saldoMinutes);
    row.appendChild(saldoCell);

    const targetCell = document.createElement("td");
    if (editable) {
      const targetInput = document.createElement("input");
      targetInput.type = "number";
      targetInput.step = "0.25";
      targetInput.className = "constraint-input";
      targetInput.value = minutesToHoursValue(stat?.target_minutes || 0);
      targetInput.addEventListener("change", () =>
        handleTargetHoursChange(nurse, stat, targetInput)
      );
      targetCell.appendChild(targetInput);
    } else {
      targetCell.textContent = minutesToHoursValue(stat?.target_minutes || 0);
    }
    row.appendChild(targetCell);

    table.appendChild(row);
  });

  table.removeEventListener("click", handleScheduleClick);
  table.removeEventListener("keydown", handleScheduleKeydown);
  if (editable) {
    table.addEventListener("click", handleScheduleClick);
    table.addEventListener("keydown", handleScheduleKeydown);
  }

  renderScheduleStats();
}

async function handleDebitChange(nurse, stat, input) {
  if (!canEditSchedule()) return;
  const value = Number(input.value);
  if (Number.isNaN(value)) return;
  const deltaMinutes = stat ? stat.delta_minutes : 0;
  const newBankMinutes = hoursToMinutes(value) + deltaMinutes;
  await httpJson(`/api/nurses/${nurse.id}`, {
    method: "PUT",
    body: JSON.stringify({ hour_balance_minutes: newBankMinutes }),
  });
  await loadNurses();
  await loadSchedule();
}

async function handleTargetHoursChange(nurse, stat, input) {
  if (!canEditSchedule()) return;
  const value = Number(input.value);
  if (Number.isNaN(value)) return;
  const minutes = hoursToMinutes(value);
  await httpJson("/api/schedule/stat", {
    method: "PUT",
    body: JSON.stringify({
      nurse_id: nurse.id,
      year: state.year,
      month: state.month,
      target_minutes: minutes,
    }),
  });
  await loadNurses();
  await loadSchedule();
}

async function moveNurseRow(nurseId, direction) {
  if (!canEditSchedule()) return;
  await httpJson(`/api/nurses/${nurseId}/move`, {
    method: "POST",
    body: JSON.stringify({ direction }),
  });
  await loadNurses();
  await loadSchedule();
  await loadConstraints();
}

function renderScheduleStats() {
  const table = document.getElementById("scheduleStatsTable");
  if (!table) return;
  table.innerHTML = "";
  if (!state.nurses.length) return;
  const header = document.createElement("tr");
  header.innerHTML = `
    <th>${t("label.professional", "Profissional")}</th>
    <th>${t("label.assigned_hours", "Horas atribuídas")}</th>
    <th>${t("label.target_hours", "Horas alvo")}</th>
    <th>${t("label.delta_month", "Delta (mês)")}</th>
    <th>${t("label.bank_previous", "Banco anterior")}</th>
    <th>${t("label.bank_current", "Banco atual")}</th>
    <th>${t("label.mornings", "Manhãs")}</th>
    <th>${t("label.afternoons", "Tardes")}</th>
    <th>${t("label.nights", "Noites")}</th>
    <th>${t("label.days_off", "Folgas")}</th>
    <th>${t("label.rests", "Descansos")}</th>
    <th>${t("label.vacations", "Férias")}</th>
  `;
  table.appendChild(header);
  const statsMap = new Map(state.scheduleStats.map((item) => [item.nurse_id, item]));
  const entriesByNurse = new Map();
  state.scheduleEntries.forEach((entry) => {
    const list = entriesByNurse.get(entry.nurse_id) || [];
    list.push(entry);
    entriesByNurse.set(entry.nurse_id, list);
  });
  const constraintsByNurse = new Map();
  state.constraints.forEach((entry) => {
    const list = constraintsByNurse.get(entry.nurse_id) || [];
    list.push(entry);
    constraintsByNurse.set(entry.nurse_id, list);
  });
  const folgaCodes = new Set([
    "PEDIDO_FOLGA",
    "DISPENSA",
    "PEDIDO_DESCANSO_FOLGA",
  ]);
  const descansoCodes = new Set(["PEDIDO_DESCANSO"]);
  getSortedNurses().forEach((nurse) => {
    const stat = statsMap.get(nurse.id);
    const actual = stat ? formatHours(stat.actual_minutes) : "0";
    const target = stat ? formatHours(stat.target_minutes) : "0";
    const delta = stat ? formatHours(stat.delta_minutes) : "0";
    const prevBank = stat ? formatHours(stat.previous_bank_minutes) : formatHours(0);
    const currentBank = stat ? formatHours(stat.bank_minutes) : formatHours(nurse.hour_balance_minutes || 0);
    let mornings = 0;
    let afternoons = 0;
    let nights = 0;
    let folgas = 0;
    let descansos = 0;
    let ferias = 0;
    (entriesByNurse.get(nurse.id) || []).forEach((entry) => {
      if (entry.service_code === "REST" && entry.shift_code === "D") {
        descansos += 1;
        return;
      }
      const meta = getShiftMeta(entry.shift_code);
      if (!meta?.shift_type) return;
      if (meta.shift_type === "M") mornings += 1;
      if (meta.shift_type === "T") afternoons += 1;
      if (meta.shift_type === "N") nights += 1;
    });
    (constraintsByNurse.get(nurse.id) || []).forEach((entry) => {
      if (entry.code === "FERIAS") {
        ferias += 1;
      } else if (folgaCodes.has(entry.code)) {
        folgas += 1;
      } else if (descansoCodes.has(entry.code)) {
        descansos += 1;
      }
    });
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${nurse.name}</td>
      <td>${actual}</td>
      <td>${target}</td>
      <td>${delta}</td>
      <td>${prevBank}</td>
      <td>${currentBank}</td>
      <td>${mornings}</td>
      <td>${afternoons}</td>
      <td>${nights}</td>
      <td>${folgas}</td>
      <td>${descansos}</td>
      <td>${ferias}</td>
    `;
    table.appendChild(row);
  });
}

function handleScheduleClick(event) {
  if (!canEditSchedule()) return;
  const cell = event.target.closest("td");
  if (!cell || !cell.dataset.nurse) return;
  openCellEditor(cell);
}

function handleScheduleKeydown(event) {
  if (!canEditSchedule()) return;
  const cell = event.target.closest("td");
  if (!cell || !cell.dataset.nurse) return;
  const nurseId = Number(cell.dataset.nurse);
  const day = Number(cell.dataset.day);
  const entry = cell.dataset.entry ? JSON.parse(cell.dataset.entry) : null;
  switch (event.key) {
    case "Enter":
      openCellEditor(cell);
      event.preventDefault();
      break;
    case "Delete":
      updateScheduleCell({
        nurse_id: nurseId,
        day,
        shift_code: null,
        locked: null,
      });
      event.preventDefault();
      break;
    case "l":
    case "L":
      if (entry) {
        updateScheduleCell({
          nurse_id: nurseId,
          day,
          shift_code: null,
          locked: !entry.locked,
        });
      }
      event.preventDefault();
      break;
    case "ArrowRight":
      moveScheduleFocus(cell, 1, 0);
      event.preventDefault();
      break;
    case "ArrowLeft":
      moveScheduleFocus(cell, -1, 0);
      event.preventDefault();
      break;
    case "ArrowDown":
      moveScheduleFocus(cell, 0, 1);
      event.preventDefault();
      break;
    case "ArrowUp":
      moveScheduleFocus(cell, 0, -1);
      event.preventDefault();
      break;
    default:
      break;
  }
}

function moveScheduleFocus(cell, colDelta, rowDelta) {
  const row = cell.parentElement;
  const table = document.getElementById("scheduleTable");
  const rowIndex = row.rowIndex;
  const cellIndex = cell.cellIndex;
  const targetRow = table.rows[rowIndex + rowDelta];
  if (!targetRow) return;
  const targetCell = targetRow.cells[cellIndex + colDelta];
  if (targetCell && targetCell.dataset.nurse) {
    targetCell.focus();
  }
}

function renderUnfilledList() {
  const list = document.getElementById("unfilledList");
  list.innerHTML = "";
  state.unfilled.forEach((slot) => {
    const item = document.createElement("li");
    const reason = translateSolverReason(slot.reason);
    item.textContent = `${t("label.day", "Dia")} ${slot.day} - ${slot.service_code}/${slot.shift_code}: ${reason}`;
    list.appendChild(item);
  });
}

function renderViolationsList() {
  const list = document.getElementById("violationsList");
  list.innerHTML = "";
  state.violations.forEach((violation) => {
    const item = document.createElement("li");
    item.textContent = translateSolverViolation(violation);
    list.appendChild(item);
  });
}

async function generate() {
  if (!canEditSchedule()) return;
  const status = document.getElementById("generationStatus");
  status.textContent = t("label.schedule_generating", "A gerar...");
  try {
    const result = await httpJson(`/api/schedule/generate?${groupQuery()}`, {
      method: "POST",
      body: JSON.stringify({
        year: state.year,
        month: state.month,
      }),
    });
    state.scheduleEntries = result.entries;
    state.unfilled = result.unfilled || [];
    state.violations = result.violations || [];
    state.scheduleStats = result.stats || [];
    renderScheduleTable();
    renderUnfilledList();
    renderViolationsList();
    await loadNurses();
    updateDashboard();
    status.textContent = t("label.schedule_updated", "Horário atualizado.");
  } catch (error) {
    status.textContent = error.message;
  }
}

async function refreshMonthData() {
  updateCurrentPeriodLabel();
  const tasks = [loadSchedule(), loadHolidays()];
  if (canEditSchedule()) {
    tasks.push(
      loadRequirements(),
      loadConstraints(),
      loadMonthConfig(),
      loadManualHolidays(),
      loadAdjustments(),
      loadReleases(),
      loadPendingAvailabilityRequests()
    );
  } else {
    tasks.push(loadMyAvailabilityRequests());
  }
  await Promise.all(tasks);
  updateDashboard();
}

function updateDashboard() {
  const totalNeeds = state.requirements.reduce(
    (sum, item) => sum + item.required_count,
    0
  );
  const assigned = state.scheduleEntries.filter(
    (entry) => entry.service_code !== "REST"
  ).length;
  const locked = state.scheduleEntries.filter((entry) => entry.locked).length;
  document.getElementById("statNeeds").textContent = totalNeeds;
  document.getElementById("statAssigned").textContent = assigned;
  document.getElementById("statLocks").textContent = locked;
  document.getElementById("statViolations").textContent =
    (state.violations?.length || 0) + (state.unfilled?.length || 0);
}

function updateCurrentPeriodLabel() {
  const label = document.getElementById("currentPeriodLabel");
  if (!label) return;
  const monthName = monthNames[state.month - 1] || "";
  label.textContent = `${t("label.active_month", "Mês ativo")}: ${monthName} ${state.year} · ${groupLabel()}`;
  updateSectionPeriodLabels();
  syncClearScheduleSelectors();
}

function updateSectionPeriodLabels() {
  const monthName = monthNames[state.month - 1] || "";
  document.querySelectorAll("[data-section-period]").forEach((el) => {
    el.textContent = `${monthName} ${state.year} · ${groupLabel()}`;
  });
}

function formatHours(minutes) {
  if (!minutes) return "0";
  return (minutes / 60).toFixed(1);
}

function chooseExportFormat() {
  return new Promise((resolve) => {
    const overlay = document.createElement("div");
    overlay.className = "export-modal";
    overlay.innerHTML = `
      <div class="export-modal-card">
        <h3>${t("label.export_title", "Exportar")}</h3>
        <div class="export-modal-actions">
          <button type="button" data-format="xlsx">Excel</button>
          <button type="button" data-format="pdf" class="secondary">PDF</button>
        </div>
        <button type="button" class="ghost export-cancel">${t("label.export_cancel", "Cancelar")}</button>
      </div>
    `;
    const cleanup = (value) => {
      overlay.remove();
      resolve(value);
    };
    overlay.addEventListener("click", (event) => {
      if (event.target === overlay) cleanup(null);
    });
    overlay
      .querySelector(".export-cancel")
      .addEventListener("click", () => cleanup(null));
    overlay.querySelectorAll("[data-format]").forEach((button) => {
      button.addEventListener("click", () => cleanup(button.dataset.format));
    });
    document.body.appendChild(overlay);
  });
}

function filenameFromDisposition(disposition) {
  if (!disposition) return null;
  const match = disposition.match(/filename\*?=(?:UTF-8''|\"?)([^\";]+)/i);
  if (!match) return null;
  try {
    return decodeURIComponent(match[1]);
  } catch {
    return match[1];
  }
}

async function downloadFile(url, format, kind, fallbackName) {
  const response = await apiFetch(url);
  if (!response.ok) {
    alert(t("label.export_failed", "Exportação falhou"));
    return;
  }
  const blob = await response.blob();
  const link = document.createElement("a");
  const downloadUrl = window.URL.createObjectURL(blob);
  link.href = downloadUrl;
  const disposition = response.headers.get("content-disposition");
  const defaultName =
    kind === "schedule"
      ? `horario_${state.year}_${state.month}.${format}`
      : kind === "constraints"
        ? `disponibilidades_${state.year}_${state.month}.${format}`
        : kind === "swap-proof"
          ? `troca_${state.year}_${state.month}.${format}`
          : `trocas.${format}`;
  link.download = filenameFromDisposition(disposition) || fallbackName || defaultName;
  document.body.appendChild(link);
  link.click();
  link.remove();
  window.URL.revokeObjectURL(downloadUrl);
}
