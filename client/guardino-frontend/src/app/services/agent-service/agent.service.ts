import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import {environment} from "../../../environment/environment";
import {Observable} from "rxjs";
import {Agent} from "../../../entities/Agent";
import {Router} from "@angular/router";

@Injectable({
  providedIn: 'root'
})
export class AgentService {


  constructor(private http: HttpClient, private router: Router) { }


  getAgents(): Observable<Agent[]> {
    return this.http.get<Agent[]>(`${environment.apiUrl}/agents/all`);
  }

}
