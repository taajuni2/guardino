import { Injectable } from '@angular/core';
import { HttpClient } from "@angular/common/http";
import { BehaviorSubject, Observable } from "rxjs";
import { environment } from "../../../environment/environment";
import { Event, EventsGrouped, AgentLifecycle } from "../../../entities/Events";
import {WebsocketService} from "../websocket-service/websocket.service";

export type UnifiedEvent = Event | AgentLifecycle; // falls beide gleiche Felder wie ts haben

@Injectable({
  providedIn: 'root'
})
export class EventService {
  private allEventsSubject = new BehaviorSubject<UnifiedEvent[]>([]);
  allEvents$ = this.allEventsSubject.asObservable();


  constructor(
    private http: HttpClient,
    private websocketService: WebsocketService
  ) {
    // Initiale Ladung aus dem Backend
    this.loadInitialEvents();

    // Live-Events aus dem WebSocket
    this.websocketService.events$.subscribe(newEvent => {
      this.addEvent(newEvent);
    });
  }

  // Falls du manuell reloaden willst
  refresh(): void {
    this.loadInitialEvents();
  }

  getSnapshot(): UnifiedEvent[] {
    return this.allEventsSubject.value;
  }

  // ---------- intern ----------

  private loadInitialEvents(): void {
    this.http.get<EventsGrouped>(`${environment.apiUrl}/events/grouped`)
      .subscribe(grouped => {
        let all: UnifiedEvent[] = [
          ...grouped.events,
          ...grouped.lifecycle
        ];

        // register-Events rausfiltern
        all = all.filter(ev => ev.event_type !== 'register');

        // nach ts sortieren: neueste zuerst
        all.sort((a, b) =>
          new Date(b.ts).getTime() - new Date(a.ts).getTime()
        );


        this.allEventsSubject.next(all);
      });
  }

  private addEvent(newEvent: Event): void {
    if (newEvent.event_type === 'register') {
      return;
    }

    const current = this.allEventsSubject.value;

    // neues Event **oben** einfügen
    let updated: UnifiedEvent[] = [newEvent, ...current];

    // optional nochmal sortieren (falls Timestamps knapp sind)
    updated.sort((a, b) =>
      new Date(b.ts).getTime() - new Date(a.ts).getTime()
    );

    this.allEventsSubject.next(updated);
  }
}
