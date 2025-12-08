import { Component, OnInit } from '@angular/core';
import {EventService} from "../../../../services/event-service/event.service";

@Component({
  selector: 'app-recent-activity',
  templateUrl: './recent-activity.component.html',
  styleUrl: './recent-activity.component.scss'
})
export class RecentActivityComponent implements  OnInit {
constructor(private eventService: EventService) {
}

ngOnInit() {
  this.eventService.getGroupedEvents().subscribe(groupedEvents => {
    console.log(groupedEvents);
  })
}
}
