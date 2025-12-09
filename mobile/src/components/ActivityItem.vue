<template>
  <ion-item>
    <ion-label>
      <h3>{{ activity.title }}</h3>
      <p>{{ formatTime(activity.start || activity.start_time) }} - {{ formatTime(activity.end || activity.end_time) }}</p>
      <p v-if="activity.location">
        <ion-icon :icon="locationOutline" style="vertical-align: middle; margin-right: 4px;"></ion-icon>
        {{ activity.location }}
      </p>
    </ion-label>
    <ion-badge slot="end" :color="activity.checked_in ? 'success' : 'medium'" v-if="activity.type === 'activity' || activity.check_in_open !== undefined">
      {{ activity.checked_in ? 'Check-in OK' : (activity.check_in_open ? 'Check-in Aberto' : 'Pendente') }}
    </ion-badge>
  </ion-item>
</template>

<script setup lang="ts">
import { IonItem, IonLabel, IonBadge, IonIcon } from '@ionic/vue';
import { locationOutline } from 'ionicons/icons';

defineProps<{
  activity: any;
}>();

const formatTime = (timeString: string) => {
  if (!timeString) return '';
  if (timeString.includes('T')) {
      return new Date(timeString).toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });
  }
  return timeString.substring(0, 5);
};
</script>
