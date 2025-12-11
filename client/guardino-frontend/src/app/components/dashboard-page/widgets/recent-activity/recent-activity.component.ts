import {Component, OnInit} from '@angular/core';
import {EventService} from "../../../../services/event-service/event.service";
import {AgentLifecycle, Event} from "../../../../../entities/Events";
import {WebsocketService} from "../../../../services/websocket-service/websocket.service";

@Component({
  selector: 'app-recent-activity',
  templateUrl: './recent-activity.component.html',
  styleUrl: './recent-activity.component.scss'
})

export class RecentActivityComponent implements OnInit {
  public allEvents: Array<Event | AgentLifecycle> = [];

  constructor(private eventService: EventService, private websocketService: WebsocketService) {
  }

  ngOnInit() {
    this.eventService.allEvents$.subscribe(events => {
      this.allEvents = events;
    });
  }
}
