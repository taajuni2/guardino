// auth.service.ts
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private _isLoggedIn = false;

  constructor(private router: Router) {}

  get isLoggedIn(): boolean {
    return this._isLoggedIn;
  }

  login(username: string, password: string): boolean {
    console.log('login', username, password);
    // TODO: echten Check machen
    if (username === 'admin' && password === 'admin') {
      this._isLoggedIn = true;
      return true;
    }
    return false;
  }

  logout() {
    this._isLoggedIn = false;
    this.router.navigate(['/login']);
  }
}
