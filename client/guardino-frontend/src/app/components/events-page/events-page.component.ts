import {Component, OnInit} from '@angular/core';
import {EventService} from "../../services/event-service/event.service";
import {EventStat} from "../../../entities/EventStats";

@Component({
  selector: 'app-events-page',
  templateUrl: './events-page.component.html',
  styleUrl: './events-page.component.scss'
})
export class EventsPageComponent implements OnInit {

  stats: EventStat[] = [];

  constructor(private eventService: EventService) {
  }

  ngOnInit(): void {

    this.eventService.allEvents$.subscribe(events => {

      const total = events.length;
      const critical = events.filter(e => e.severity === 'critical').length;
      const warning = events.filter(e => e.severity === 'warning').length;

      // Last hour
      const oneHourAgo = Date.now() - 60 * 60 * 1000;
      const lastHour = events.filter(e => new Date(e.ts).getTime() >= oneHourAgo).length;

      // Threats aus threatsByAgent$ separat holen
      this.eventService.threatsByAgent$.subscribe(threatMap => {

        const threats = Object.values(threatMap)
          .reduce((sum, x) => sum + x, 0);

        // Jetzt das Array aktualisieren
        this.stats = [
          {label: 'Total Events', icon: 'list', value: total},
          {label: 'Critical', icon: 'error', value: critical, tone: 'danger'},
          {label: 'Warning', icon: 'warning', value: warning, tone: 'warn'},
          {label: 'Threats', icon: 'security', value: threats},
          {label: 'Last Hour', icon: 'schedule', value: lastHour}
        ];
      });
    });
  }
}
