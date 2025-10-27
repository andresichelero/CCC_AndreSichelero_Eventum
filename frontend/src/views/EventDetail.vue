<template>
  <div class="event-detail-section">
    <v-container>
      <v-card class="main-card elevation-4 mb-6" color="rgba(255,255,255,0.95)">
        <v-card-title class="text-h4 primary--text">
          <v-icon class="me-2">mdi-calendar-star</v-icon>
          {{ event.title }}
        </v-card-title>
        <v-card-subtitle class="secondary--text">
          <v-icon small class="me-1">mdi-account</v-icon>
          Organizado por: {{ event.organizer?.name }}
        </v-card-subtitle>
        <v-card-text>
          <v-row>
            <v-col cols="12" md="8">
              <h4 class="mb-3">
                <v-icon class="me-2">mdi-text</v-icon>
                Descrição
              </h4>
              <div v-html="event.description" class="event-description"></div>
              <v-divider class="my-4"></v-divider>
              <div class="periods-info mb-4">
                <v-row>
                  <v-col cols="12" md="6">
                    <v-icon small class="me-1">mdi-calendar-range</v-icon>
                    <strong>Período de Inscrição:</strong><br />
                    {{ formatDateTime(event.inscription_start_date) }} a
                    {{ formatDateTime(event.inscription_end_date) }}
                  </v-col>
                  <v-col v-if="event.submission_start_date" cols="12" md="6">
                    <v-icon small class="me-1">mdi-file-document</v-icon>
                    <strong>Período de Submissão:</strong><br />
                    {{ formatDateTime(event.submission_start_date) }} a
                    {{ formatDateTime(event.submission_end_date) }}
                  </v-col>
                </v-row>
              </div>
              <v-divider class="my-4"></v-divider>
              <div class="date-info">
                <p class="mb-2">
                  <v-icon small class="me-1">mdi-calendar-start</v-icon>
                  <strong>Início:</strong> {{ formatDateTime(event.start_date) }}
                </p>
                <p>
                  <v-icon small class="me-1">mdi-calendar-end</v-icon>
                  <strong>Fim:</strong> {{ formatDateTime(event.end_date) }}
                </p>
              </div>
            </v-col>
            <v-col cols="12" md="4">
              <!-- Organizer Actions -->
              <v-card
                v-if="user && event.organizer_id === user.id"
                class="action-card elevation-3 mb-4"
              >
                <v-card-title class="primary--text">
                  <v-icon class="me-2">mdi-cog</v-icon>
                  Ações do Organizador
                </v-card-title>
                <v-card-text>
                  <v-btn
                    :to="`/events/${event.id}/edit`"
                    color="primary"
                    variant="elevated"
                    prepend-icon="mdi-pencil"
                    block
                    class="mb-2"
                  >
                    Editar Evento
                  </v-btn>
                  <v-btn
                    :to="`/events/${event.id}/manage-schedule`"
                    color="info"
                    variant="elevated"
                    prepend-icon="mdi-calendar-edit"
                    block
                    class="mb-2"
                  >
                    Gerenciar Programação
                  </v-btn>
                  <v-btn
                    @click="deleteEvent"
                    color="error"
                    variant="elevated"
                    prepend-icon="mdi-delete"
                    block
                  >
                    Remover Evento
                  </v-btn>
                </v-card-text>
              </v-card>
              <!-- Participant Inscription -->
              <v-card
                v-if="user && event.organizer_id !== user.id"
                class="action-card elevation-3 mb-4"
              >
                <v-card-title class="primary--text">
                  <v-icon class="me-2">mdi-account-plus</v-icon>
                  Inscrição
                </v-card-title>
                <v-card-text>
                  <div class="mb-3">
                    <v-icon small class="me-1">mdi-calendar-range</v-icon>
                    <strong>Período de Inscrição:</strong><br />
                    {{ formatDateTime(event.inscription_start_date) }} a
                    {{ formatDateTime(event.inscription_end_date) }}
                  </div>
                  <v-divider class="my-3"></v-divider>
                  <v-btn
                    v-if="isInscribed"
                    @click="showCheckinDialog = true"
                    color="teal"
                    variant="flat"
                    block
                    class="mb-2"
                  >
                    Fazer Check-in
                  </v-btn>
                  <v-btn
                    v-if="isInscriptionOpen && !isInscribed"
                    @click="inscribe"
                    color="primary"
                    variant="elevated"
                    prepend-icon="mdi-check-circle"
                    block
                  >
                    Inscrever-se
                  </v-btn>
                  <v-btn
                    v-if="isInscribed"
                    :color="showCancelButton ? 'error' : 'success'"
                    variant="elevated"
                    block
                    @mouseover="showCancelButton = true"
                    @mouseleave="showCancelButton = false"
                    @click="showCancelButton ? cancelInscription() : null"
                  >
                    <v-icon class="me-2">{{
                      showCancelButton ? 'mdi-close-circle' : 'mdi-check-circle'
                    }}</v-icon>
                    {{ showCancelButton ? 'Cancelar inscrição' : 'Você está inscrito' }}
                  </v-btn>
                  <v-btn
                    v-if="isInscribed && isEventFinished"
                    @click="downloadCertificate"
                    color="primary"
                    variant="elevated"
                    prepend-icon="mdi-download"
                    block
                    class="mt-2"
                  >
                    Baixar Certificado
                  </v-btn>
                  <v-btn
                    v-if="!isInscriptionOpen"
                    variant="elevated"
                    block
                    disabled
                    prepend-icon="mdi-clock-outline"
                  >
                    Inscrições Encerradas
                  </v-btn>
                </v-card-text>
              </v-card>
              <!-- Speaker Submission -->
              <v-card v-if="user && user.role === 2" class="action-card elevation-3 mb-4">
                <v-card-title class="primary--text">
                  <v-icon class="me-2">mdi-file-document</v-icon>
                  Submissão de Trabalhos
                </v-card-title>
                <v-card-text>
                  <div v-if="event.submission_start_date" class="mb-3">
                    <v-icon small class="me-1">mdi-calendar-range</v-icon>
                    <strong>Período de Submissão:</strong><br />
                    {{ formatDateTime(event.submission_start_date) }} a
                    {{ formatDateTime(event.submission_end_date) }}
                  </div>
                  <v-divider class="my-3"></v-divider>
                  <v-btn
                    v-if="isSubmissionOpen"
                    :to="`/events/${event.id}/submit`"
                    color="info"
                    variant="elevated"
                    prepend-icon="mdi-file-plus"
                    block
                  >
                    Enviar Trabalho
                  </v-btn>
                  <v-btn
                    v-if="!isSubmissionOpen"
                    variant="elevated"
                    block
                    disabled
                    prepend-icon="mdi-clock-outline"
                  >
                    Submissões Encerradas
                  </v-btn>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>

      <!-- Organizer Management Section -->
      <v-row v-if="user && event.organizer_id === user.id" class="mb-6">
        <v-col cols="12" md="4">
          <!-- Manage Check-in -->
          <v-card class="action-card elevation-3 organizer-management-card">
            <v-card-title class="primary--text">
              <v-icon class="me-2">mdi-check-circle</v-icon>
              Gerenciar Check-in das Atividades
              <v-spacer></v-spacer>
              <v-btn icon @click="showCheckinSection = !showCheckinSection">
                <v-icon>{{ showCheckinSection ? 'mdi-chevron-up' : 'mdi-chevron-down' }}</v-icon>
              </v-btn>
            </v-card-title>
            <v-card-text v-if="showCheckinSection">
              <v-list v-if="activities.length > 0">
                <v-list-item v-for="activity in activities" :key="activity.id">
                  <v-list-item-content>
                    <v-list-item-title>{{ activity.title }}</v-list-item-title>
                    <v-list-item-subtitle>{{ formatDateTime(activity.start_time) }} - {{ formatDateTime(activity.end_time) }}</v-list-item-subtitle>
                    <div v-if="activity.check_in_open" class="mt-2">
                      <p class="text-h4 text-center my-2">{{ activity.check_in_code }}</p>
                      <p class="text-caption text-center">
                        Instrua os participantes a usarem este código para o check-in.
                      </p>
                      <v-btn @click="closeCheckin(activity.id)" color="warning" size="small" class="mt-2">
                        Encerrar Check-in
                      </v-btn>
                    </div>
                    <div v-else class="mt-2">
                      <p class="text-caption">
                        Abra o check-in para gerar um código e permitir a entrada dos participantes.
                      </p>
                      <v-btn @click="openCheckin(activity.id)" color="success" size="small" class="mt-2">
                        Abrir Check-in
                      </v-btn>
                    </div>
                    <p class="text-body-2 mt-2">
                      Participantes Registrados: {{ activity.attendees_count || 0 }}
                    </p>
                  </v-list-item-content>
                </v-list-item>
              </v-list>
              <p v-else>A programação deste evento ainda não foi divulgada.</p>
              <v-alert v-if="checkinError" type="error" class="mt-4">{{ checkinError }}</v-alert>
              <v-alert v-if="checkinMessage" type="success" class="mt-4">{{ checkinMessage }}</v-alert>
            </v-card-text>
          </v-card>
        </v-col>
        <v-col cols="12" md="4">
          <!-- Participants List -->
          <v-card class="action-card elevation-3 organizer-management-card">
            <v-card-title class="primary--text">
              <v-icon class="me-2">mdi-account-multiple</v-icon>
              Participantes Inscritos ({{ event.participants?.length || 0 }})
              <v-spacer></v-spacer>
              <v-btn icon @click="showParticipantsSection = !showParticipantsSection">
                <v-icon>{{ showParticipantsSection ? 'mdi-chevron-up' : 'mdi-chevron-down' }}</v-icon>
              </v-btn>
            </v-card-title>
            <v-card-text v-if="showParticipantsSection">
              <v-btn
                v-if="event.participants?.length > 0"
                @click="exportParticipants"
                color="secondary"
                size="small"
                class="mb-4"
              >
                Exportar para CSV
              </v-btn>
              <v-list v-if="event.participants?.length > 0">
                <v-list-item v-for="participant in event.participants" :key="participant.id">
                  {{ participant.name }} ({{ participant.email }})
                </v-list-item>
              </v-list>
              <p v-else>Ainda não há participantes inscritos neste evento.</p>
            </v-card-text>
          </v-card>
        </v-col>
        <v-col cols="12" md="4">
          <!-- Submissions List -->
          <v-card class="action-card elevation-3 organizer-management-card">
            <v-card-title class="primary--text">
              <v-icon class="me-2">mdi-file-document-multiple</v-icon>
              Trabalhos Submetidos ({{ event.submissions?.length || 0 }})
              <v-spacer></v-spacer>
              <v-btn icon @click="showSubmissionsSection = !showSubmissionsSection">
                <v-icon>{{ showSubmissionsSection ? 'mdi-chevron-up' : 'mdi-chevron-down' }}</v-icon>
              </v-btn>
            </v-card-title>
            <v-card-text v-if="showSubmissionsSection">
              <v-card v-for="sub in event.submissions" :key="sub.id" class="mb-2">
                <v-card-title>{{ sub.title }}</v-card-title>
                <v-card-text>
                  <p><strong>Autor:</strong> {{ sub.author?.name }} ({{ sub.author?.email }})</p>
                  <p>
                    <strong>Arquivo:</strong>
                    <a :href="`/api/submissions/${sub.id}/download`" target="_blank">{{
                      sub.file_path
                    }}</a>
                  </p>
                </v-card-text>
                <v-card-actions>
                  <v-chip :color="getStatusColor(sub.status)" size="small">
                    {{ getStatusText(sub.status) }}
                  </v-chip>
                  <v-spacer></v-spacer>
                  <template v-if="sub.status === 1">
                    <v-btn @click="confirmEvaluateSubmission(sub.id, 3, 'aprovar')" color="success" size="small">
                      Aprovar
                    </v-btn>
                    <v-btn @click="confirmEvaluateSubmission(sub.id, 4, 'rejeitar')" color="error" size="small" class="ml-2">
                      Rejeitar
                    </v-btn>
                  </template>
                </v-card-actions>
              </v-card>
              <p v-if="!event.submissions?.length">
                Nenhum trabalho foi submetido a este evento ainda.
              </p>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <!-- Quem Vai (Networking) -->
      <v-card v-if="user && isInscribed" class="mb-4">
        <v-card-title>
          <v-icon class="me-2">mdi-account-network</v-icon>
          Quem Vai (Networking)
        </v-card-title>
        <v-card-text>
          <p class="text-caption mb-4">
            Esta lista mostra outros participantes que optaram por compartilhar seu perfil
            publicamente neste evento.
          </p>
          <v-list v-if="event.public_participants && event.public_participants.length > 0">
            <v-list-item v-for="participant in event.public_participants" :key="participant.id">
              <span v-if="participant.id !== user.id">{{ participant.name }}</span>
              <span v-else
                ><strong>{{ participant.name }} (Você)</strong></span
              >
            </v-list-item>
          </v-list>
          <p v-else>
            Nenhum participante habilitou o perfil público para este evento ainda. Você pode
            habilitar o seu em "Meu Perfil".
          </p>
        </v-card-text>
      </v-card>

      <!-- Schedule -->
      <v-card>
        <v-card-title>
          <v-icon class="me-2">mdi-calendar-clock</v-icon>
          Programação
        </v-card-title>
        <v-card-text>
          <v-btn
            v-if="showCalendar"
            @click="showCalendar = false"
            color="secondary"
            variant="outlined"
            class="mb-2"
          >
            Ocultar Calendário
          </v-btn>
          <v-btn
            v-else
            @click="showCalendar = true"
            color="primary"
            variant="outlined"
            class="mb-2"
          >
            Mostrar Calendário
          </v-btn>
          <div v-if="showCalendar">
            <FullCalendar v-if="event.start_date" :options="calendarOptions" />
            <div v-else class="text-center py-4">
              <v-progress-circular indeterminate color="primary"></v-progress-circular>
              <p class="mt-2">Carregando programação...</p>
            </div>
          </div>
          <p v-if="activities.length === 0">A programação deste evento ainda não foi divulgada.</p>
        </v-card-text>
      </v-card>

      <v-dialog v-model="showCheckinDialog" max-width="500px">
        <v-card>
          <v-card-title>Fazer Check-in</v-card-title>
          <v-card-text>
            <p>Digite o código fornecido pelo organizador da atividade:</p>
            <v-text-field
              v-model="checkinForm.code"
              label="Código de Check-in"
              class="mt-4"
              autofocus
            ></v-text-field>
            <v-alert v-if="checkinForm.error" type="error" class="mt-2">{{
              checkinForm.error
            }}</v-alert>
            <v-alert v-if="checkinForm.message" type="success" class="mt-2">{{
              checkinForm.message
            }}</v-alert>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn text @click="showCheckinDialog = false">Cancelar</v-btn>
            <v-btn color="primary" @click="submitCheckin">Confirmar Presença</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-container>
  </div>
