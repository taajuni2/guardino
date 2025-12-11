import { Component, OnInit } from '@angular/core';
import {AuthService} from "../../services/auth-service/auth.service";
import {Router} from "@angular/router";

@Component({
  selector: 'app-auth-page',
  templateUrl: './auth-page.component.html',
  styleUrl: './auth-page.component.scss'
})
export class AuthPageComponent implements OnInit {
  username = '';
  password = '';
  error = '';
  constructor(private auth: AuthService, private router: Router) {}

  onSubmit() {
    const ok = this.auth.login(this.username, this.password).subscribe(res => {
      console.log(res);
      this.auth.storeTokens(res.access_token)
      this.router.navigate(['/dashboard']).then(r =>  console.log("Login Sucessfull", ok))
    })
  }
  ngOnInit(): void {

  }

  register() {
    this.auth.register("admin", "admin", "nicolas.julier@test.ch").subscribe(result => {
    })
  }

}

