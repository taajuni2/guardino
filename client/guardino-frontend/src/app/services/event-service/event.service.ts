import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {BehaviorSubject, interval, Observable, switchMap} from "rxjs";
import {environment} from "../../../environment/environment";
import {Event, EventsGrouped, AgentLifecycle } from "../../../entities/Events";
import {Agent} from "../../../entities/Agent";

@Injectable({
  providedIn: 'root'
})
export class EventService {
  private eventsSubject = new BehaviorSubject<Event[]>([]);
  events$ = this.eventsSubject.asObservable();
  constructor(private http: HttpClient) { }




  getGroupedEvents(): Observable<EventsGrouped> {
    return this.http.get<EventsGrouped>(`${environment.apiUrl}/events/grouped`);
  }

}

