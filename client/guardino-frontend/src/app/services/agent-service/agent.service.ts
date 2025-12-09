import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import {environment} from "../../../environment/environment";
import {BehaviorSubject, interval, Observable, switchMap} from "rxjs";
import {Agent} from "../../../entities/Agent";
import {Router} from "@angular/router";

@Injectable({
  providedIn: 'root'
})
export class AgentService {

  private agentsSubject = new BehaviorSubject<Agent[]>([]);
  agents$ = this.agentsSubject.asObservable();
  constructor(private http: HttpClient, private router: Router) { }


  getAgents(): Observable<Agent[]> {
    return this.http.get<Agent[]>(`${environment.apiUrl}/agents/all`);
  }

  startPolling() {
    interval(5000)
      .pipe(
        switchMap(() => this.http.get<Agent[]>('/agents/all'))
      )
      .subscribe(agents => {
        this.agentsSubject.next(agents); // einfach ersetzen
      });
  }

}
