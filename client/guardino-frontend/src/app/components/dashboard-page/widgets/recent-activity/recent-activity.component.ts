import {Component, OnInit} from '@angular/core';
import {EventService} from "../../../../services/event-service/event.service";
import {AgentLifecycle, Event} from "../../../../../entities/Events";

@Component({
  selector: 'app-recent-activity',
  templateUrl: './recent-activity.component.html',
  styleUrl: './recent-activity.component.scss'
})

export class RecentActivityComponent implements OnInit {
  public allEvents: Array<Event | AgentLifecycle> = [];

  constructor(private eventService: EventService) {
  }

  ngOnInit() {
    this.eventService.getGroupedEvents().subscribe(groupedEvents => {
      this.allEvents = [...groupedEvents.events, ...groupedEvents.lifecycle];
      console.log(this.allEvents);
      this.allEvents = this.allEvents.filter(ev => ev.event_type !== "register");
      this.allEvents.sort((a, b) => new Date(b.ts).getTime() - new Date(a.ts).getTime());
    })
  }
}