</template>

<script>
import axios from 'axios';
import FullCalendar from '@fullcalendar/vue3';
import dayGridPlugin from '@fullcalendar/daygrid';
import timeGridPlugin from '@fullcalendar/timegrid';

export default {
  name: 'EventDetail',
  components: {
    FullCalendar,
  },
  props: ['id'],
  data() {
    return {
      event: {},
      activities: [],
      isInscriptionOpen: false,
      isSubmissionOpen: false,
      isInscribed: false,
      user: null,
      showCancelButton: false,
      showCheckinDialog: false,
      showCalendar: true,
      checkinForm: {
        code: '',
        error: '',
        message: '',
      },
      checkinError: '',
      checkinMessage: '',
      showCheckinSection: false,
      showParticipantsSection: false,
      showSubmissionsSection: false,
      calendarOptions: {
        plugins: [dayGridPlugin, timeGridPlugin],
        initialView: 'timeGridDay',
        initialDate: null, // Will be set to event start
        headerToolbar: {
          left: 'prev,next today',
          center: 'title',
          right: 'dayGridMonth,timeGridWeek,timeGridDay',
        },
        editable: false, // Leitura-apenas
        events: [],
        slotMinTime: '00:00:00',
        slotMaxTime: '23:59:00',
        height: 600,
        scrollTime: '12:00:00', // Default to noon
        scrollTimeReset: false,
        slotLabelFormat: {
          hour: '2-digit',
          minute: '2-digit',
          hour12: false
        },
        eventTimeFormat: {
          hour: '2-digit',
          minute: '2-digit',
          hour12: false
        },
      },
    };
  },
  computed: {
    isEventFinished() {
      if (this.event && this.event.end_date) {
        return new Date(this.event.end_date) < new Date();
      }
      return false;
    },
  },
  async created() {
    await this.loadData();
  },
  watch: {
    event: {
      handler(newEvent) {
        if (newEvent && newEvent.start_date) {
          // Atualiza initialDate quando o evento carrega
          this.calendarOptions.initialDate = newEvent.start_date;
          
          // Calcula a duração e define o initialView
          const eventStart = new Date(newEvent.start_date);
          const eventEnd = new Date(newEvent.end_date);
          const durationMs = eventEnd.getTime() - eventStart.getTime();
          const durationDays = durationMs / (1000 * 60 * 60 * 24);

          if (durationDays <= 1) {
            this.calendarOptions.initialView = 'timeGridDay';
          } else if (durationDays <= 7) {
            this.calendarOptions.initialView = 'timeGridWeek';
          } else {
            this.calendarOptions.initialView = 'dayGridMonth';
          }
        }
      },
      deep: true
    }
  },
  methods: {
    async loadData() {
      try {
        const response = await axios.get('/api/');
        if (response.data.authenticated) {
          this.user = response.data.user;
        }
        const eventResponse = await axios.get(`/api/events/${this.id}`);
        this.event = eventResponse.data.event;
        this.activities = eventResponse.data.activities;
        this.isInscriptionOpen = eventResponse.data.is_inscription_open;
        this.isSubmissionOpen = eventResponse.data.is_submission_open;
        this.isInscribed = this.user && this.event.participants?.some((p) => p.id === this.user.id);

        // Set initial date to event start
        this.calendarOptions.initialDate = this.event.start_date;

        // Calcula a duração do evento em dias
        const eventStart = new Date(this.event.start_date);
        const eventEnd = new Date(this.event.end_date);
        const durationMs = eventEnd.getTime() - eventStart.getTime();
        const durationDays = durationMs / (1000 * 60 * 60 * 24);

        // Define o initialView baseado na duração
        if (durationDays <= 1) {
          this.calendarOptions.initialView = 'timeGridDay';
        } else if (durationDays <= 7) {
          this.calendarOptions.initialView = 'timeGridWeek';
        } else {
          this.calendarOptions.initialView = 'dayGridMonth';
        }

        // Mapeia as atividades para o formato do FullCalendar
        this.calendarOptions.events = this.activities.map((act) => ({
          id: act.id,
          title: act.title,
          start: act.start_time,
          end: act.end_time,
          description: act.description, // Podemos usar isso em popups futuros
          location: act.location,
        }));

        // Set scrollTime to first activity or noon
        if (this.activities.length > 0) {
          const firstActivity = this.activities.sort(
            (a, b) => new Date(a.start_time) - new Date(b.start_time)
          )[0];
          const startTime = new Date(firstActivity.start_time);
          this.calendarOptions.scrollTime = startTime.toTimeString().slice(0, 5) + ':00';
        } else {
          this.calendarOptions.scrollTime = '12:00:00';
        }
      } catch (err) {
        console.error(err);
      }
    },
    formatDateTime(dateString) {
      const date = new Date(dateString);
      return date.toLocaleString('pt-BR');
    },
    async inscribe() {
      try {
        await axios.post(`/api/events/${this.id}/inscribe`);
        await this.loadData();
      } catch (err) {
        console.error(err);
      }
    },
    async submitCheckin() {
      this.checkinForm.error = '';
      this.checkinForm.message = '';
      if (!this.checkinForm.code) {
        this.checkinForm.error = 'O código é obrigatório.';
        setTimeout(() => { this.checkinForm.error = ''; }, 10000);
        return;
      }

      try {
        const response = await axios.post('/api/checkin', {
          code: this.checkinForm.code,
        });
        this.checkinForm.message = response.data.message;
        setTimeout(() => { this.checkinForm.message = ''; }, 10000);
        this.checkinForm.code = ''; // Limpa o campo
        // Fecha o dialog após 2 segundos
        setTimeout(() => {
          this.showCheckinDialog = false;
        }, 2000);
      } catch (err) {
        this.checkinForm.error = err.response?.data?.error || 'Erro ao processar check-in.';
        setTimeout(() => { this.checkinForm.error = ''; }, 10000);
      }
    },
    async cancelInscription() {
      try {
        await axios.delete(`/api/events/${this.id}/inscribe`);
        await this.loadData();
      } catch (err) {
        console.error(err);
      }
    },
    async deleteEvent() {
      if (confirm('Tem certeza que deseja remover este evento?')) {
        try {
          await axios.delete(`/api/events/${this.id}`);
          this.$router.push('/dashboard');
        } catch (err) {
          console.error(err);
        }
      }
    },
    async downloadCertificate() {
      try {
        // Abre o link da API em uma nova aba; o backend forçará o download.
        window.open(`/api/events/${this.event.id}/certificate`, '_blank');
        await this.loadData();
      } catch (err) {
        console.error(err);
      }
    },
    async exportParticipants() {
      try {
        // Trigger download
        window.open(`/api/events/${this.event.id}/export_participants`, '_blank');
      } catch (err) {
        console.error(err);
      }
    },
    async confirmEvaluateSubmission(subId, status, action) {
      if (confirm(`Você tem certeza que quer ${action} esta submissão?`)) {
        await this.evaluateSubmission(subId, status);
      }
    },
    async evaluateSubmission(subId, status) {
      const allowedStatuses = [3, 4]; // 3: Aprovar, 4: Rejeitar
      if (!allowedStatuses.includes(status)) {
        console.error('Status inválido para avaliação de submissão:', status);
        return;
      }
      try {
        await axios.post(`/api/submissions/${subId}/evaluate`, {
          new_status: status,
        });
        await this.loadData();
      } catch (err) {
        console.error(err);
      }
    },
    getStatusColor(status) {
      switch (status) {
        case 1:
          return 'info';
        case 3:
          return 'success';
        case 4:
          return 'error';
        default:
          return 'default';
      }
    },
    getStatusText(status) {
      switch (status) {
        case 1:
          return 'Submetido';
        case 3:
          return 'Aprovado';
        case 4:
          return 'Rejeitado';
        default:
          return 'Em avaliação';
      }
    },
    // Check-in methods
    async openCheckin(activityId) {
      this.checkinError = '';
      this.checkinMessage = '';
      try {
        await axios.post(`/api/activities/${activityId}/open-checkin`);
        this.checkinMessage = 'Check-in aberto!';
        setTimeout(() => { this.checkinMessage = ''; }, 10000);
        await this.loadData(); // Recarrega os dados da atividade (código, status)
      } catch (err) {
        this.checkinError = err.response?.data?.error || 'Erro ao abrir check-in.';
        setTimeout(() => { this.checkinError = ''; }, 10000);
      }
    },
    async closeCheckin(activityId) {
      this.checkinError = '';
      this.checkinMessage = '';
      try {
        await axios.post(`/api/activities/${activityId}/close-checkin`);
        this.checkinMessage = 'Check-in encerrado!';
        setTimeout(() => { this.checkinMessage = ''; }, 10000);
        await this.loadData(); // Recarrega os dados da atividade
      } catch (err) {
        this.checkinError = err.response?.data?.error || 'Erro ao fechar check-in.';
        setTimeout(() => { this.checkinError = ''; }, 10000);
      }
    },
  },
};
</script>

