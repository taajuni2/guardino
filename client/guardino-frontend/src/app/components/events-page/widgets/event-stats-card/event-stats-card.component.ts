import { Component } from '@angular/core';

interface EventStat {
  label: string;
  value: number;
  icon: string;
  tone?: 'danger' | 'warn' | 'muted';
}


@Component({
  selector: 'app-event-stats-card',
  templateUrl: './event-stats-card.component.html',
  styleUrl: './event-stats-card.component.scss'
})
export class EventStatsCardComponent {

  stats: EventStat[] = [
    { label: 'Total Events', value: 10, icon: 'article' },
    { label: 'Critical', value: 1, icon: 'report', tone: 'danger' },
    { label: 'Warning', value: 1, icon: 'warning', tone: 'warn' },
    { label: 'Threats', value: 3, icon: 'security' },
    { label: 'Last Hour', value: 0, icon: 'schedule', tone: 'muted' }
  ];

}
