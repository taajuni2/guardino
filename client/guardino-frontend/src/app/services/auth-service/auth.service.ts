// auth.service.ts
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import {BehaviorSubject, Observable} from "rxjs";
import {authResponse, User} from "../../../entities/User";
import {environment} from "../../../environment/environment";
import {HttpClient} from "@angular/common/http";

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private API_URL = environment.apiUrl;
  private currentUserSubject = new BehaviorSubject<User | null>(this.loadUserFromStorage());
  currentUser$ = this.currentUserSubject.asObservable();
  public isAuthenticated: boolean = !!localStorage.getItem('access_token');
  private accessToken = "";

  constructor(private router: Router, private http: HttpClient) {}

  public login(name: string, password: string): Observable<authResponse> {
    console.log(name, password);
    return this.http.post<authResponse>(this.API_URL + "/auth/login", {name: name, password: password});
  }

  public register(name: string, password: string, email: string): Observable<authResponse> {
    return this.http.post<authResponse>(this.API_URL + "/auth/register", {name: name, password: password, email: email});
  }


  public logout(){
    localStorage.clear();
    this.router.navigate(['/login']);
  }



  public storeTokens(token: string) {
    this.accessToken = token;
    localStorage.setItem('access_token', token);
  }


  private loadUserFromStorage(): User | null {
    const raw = localStorage.getItem('auth_user');
    return raw ? JSON.parse(raw) : null;
  }

  getAccessToken(): string | null {
    return localStorage.getItem('access_token');
  }
}
