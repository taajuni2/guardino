import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import {environment} from "../../../environment/environment";
import {BehaviorSubject, map, Observable, tap} from "rxjs";
import {User, authResponse} from "../../../entities/User";
import {Router} from "@angular/router";

@Injectable({
  providedIn: 'root'
})
export class AgentService {


  constructor(private http: HttpClient, private router: Router) { }



}
