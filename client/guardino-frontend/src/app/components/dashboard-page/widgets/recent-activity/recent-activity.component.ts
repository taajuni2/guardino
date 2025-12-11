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
    // this.eventService.getGroupedEvents().subscribe(groupedEvents => {
    //   this.allEvents = [...groupedEvents.events, ...groupedEvents.lifecycle];
    //   this.allEvents = this.allEvents.filter(ev => ev.event_type !== "register");
    //   this.allEvents.sort((a, b) => new Date(b.ts).getTime() - new Date(a.ts).getTime());
    // })

    this.websocketService.connect();
    this.websocketService.events$.subscribe(newEvents => {
      console.log("[Websocket] event.push", newEvents.event_type);
      if (newEvents.event_type != "agent_register") {
        this.allEvents.push(newEvents)
        console.log("pushed to all Events")
      } else {
        return;
      }
    })
  }
}
