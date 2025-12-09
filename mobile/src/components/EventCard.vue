<template>
  <ion-card :router-link="`/tabs/events/${event.id}`" button>
    <img v-if="event.image_url" :src="event.image_url" alt="Event Image" class="event-image" />
    <div v-else class="placeholder-image">
      <ion-icon :icon="imageOutline" class="placeholder-icon"></ion-icon>
    </div>
    
    <ion-card-header>
      <div class="status-badge" v-if="event.status !== undefined">
        <ion-badge :color="event.status === 2 ? 'success' : 'warning'">
          {{ event.status === 2 ? 'Publicado' : 'Rascunho' }}
        </ion-badge>
      </div>
      <ion-card-subtitle>{{ formatDate(event.start_date) }}</ion-card-subtitle>
      <ion-card-title>{{ event.title }}</ion-card-title>
    </ion-card-header>

    <ion-card-content>
      {{ truncate(event.description, 100) }}
    </ion-card-content>
  </ion-card>
</template>

<script setup lang="ts">
import { IonCard, IonCardHeader, IonCardSubtitle, IonCardTitle, IonCardContent, IonBadge, IonIcon } from '@ionic/vue';
import { imageOutline } from 'ionicons/icons';
import { formatDate, truncate } from '@/utils/formatters';

defineProps<{
  event: any;
}>();
</script>

<style scoped>
.event-image {
  width: 100%;
  height: 150px;
  object-fit: cover;
}

.placeholder-image {
  height: 150px;
  background-color: #f0f0f0;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.placeholder-icon {
  font-size: 48px;
  color: #ccc;
}

.status-badge {
  margin-bottom: 8px;
}
</style>