<style scoped>
.event-detail-section {
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  min-height: 100vh;
  padding: 2rem 0 20px 0;
}

.main-card {
  border-radius: 12px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.action-card {
  border-radius: 12px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.date-info {
  background-color: rgba(25, 118, 210, 0.1);
  padding: 12px;
  border-radius: 8px;
  border-left: 4px solid #1976d2;
}

.event-description {
  line-height: 1.6;
}

@media (max-width: 600px) {
  .event-detail-section {
    padding: 2rem 10px 10px 10px;
  }
}

/* Rest of existing styles */
.v-card {
  margin-bottom: 20px;
}

.v-card-title {
  font-size: 1.5rem;
  font-weight: 500;
}

.v-card-subtitle {
  font-size: 1rem;
  color: #666;
}

.v-card-text {
  padding: 16px;
}

.v-divider {
  margin: 16px 0;
}

.v-btn {
  text-transform: none;
}

.v-list-item {
  padding: 12px 16px;
}

.v-list-item-title {
  font-weight: 500;
}

.v-list-item-subtitle {
  font-size: 0.875rem;
  color: #666;
}

.v-chip {
  font-size: 0.875rem;
  font-weight: 500;
}

.organizer-management-card {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.organizer-management-card .v-card-text {
  flex: 1;
  overflow-y: auto;
}
</style>
