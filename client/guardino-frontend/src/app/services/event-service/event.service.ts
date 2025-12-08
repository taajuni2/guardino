import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";
import {environment} from "../../../environment/environment";
import {Event, EventsGrouped, AgentLifecycle } from "../../../entities/Events";

@Injectable({
  providedIn: 'root'
})
export class EventService {

  constructor(private http: HttpClient) { }




  getGroupedEvents(): Observable<EventsGrouped[]> {
    return this.http.get<EventsGrouped[]>(`${environment.apiUrl}/events/grouped`);
  }

}

