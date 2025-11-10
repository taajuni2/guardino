import { Component } from '@angular/core';
import {AuthService} from "../../services/auth-service/auth.service";
import {Router} from "@angular/router";

@Component({
  selector: 'app-auth-page',
  templateUrl: './auth-page.component.html',
  styleUrl: './auth-page.component.scss'
})
export class AuthPageComponent {
  username = '';
  password = '';
  error = '';
  constructor(private auth: AuthService, private router: Router) {}

  onSubmit() {
    const ok = this.auth.login(this.username, this.password);
    if (ok) {
      this.router.navigate(['/dashboard']);
    } else {
      this.error = 'Invalid credentials';
    }
  }
}
