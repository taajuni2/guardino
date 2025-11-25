// auth.guard.ts
import { Injectable } from '@angular/core';
import { CanActivate, Router } from '@angular/router';
import { AuthService } from './services/auth-service/auth.service';
import { HttpClient } from '@angular/common/http';

@Injectable({ providedIn: 'root' })
export class AuthGuard implements CanActivate {
  constructor(private auth: AuthService, private router: Router) {}

  canActivate(): boolean {
    console.log('isAuthenticated', this.auth.isAuthenticated);
    if (this.auth.isAuthenticated) {
      return true;
    }

    // nicht eingeloggt → zurück zum Login
    this.router.navigate(['/login']);
    return false;
  }
}
