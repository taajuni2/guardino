import {Component, Input} from '@angular/core';

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
  @Input() eventStats: EventStat[] = [];

}
