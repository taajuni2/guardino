import {Component, OnInit} from '@angular/core';
import {EventService, UnifiedEvent} from "../../../../services/event-service/event.service";
import {Event} from "../../../../../entities/Events";

interface TimelineEvent {
  title: string;
  agentName: string;
  agent: string;
  description: string | null;
  timestamp: string;
  severity: 'info' | 'warning' | 'critical';
}

@Component({
  selector: 'app-event-timeline',
  templateUrl: './event-timeline.component.html',
  styleUrl: './event-timeline.component.scss'
})
export class EventTimelineComponent implements  OnInit {
  events: TimelineEvent[] = [];

  constructor(private eventService: EventService) {
  }


  ngOnInit(): void {
    this.eventService.allEvents$.subscribe(rawEvents => {
      this.events = rawEvents.map(ev => this.mapEvent(ev));
      console.log(this.events);
    });
  }

  private mapEvent(ev: Event): TimelineEvent {
    if (!ev.paths || ev.paths.length === 0) {
      return {
        title: ev.summary ?? 'Unknown Event',
        agentName: ev.agent_id ?? 'Unknown Agent',
        agent: ev.agent_id ?? 'N/A',
        description: ev.summary ?? 'Unknown Event',
        timestamp: new Date(ev.ts).toLocaleString(),
        severity: (ev.severity as any) ?? 'info'
      };
    }

    // Event mit paths
    return {
      title: ev.summary ?? 'Unknown Event',
      agentName: ev.agent_id ?? 'Unknown Agent',
      agent: ev.agent_id ?? 'N/A',
      description: ev.paths[0],
      timestamp: new Date(ev.ts).toLocaleString(),
      severity: (ev.severity as any) ?? 'info'
    };
  }

}
